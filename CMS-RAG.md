### Give Requirement for CMS Rag app

<img width="996" height="588" alt="image" src="https://github.com/user-attachments/assets/fb05551b-bb7a-4ecd-9947-c1657c64ead1" />


  ### Title: Catalogue Intelligence System with RAG
Catalogue Management System + RAG

## 1️⃣ Data Source
o	PDF product catalog
o	Product images
o	Specifications
o	Price information
 This represents real-world catalog data used by estimators and designers.

## 2️⃣ CMS Ingestion (Catalogue Management System)
•	PDF Catalogs
o	PDFs → OCR → extracted text
o	Human validation ensures accuracy of SKUs, specs, and prices
•	Price Lists
o	Uploaded as CSV / Excel
o	Stored as structured data (single source of truth)
•	Images & Links
o	Images stored in object storage
o	Product links and image URLs stored in DB
o	All data linked using SKU
 CMS ensures clean, trusted, and governed data.

## 3️⃣ Embeddings Creation
•	Validated catalog text is split into chunks
•	Text is converted into embeddings using MiniLM
•	Embeddings are stored in MongoDB Vector Search with metadata:
o	SKU
o	Tenant ID
o	Source (PDF, page, link)
 This prepares data for semantic retrieval.

## 4️⃣ Ask a Live Question
Example user query:
“Which LED panels under ₹5,000 support outdoor use?”

## 5️⃣ RAG Flow (How the system answers)
•	User query → converted to embedding
•	MongoDB performs vector search
•	Relevant catalog chunks are retrieved
•	LLM receives:
o	User question
o	Retrieved catalog context
 LLM generates a grounded answer using only retrieved data.

## 6️⃣ Show Output
•	Final answer includes:
o	Product name
o	SKU
o	Price
o	Catalog / manufacturer link
 Explain:
•	Traceability (where the answer came from)
•	No hallucination (LLM doesn’t guess)

## 7️⃣ Close
•	System is:
o	Scalable
o	Secure
o	Multi-tenant
•	Supports:
o	Estimators (cost accuracy)
o	Designers (product discovery)

 
 ### Simple Data Flow (One Look Understanding)
Website / PDFs / CSVs
        ↓
CMS (Validated & Structured Data)
        ↓
Text → Embeddings
        ↓
MongoDB Vector Search
        ↓
RAG (Retrieve + Generate)
        ↓
Grounded Answer

 ### Tech Stack (What & Why)
## Data Storage
•	MongoDB Atlas
o	Structured product data (SKU, price, specs)
o	Vector Search for embeddings
o	Supports multi-tenant filtering
•	Object Storage (Local FS)
o	Stores PDFs and images
o	MongoDB stores references (URLs)

## Ingestion & Processing
•	OCR (Tesseract / Textract)
o	Extracts text from PDF catalogs
o	Human validation ensures correctness
•	CSV / Excel (Pandas)
o	Price list ingestion
o	Ensures data integrity

## Embeddings
•	Model: sentence-transformers/all-MiniLM-L6-v2
•	Why MiniLM
o	Fast and lightweight
o	Strong semantic understanding
o	Cost-efficient (384 dimensions)
o	Free & open-source
•	Purpose
o	Enables semantic search over catalog data

## RAG & Orchestration
•	LangChain
o	Chunking
o	History-aware query rewriting
o	Prompt orchestration
•	MongoDB Vector Search
o	Semantic retrieval with metadata filtering

## LLM (Answer Generation)
•	Groq (LLaMA-3)
o	Used only for answer generation
o	Fast inference
o	Keeps costs low
•	Purpose
o	Converts retrieved context into human-readable answers

## Security & Config
•	dotenv
o	Secure management of API keys
•	Tenant ID
o	Enforced during ingestion and retrieval for isolation

## Final flow which is implemented
catalog_data/
│
├── pdf_catalogs/              # Raw manufacturer PDFs
├── extracted_text/            # OCR output text
├── product_images/            # Extracted product images
├── structured_data/           # CSVs (prices, specs, links)
│
├── extract.py                 # OCR + image extraction
├── cms_ingestion_pipeline.py  # CMS validation & storage
├── embedding_pipeline.py      # Create embeddings
├── retrieval_pipeline.py      # Vector search
├── answer_generation.py       # LLM grounded answers
├── history_aware_generation.py# Conversational RAG
├── chat_rag_app.py            # Interactive terminal chat
