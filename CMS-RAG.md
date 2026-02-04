1. CORE SYSTEM ARCHITECTURE & DATA FLOW
The application relies on two primary engines connected by the central Catalogue Management System (CMS).
A. System Overview
The system must be designed around multi-tenancy to strictly segregate proprietary data (catalogs) between different dealers.
Component	Responsibility	Action Required by Developer
Input Layer	Accepts user photos and metadata (e.g., $20 bill, room type).	Design robust input processing logic for image and dimension extraction.
Computer Vision (CV) / AI Estimating Engine	Performs dimensional analysis (metrology), recognizes styles/fixtures, and generates the draft Bill of Materials (BOM).	Develop and integrate the core machine learning models for room analysis and product prediction.
Catalogue Management System (CMS)	Stores and manages all structured and unstructured product data (prices, specs, images, links).	Build the secure, scalable, multi-tenant database structure for catalog ingestion.
Human-in-the-Loop (HIL) Interface	The front-end interface where a human designer reviews, validates, and finalizes the AI's estimate.	Focus UX on speed, clarity, and ease of override (see Section 3).

2. CATALOGUE MANAGEMENT SYSTEM (CMS) REQUIREMENTS
The CMS must be designed to handle and process diverse, multi-modal data types to serve both the estimating AI (structured data) and the designer (unstructured data).
A. Unstructured Data Ingestion (PDFs, Images, Links)
Data Type	Developer Action Required (Functionality)
PDF Catalogues	Implement a Data Extraction Pipeline capable of ingesting PDF files. This pipeline must feature Optical Character Recognition (OCR) capabilities to convert text (SKUs, dimensions, prices) into structured database records. Note: A human-assisted validation layer for OCR output is crucial.
Images	Build storage and indexing for high-resolution product photos (linked by SKU). Action: Ensure images are accessible by the CV Training Pipeline for model refinement and are displayed in the final customer report.
Online Links	Create database fields to store direct URLs (links to manufacturer pages, specs, installation guides) associated with each SKU. These must be included in the final design package output.
B. Structured Data Management
●	Price List Integration: Develop APIs to accept and process raw price list files (CSV, Excel) and load them as the single source of truth for cost calculation.
●	Data Integrity: Implement checksums and validation rules to ensure price data remains synchronized and uncorrupted.

