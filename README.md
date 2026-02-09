### Catalogue Intelligence System with RAG

An end-to-end Catalogue Management System (CMS) + Retrieval-Augmented Generation (RAG) pipeline that turns raw product catalogs into an intelligent, searchable knowledge system.

This system helps estimators, designers, and engineers quickly find accurate, grounded product information from PDFs, specs, and price lists — without hallucinations.

## What This Project Does

It converts messy catalog data into a structured AI-searchable system:

PDFs / CSVs / Images
        ↓
CMS (Validated Structured Data)
        ↓
Text → Embeddings
        ↓
MongoDB Vector Search
        ↓
RAG (Retrieve + Generate)
        ↓
Grounded Answers with Page References

### System Architecture
## 1️⃣ Data Sources

 PDF product catalogs (scanned + digital)

 Product images

 Specifications (CSV)

 Price lists (CSV)

## 2️⃣ CMS Layer (Catalogue Management System)

Responsible for data validation and structuring before AI usage.

Input	Processing	Output
PDF catalogs	Hybrid text extraction (Native + OCR)	Page-structured product descriptions
CSV price lists	Structured ingestion	SKU → Price
Specs CSV	Structured ingestion	SKU → Technical specs
Images	Extracted & renamed	Linked by SKU or page

✔ Page numbers are preserved
✔ Images intelligently matched
✔ Human validation logic ensures SKU accuracy

## 3️ Text Extraction (Improved)

The system uses a Hybrid Extraction Strategy:

Page Type	Method
Digital text PDF	Native extraction (PyMuPDF)
Scanned/image PDF	EasyOCR deep learning OCR

This avoids OCR errors when text is already embedded and improves accuracy for scanned catalogs.

## 4️⃣ Embedding Layer

Validated product text is:

Split into semantic chunks

Assigned correct page numbers

Given unique chunk IDs (no overwriting)

Converted into embeddings using MiniLM

Stored in MongoDB Atlas Vector Search

## 5️⃣ Retrieval (RAG)

When a user asks a question:

Query → embedding

MongoDB vector search retrieves relevant chunks

Correct catalog page numbers are preserved

Context sent to LLM

LLM generates grounded answer with sources

## 6️⃣ Answer Generation

The LLM:

Uses only retrieved catalog data

Avoids hallucinations

Provides traceable product info

Supports fuzzy model number matching

Handles imperfect OCR model numbers

###  Tech Stack
## Data Storage

MongoDB Atlas

Structured product data

Vector search for embeddings

Local File Storage

PDFs

Extracted product images

## Ingestion & Processing
Tool	Purpose
PyMuPDF	Native PDF text extraction + images
pdf2image + Poppler	Convert scanned pages to images
EasyOCR	Deep learning OCR for scanned catalogs
Pandas	CSV ingestion

##  Embeddings

Model: sentence-transformers/all-MiniLM-L6-v2

384-dimensional vectors

Fast, lightweight, ideal for product search

## RAG & LLM
Tool	Purpose
LangChain	Orchestration & prompting
MongoDB Vector Search	Semantic retrieval
Groq (LLaMA 3)	Grounded answer generation

## Security & Config

.env for API keys

Environment-based configuration

No hardcoded secrets

##  Project Structure
catalog_data/
│
├── pdf_catalogs/              # Raw manufacturer PDFs
├── extracted_text/            # Page-wise extracted text
├── product_images/            # Extracted product images
├── structured_data/           # CSVs (prices, specs)
│
├── extract.py                 # Hybrid text + image extraction
├── cms_ingestion_pipeline.py  # CMS validation & storage
├── embedding_pipeline.py      # Chunking + embeddings
├── retrieval_pipeline.py      # Vector search
├── answer_generation.py       # LLM grounded answers
├── chat_rag_app.py            # Interactive chat UI

###  Setup Instructions
## 1️⃣ Create Virtual Environment
python -m venv venv

## 2️⃣ Activate
venv\Scripts\activate

## 3️⃣ Upgrade pip
python -m pip install --upgrade pip

## 4️⃣ Install Dependencies
pip install -r requirements.txt

## System Dependencies
Tool	Required For
Poppler	PDF → image conversion
Tesseract (optional)	Legacy OCR fallback (not primary)

## Serve PDFs for Page Jumping

To allow links like “Open Catalog” to open the exact page:

cd catalog_data/pdf_catalogs
python -m http.server 9000


The app links to:

http://localhost:9000/catalog.pdf#page=12

## Environment Variables

Create .env file:

MONGODB_URI=your_mongodb_connection_string
GROQ_API_KEY=your_groq_api_key

## ▶️ Running the Pipelines
Step 1 — Extract Data from PDFs
python extract.py

Step 2 — CMS Structured Ingestion
python cms_ingestion_pipeline.py

Step 3 — Generate Embeddings
python embedding_pipeline.py

Step 4 — Ask Questions
python chat_rag_app.py

### Key Features

✔ Hybrid OCR for scanned + digital catalogs
✔ Accurate page tracking per chunk
✔ PDF links that open at exact source page
✔ Image-to-product linking
✔ Fuzzy model number understanding
✔ Grounded answers with citations

## Outcome

You now have a production-style Catalog Intelligence System that:

Understands messy real-world catalogs

Extracts structured product knowledge

Provides accurate, traceable AI answers

Avoids hallucinations

### Questions: 
## phillips-cat.pdf
**LED Bulbs & Lamps**
What is the lumen output of Philips Ace Saver 7W LED lamp?
What is the life hours of Stellar Bright High Wattage LED bulbs?
Which base types are available for Ace Saver bulbs?
What is the MRP of the Stellar Bright 2-in-1 LED lamp?
How many lumens does the Mini Tubelight 10W bulb produce?
What is the color temperature of the DecoRing 10W bulb?
**LED Battens & Tubelights**
What is the lumen output of the Slimline NEXT 20W batten?
What voltage protection range is supported by Astra Line battens?
What are the lighting modes available in Astra Line Scene Switch?
What is the MRP of the Linea Plus 23W LED batten?
How many lumens does the Stellar Bright TLED 20W tube provide?
What is the life span of the Stellar Bright TLED?
**Downlights & Panels**
What surge protection is provided in Astra Max Metal Panels?
What are the dimming modes in Astra Prime Scene Switch Downlighter?
What is the life class of Ultraslim+ panel lights?
How many lumens does the GreenLED Plus 12.5W downlight produce?
**Wall, Desk & Decorative Lights**
What is the lumen output of the Coral LED Wall Light 10W?
What features does the Ultron LED Wall Light have?
What is the MRP of the Cap LED Desklight?
What battery backup time is provided by Ujjwal Plus Emergency Light?
**Outdoor Lights**
What is the wattage and efficacy of the Smart Bright Street Light 35W?
What IP rating does the Smart Bright Flood Light have?
What is the lumen per watt efficacy of the Greenline Street Light?
What is the MRP of the Essential SmartBright 20W Floodlight?
**Switches & Electrical**
What are the features of Smart+ modular switches?
What current ratings are available in Philips MCBs?
What protection range is available in Philips RCCB?
What is the MRP of the 3-pin Philips Plug Top 16A?

## legrandcat.pdf:
**Switches (Classic White)**
What is the MRP of the Legrand 6A 1 way switch 1M White (Cat.No 6792 00)?
What is the price of the 16A Switch 1 way 1M White?
What is the MRP of the 20A DP Switch 2M White with indicator?
How much does the 32A DP Switch 2M with indicator White cost?
What is the pack size of the 10A intermediate switch 2M White?
**Push Buttons & Bell Push**
What is the MRP of the 6A bell push 1 way 1M White?
How much does the 6A push button with indicator White cost?
What is the price of the 6A bell push 2M with indicator White?
**Sockets**
What is the MRP of the 6/16A 2 Pin Euro US Socket 1M White?
What is the price of the 16A 3 Pin Switched Socket 3M White?
What is the MRP of the Multistandard Socket 2M White?
How much does the 25A Socket 2M White cost?
**Dimmers & Fan Regulators**
What is the MRP of the Rotary Dimmer 400W 1M White?
How much does the Fan Regulator 100W 1M White cost?
What is the price of the Fan Regulator 120W 2M White?
**Hospitality & Sensors**
What is the MRP of the Infrared Sensor Switch 400W 2M White?
What is the price of the Hotel Key FOB Switch 16A 2M White?
How much does the Bell Call Indicator 1M White cost?
What is the MRP of the Buzzer 230V 1M White?
**Data, TV & AV**
What is the price of the RJ45 UTP Cat6 tool-less socket 1M White?
What is the MRP of the TV Co-axial Socket White?
How much does the Preterminated HDMI Socket 1M White cost?
**USB & Charging**
What is the MRP of the Volume Controller 2M White?
What is the price of the Ceiling Loudspeaker 8 Ohms 100mm White?
How much does the Bluetooth Sound Diffusion 2M White cost?
**Audio & Smart Controls**
What is the MRP of the 6A Switch 1 way 1M Charcoal Grey?
What is the price of the 16A 3 Pin Switched Socket 3M Charcoal Grey?
How much does the 6A Bell Push 1M with indicator Charcoal Grey cost?
**Charcoal Grey Range**
What is the MRP of the 6A Switch 1 way 1M Charcoal Grey?
What is the price of the 16A 3 Pin Switched Socket 3M Charcoal Grey?
How much does the 6A Bell Push 1M with indicator Charcoal Grey cost?

## legrand questions

 **General Product Discovery (Legrand)**
These are perfect for homeowners, electricians, and architects.
“Show me all 16A switches available in Legrand Myrius.
“Which Legrand switches come with indicator lights?”
“Do you have bell push switches in the Myrius range?”
“List all fan regulators from Legrand with wattage details.”
“Which Legrand products are suitable for AC or geyser control?” legrand-catalog
“Show all socket types available in Legrand (universal, Euro, multistandard).”
“Do you have shaver sockets in Legrand? What voltage do they support?” legrand-catalog
**Design & Aesthetics (Big for Architects / Interior Designers)**
Legrand Myrius is heavily design-focused.
“What color finishes are available in Legrand Myrius plates?
“Show Legrand switches in Charcoal Grey finish.”
“Do you have black finish plates in Legrand?”
“What are the premium designer plate options in Myrius NextGen?”
“Compare White vs Charcoal Grey devices in Legrand.”
“Which Legrand plates are available in Pearl / Champagne / Sonic Silver shades?” legrand-catalog
**Smart / Connected Home Questions**
Myrius NextGen includes connected devices.
“Does Legrand have smart switches that work with app control?”
“Show me connected light switches from Legrand.”
“Do you have Wi-Fi or gateway-based smart home devices in Myrius?” legrand-catalog
“Which Legrand products support remote control of curtains or blinds?” legrand-catalog
“Are there wireless scene switches like Home/Away modes?” legrand-catalog
“Show me Legrand devices for voice or app-based control.”
**Hospitality (Hotels, Resorts, Service Apartments)**
Legrand has a strong hospitality section.
“Do you have hotel key card switches in Legrand?” legrand-catalog
“Show DND (Do Not Disturb) and MMR switches for hotel rooms.” legrand-catalog
“Which Legrand products are designed for hotel room automation?”
“Do you have bell call indicators or buzzers for hospitality use?” legrand-catalog
“Show all hospitality function modules from Legrand.”
**Health & Safety (Anti-Bacterial Range)**
Very unique selling point.
“Do you have anti-bacterial switches or plates in Legrand?” legrand-catalog
“Which Legrand products are designed for hygienic or hospital use?”
“Show anti-bacterial plate frames from Legrand.”
“What is special about Legrand anti-bacterial range?”
**Technical & Electrical Filtering**
Great for electricians and contractors.
“List all 32A switches from Legrand.”
“Show 20A DP switches with indicator.”
“Which Legrand sockets support 6/16A appliances?”
“Do you have USB charging sockets in Legrand?” legrand-catalog
“Show motor starters in Legrand wiring devices.” legrand-catalog
“Which dimmers support LED loads?”
**Price & SKU Based Questions**
Perfect for procurement teams.
“What is the price of Legrand Cat No 6792 53?” legrand-catalog
“Show all Legrand products under ₹500.”
“Compare prices of 16A switches across Legrand models.”
“What is the MRP of Legrand hotel key FOB switch?” legrand-catalog
“Give me SKU, description and price for all fan regulators.”
**Combo Questions**
These feel intelligent and useful:
“Suggest Legrand products needed for a hotel room electrical setup.”
“What Legrand devices do I need for a smart bedroom with dimming and curtain control?” legrand-catalog
“Recommend Legrand switches and sockets for a premium modern living room.”
“Build a Legrand bill of materials for a 2BHK home (basic, non-smart).”
“What Legrand options are there for elderly-friendly or night navigation lighting (like skirting lights)?” 
**Combine With Philips (Cross-Brand Power)**
“Suggest Legrand switches + Philips lights for a smart living room.”
“Best Philips LED panels + Legrand dimmers combination?”
“Give a full electrical material list using Philips lighting and Legrand wiring devices for a 3BHK home.”
“Which Legrand dimmers are compatible with LED lighting setups?”

