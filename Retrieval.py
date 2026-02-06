import os
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise EnvironmentError("MONGODB_URI not found in .env file")

try:
    client = MongoClient(MONGODB_URI)
    db = client["rag_db"]
    collection = db["CMS-Embeddings"]
    print("Connected to MongoDB")
except Exception as e:
    raise ConnectionError(f"Failed to connect to MongoDB: {e}")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def retrieve_documents(query, k=3):
    print(f"\nUser Query: {query}")

    query_vector = embedding_model.embed_query(query)

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_vector,
                "numCandidates": 100,
                "limit": k
            }
        },
        {
            "$project": {
                "_id": 0,
                "text": 1,
                "metadata": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]

    results = list(collection.aggregate(pipeline))

    if not results:
        print("No matching documents found.")
        return []

    formatted_results = []

    for r in results:
        meta = r.get("metadata", {})
        product_name = meta.get("product_name")
        image_path = meta.get("image_path")

        formatted_results.append({
            "text": r.get("text", ""),
            "score": r.get("score", 0),
            "source": meta.get("source"),
            "product_name": product_name,
            "image_path": image_path,
            "source_file": meta.get("source_file"),
            "page_number": meta.get("page_number"),
            "pdf_path": meta.get("pdf_path")  # NEW
        })

    return formatted_results
