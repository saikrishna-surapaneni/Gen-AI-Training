"""
========================================================
CMS PDF INGESTION PIPELINE (OCR + SMART IMAGE NAMING + STRUCTURED DATA)
========================================================
"""

import os
import re
import fitz
import pandas as pd
import easyocr
import numpy as np  # ✅ ADDED
from pdf2image import convert_from_path

# -------------------------------------------------
# CONFIGURATION
# -------------------------------------------------

PDF_FOLDER = "catalog_data/pdf_catalogs"
TEXT_OUTPUT_FOLDER = "catalog_data/extracted_text"
IMAGE_OUTPUT_FOLDER = "catalog_data/product_images"
STRUCTURED_FOLDER = "catalog_data/structured_data"

POPPLER_PATH = r"C:\Users\ASA solutions\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"

os.makedirs(TEXT_OUTPUT_FOLDER, exist_ok=True)
os.makedirs(IMAGE_OUTPUT_FOLDER, exist_ok=True)
os.makedirs(STRUCTURED_FOLDER, exist_ok=True)

reader = easyocr.Reader(['en'], gpu=False)

# -------------------------------------------------
# STEP 1 — HYBRID TEXT EXTRACTION (Native + EasyOCR)
# -------------------------------------------------
def extract_text_with_ocr(pdf_path, brand_name):
    print(f"Processing text with EasyOCR hybrid: {pdf_path}")

    doc = fitz.open(pdf_path)
    full_text = ""

    for i, page in enumerate(doc):
        text = page.get_text("text")

        if len(text.strip()) < 50:
            print(f"Page {i+1}: Using EasyOCR fallback")
            images = convert_from_path(pdf_path, first_page=i+1, last_page=i+1, poppler_path=POPPLER_PATH)
            image = images[0]

            # ✅ FIX: Convert PIL image to NumPy array for EasyOCR
            results = reader.readtext(np.array(image))
            ocr_text = "\n".join([res[1] for res in results])
            text = ocr_text

        full_text += f"\n\n--- Page {i+1} ---\n{text}"

    text_file_path = os.path.join(TEXT_OUTPUT_FOLDER, f"{brand_name}.txt")

    with open(text_file_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"Saved extracted text → {text_file_path}")

# -------------------------------------------------
# STEP 2 — SMART IMAGE EXTRACTION (UNCHANGED)
# -------------------------------------------------
def extract_images_from_pdf(pdf_path, brand_name):
    print(f"Extracting embedded images with smart naming: {pdf_path}")
    doc = fitz.open(pdf_path)

    for page_index in range(len(doc)):
        page = doc[page_index]
        page_text = page.get_text("text").lower()

        detected_name = None
        sku_match = re.search(r"\b\d{3,}\b", page_text)
        if sku_match:
            detected_name = sku_match.group()

        if not detected_name:
            model_match = re.search(r"(model\s*[:\-]?\s*[a-z0-9\-]+)", page_text)
            if model_match:
                detected_name = model_match.group().replace("model", "").strip()

        if not detected_name:
            detected_name = f"{brand_name}_page{page_index+1}"

        detected_name = re.sub(r"[^a-zA-Z0-9_\-]", "_", detected_name)

        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]

            image_filename = f"{detected_name}_{img_index+1}.{ext}"
            image_path = os.path.join(IMAGE_OUTPUT_FOLDER, image_filename)

            with open(image_path, "wb") as f:
                f.write(image_bytes)

    print(f"Saved intelligently named images for {brand_name}")

# -------------------------------------------------
# STEP 3 — STRUCTURED DATA EXTRACTION (UNCHANGED)
# -------------------------------------------------
def extract_structured_data(brand_name):
    text_file_path = os.path.join(TEXT_OUTPUT_FOLDER, f"{brand_name}.txt")

    if not os.path.exists(text_file_path):
        print(f"No OCR text found for {brand_name}")
        return

    with open(text_file_path, "r", encoding="utf-8") as f:
        text = f.read()

    lines = text.split("\n")

    products = []
    current_product = {"brand": brand_name, "product_name": "", "sku": "", "price": "", "specs": []}

    price_pattern = r"(₹\s?\d+[,\d]*\.?\d*|Rs\.?\s?\d+[,\d]*\.?\d*|\$\s?\d+[,\d]*\.?\d*)"
    sku_pattern = r"(SKU[:\s\-]*[A-Z0-9\-]+)"
    model_pattern = r"(Model[:\s\-]*[A-Z0-9\-]+)"

    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            continue

        sku_match = re.search(sku_pattern, clean_line, re.IGNORECASE)
        if sku_match:
            current_product["sku"] = sku_match.group().replace("SKU", "").replace(":", "").strip()

        model_match = re.search(model_pattern, clean_line, re.IGNORECASE)
        if model_match:
            current_product["product_name"] = model_match.group().replace("Model", "").replace(":", "").strip()

        price_match = re.search(price_pattern, clean_line)
        if price_match:
            current_product["price"] = price_match.group()
            current_product["specs"] = "; ".join(current_product["specs"])
            products.append(current_product.copy())
            current_product = {"brand": brand_name, "product_name": "", "sku": "", "price": "", "specs": []}
            continue

        if any(keyword in clean_line.lower() for keyword in ["watt", "volt", "mm", "kg", "size", "capacity", "speed", "power"]):
            current_product["specs"].append(clean_line)

    if not products:
        print(f"No structured product data detected for {brand_name}")
        return

    new_df = pd.DataFrame(products)
    csv_path = os.path.join(STRUCTURED_FOLDER, "price_list.csv")

    if os.path.exists(csv_path):
        existing_df = pd.read_csv(csv_path)
        existing_df = existing_df[existing_df["brand"] != brand_name]
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        combined_df.to_csv(csv_path, index=False)
    else:
        new_df.to_csv(csv_path, index=False)

    print(f"Saved structured product data for {brand_name} (duplicates prevented)")

# -------------------------------------------------
# MAIN CMS INGESTION PROCESS
# -------------------------------------------------
def process_all_pdfs():
    if not os.path.exists(PDF_FOLDER):
        raise FileNotFoundError(f"Folder not found: {PDF_FOLDER}")

    for file in os.listdir(PDF_FOLDER):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(PDF_FOLDER, file)
            brand_name = os.path.splitext(file)[0]

            print(f"\nProcessing catalog: {brand_name}")

            extract_text_with_ocr(pdf_path, brand_name)
            extract_images_from_pdf(pdf_path, brand_name)
            extract_structured_data(brand_name)

# -------------------------------------------------
# RUN
# -------------------------------------------------
if __name__ == "__main__":
    print("\nStarting CMS PDF Ingestion (EasyOCR Enabled)...\n")
    process_all_pdfs()
    print("\nCMS ingestion completed successfully!\n")
