AI Estimation & Catalogue Intelligence System
Core Architecture & CMS Requirements

This document defines the system architecture, data flow, and Catalogue Management System (CMS) requirements for a multi-tenant AI-powered estimation platform.

1.Core System Architecture & Data Flow

The application is built around two primary AI engines connected through a centralized Catalogue Management System (CMS).

A. System Overview

The entire platform must follow a multi-tenant architecture to ensure strict data isolation between different dealers and their proprietary catalogs.

Component	Responsibility	Action Required by Developer
Input Layer	Accepts user photos and metadata (e.g., $20 bill for scale, room type).	Design robust input processing logic for image normalization, metadata capture, and dimension reference detection.
Computer Vision (CV) / AI Estimating Engine	Performs room measurement (metrology), recognizes styles and fixtures, and generates a draft Bill of Materials (BOM).	Develop and integrate ML models for room analysis, object detection, and product prediction.
Catalogue Management System (CMS)	Stores and manages all product data (structured + unstructured).	Build a secure, scalable, multi-tenant database for catalog ingestion and querying.
Human-in-the-Loop (HIL) Interface	Allows designers to review, validate, and finalize AI-generated estimates.	Focus UX on speed, clarity, and easy override/editing of AI outputs.

2. Catalogue Management System (CMS) Requirements

The CMS must support multi-modal data ingestion to power both:
The AI Estimating Engine (structured data)
The Designer Interface (visual and reference data)
A. Unstructured Data Ingestion

The system must process and structure raw manufacturer materials.
Data Type	Developer Functionality Required
PDF Catalogues	Build a Data Extraction Pipeline with OCR to convert SKUs, dimensions, and prices into structured database records. Include a human validation layer to correct OCR errors.
Images	Implement storage and indexing for high-resolution product images linked by SKU. Images must be accessible to:
• The CV training pipeline
• The final customer design report
Online Links	Add database fields for manufacturer URLs, spec sheets, and installation guides linked to each SKU. These must be included in the final design package output.
B. Structured Data Management

Structured data powers cost accuracy and AI product matching.

🔹 Price List Integration

Develop APIs to ingest CSV/Excel price lists

These files become the single source of truth for all cost calculations

Support dealer-specific pricing tiers (multi-tenant support)

🔹 Data Integrity

Implement safeguards to maintain pricing reliability:

Checksums for file validation

Schema validation before database insertion

Version tracking for price updates

Sync validation to prevent corruption or mismatch

🏗️ Architectural Principles

Multi-Tenant by Design — Complete data segregation between dealers

AI + Human Collaboration — AI generates, humans validate

Structured + Unstructured Fusion — Supports both machine reasoning and human review

Scalable CMS Core — Future-proof for additional brands and catalogs

🚀 Outcome

This system transforms raw product catalogs and room images into:

✅ Accurate AI-generated Bills of Materials
✅ Designer-reviewed professional estimates
✅ Rich final reports with images, specs, and product links

<img width="996" height="588" alt="image" src="https://github.com/user-attachments/assets/fb05551b-bb7a-4ecd-9947-c1657c64ead1" />
