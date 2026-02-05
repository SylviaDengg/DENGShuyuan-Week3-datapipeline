# DENGShuyuan-Week3-datapipeline

This repository contains a simple data cleaning and validation pipeline developed for an introductory course on data structuring and AI-assisted (“vibe”) coding.

The pipeline processes a small dataset of New York Times articles, applies rule-based cleaning and validation, and produces cleaned outputs along with a data quality report.

---

## Repository Structure

- `cleaner.py`  
  Data cleaning functions (text normalization, HTML artifact removal, edge-case handling)

- `validator.py`  
  Data validation functions (required fields, URL format, content length checks)

- `sample_input_data.json`  
  Sample input dataset (NYT articles scraped during lecture)

- `cleaned_output.json`  
  Cleaned and validated output dataset

- `quality_report.txt`  
  Summary report describing data quality and validation results

- `prompt-log.md`  
  Log of AI-assisted prompts used during development

---

## Data Cleaning

Data cleaning is implemented in `cleaner.py` and includes:

- Removal of extra whitespace and HTML tags
- Decoding of HTML entities (e.g. `&amp;`, `&quot;`)
- Unicode text normalization
- Removal of known New York Times access and paywall boilerplate text
- Record-level cleaning while preserving the original dataset structure

These steps address common issues in scraped web article text.

---

## Data Validation

Data validation is implemented in `validator.py` and includes:

- Required field checks for `title`, `content`, and `url`
- URL format validation (HTTP/HTTPS only)
- Minimum content length checks
- Clear and consistent validation error messages

Invalid records are flagged with explicit reasons rather than being removed.

---
## Running the Pipeline

To run the full pipeline, a run_pipeline.py is created but not included in this repository that

- Read sample_input_data.json
- Clean all article records
- Validate each record
- Generate:
  - cleaned_output.json
  - quality_report.txt

---
## Author: DENG Shuyuan Sylvia
