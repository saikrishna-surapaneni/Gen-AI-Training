import os
import pandas as pd
from pymongo import MongoClient, UpdateOne
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["catalogue_cms"]

STRUCTURED = "catalog_data/structured_data"
os.makedirs(STRUCTURED, exist_ok=True)

def ensure_csv(name, cols):
    path = os.path.join(STRUCTURED, name)
    if not os.path.exists(path):
        pd.DataFrame(columns=cols).to_csv(path, index=False)
        print(f"🆕 Created {name}")
    return path

def upsert_csv(name, collection, keys, cols):
    path = ensure_csv(name, cols)
    df = pd.read_csv(path)

    if df.empty:
        print(f"⚠ {name} empty")
        return

    ops = []
    for row in df.to_dict("records"):
        query = {k: row.get(k) for k in keys if row.get(k)}
        if not query:
            continue
        ops.append(UpdateOne(query, {"$set": row}, upsert=True))

    if ops:
        collection.bulk_write(ops)
        print(f"✅ {name} synced ({len(ops)} records)")

def link_structured_to_embeddings():
    """
    🔗 Attach structured data (price, specs, links) to RAG embedding metadata using SKU
    """
    print("🔄 Linking structured data to embeddings...")

    embed_col = client["rag_db"]["CMS-Embeddings"]
    prices = {p["sku"]: p for p in db.prices.find()}
    links = {l["sku"]: l for l in db.product_links.find()}

    updates = []

    for doc in embed_col.find({"metadata.sku": {"$exists": True}}):
        sku = doc["metadata"].get("sku")
        meta_update = {}

        if sku in prices:
            meta_update["price"] = prices[sku].get("price")
            meta_update["brand"] = prices[sku].get("brand")

        if sku in links:
            meta_update["product_url"] = links[sku].get("product_url")
            meta_update["image_url"] = links[sku].get("image_url")

        if meta_update:
            updates.append(
                UpdateOne(
                    {"_id": doc["_id"]},
                    {"$set": {f"metadata.{k}": v for k, v in meta_update.items()}}
                )
            )

    if updates:
        embed_col.bulk_write(updates)
        print(f"🔗 Linked structured data to {len(updates)} embedding chunks")
    else:
        print("ℹ No SKU matches found for linking")

def run():
    upsert_csv("price_list.csv", db.prices, ["sku"], ["sku","brand","product_name","price"])
    upsert_csv("specifications.csv", db.specifications, ["sku","spec_type"], ["sku","spec_type","spec_value"])
    upsert_csv("product_links.csv", db.product_links, ["sku"], ["sku","product_url","image_url"])

    link_structured_to_embeddings()

if __name__ == "__main__":
    run()
