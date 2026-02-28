# Project Explanation

## For Professor Submission

---

## 1. What this project is

**Title**: Document to Dataset Converter

This is a tool that takes common document formats (PDF, Word, Excel, text files, CSV) and converts them into structured data formats (JSON, CSV, XML) that can be used for AI/ML training.

The main problem it solves: if you want to train a machine learning model, you need clean, structured data. But most real-world data sits in PDFs, Word documents, spreadsheets, etc. Getting that data out manually is slow and tedious. This tool automates that process.

It also includes a chatbot feature — after converting a document, you can ask questions about the data using natural language, powered by Groq's LLM API.

**What it does in practice:**
- Takes a messy PDF or Word doc as input
- Extracts the text, tables, and metadata
- Cleans up noise (page numbers, extra whitespace, URLs)
- Outputs clean structured data in your chosen format
- Lets you query the converted data through a chatbot

---

## 2. How it works — the pipeline

The system processes files in four stages:

### Stage 1: Validation
- Checks if the file type is supported
- Verifies the file isn't too large (50MB limit)
- Makes sure the file isn't empty or corrupted

### Stage 2: Extraction
- Picks the right parser based on file extension
- PDF: Uses PyMuPDF for text, pdfplumber for tables
- Word: Uses python-docx for paragraphs and tables
- Excel: Uses pandas to read all sheets
- Text/CSV: Reads directly with encoding detection

### Stage 3: Cleaning
- Removes page numbers, headers, footers
- Strips extra whitespace and line breaks
- Optionally removes URLs, email addresses
- Normalizes encoding to UTF-8

### Stage 4: Formatting and export
- Structures the data into chosen output format
- JSON: nested structure with metadata
- CSV: flat table format
- XML: hierarchical markup
- AI Training Format: includes text + metadata + features
- Saves the file and shows a preview

```
Upload -> Validate -> Extract -> Clean -> Format -> Download
```

---

## 3. Tech stack

### Language
**Python 3.8+** — standard choice for data processing and ML work.

### Libraries used

| Library | What it does |
|---------|-------------|
| Gradio | Web interface framework |
| PyMuPDF (fitz) | Extracts text from PDFs |
| pdfplumber | Extracts tables from PDFs |
| python-docx | Reads Word documents |
| pandas | Handles Excel data and tabular operations |
| openpyxl | Reads/writes XLSX files |
| chardet | Detects file encoding |
| Groq | LLM API for the chatbot feature |
| python-dotenv | Loads environment variables |

### Architecture

Object-oriented design. There's a base converter class, and each file type has its own converter that inherits from it. Utilities (cleaning, formatting, validation) are separate modules.

```
Gradio UI (app.py)
    |
    v
Application logic (AIDataConverter class)
    |
    v
Converters (pdf, word, excel, text)
    |
    v
Utilities (cleaner, formatter, validator)
```

Each converter implements two methods: `extract()` and `get_metadata()`. This makes it straightforward to add support for new file types later.

---

## 4. Where this could be used

### Legal / Finance
Law firms deal with thousands of contracts in PDF. This tool could convert them into structured data for training contract-analysis models.

### Healthcare
Medical records and research papers are usually unstructured. Converting them to structured formats enables training diagnostic or research AI.

### Customer support
Support tickets, chat logs, emails — all text-heavy, all unstructured. Converting them creates training data for chatbots and sentiment analysis.

### Research
Researchers analyzing hundreds of papers could extract and structure the content for systematic reviews or meta-analysis.

### General business
Any situation where data is trapped in documents and needs to be analyzed or used for ML training.

---

## 5. Output examples

### JSON output (from a PDF invoice)

```json
{
  "document_type": "PDF",
  "total_pages": 1,
  "full_text": "Invoice #12345\nDate: 2023-10-25\n...",
  "tables": [
    {
      "page": 1,
      "rows": 5,
      "columns": 4,
      "data": [
        ["Item", "Quantity", "Price", "Total"],
        ["Cloud Storage", "1", "50.00", "50.00"],
        ["API Access", "1", "100.00", "100.00"]
      ]
    }
  ],
  "metadata": {
    "author": "Company Inc.",
    "created": "2023-10-25"
  }
}
```

### AI Training Format

```json
{
  "input_text": "Invoice #12345 Date: October 25, 2023...",
  "metadata": {
    "document_type": "invoice",
    "page_count": 1,
    "word_count": 45
  },
  "features": {
    "has_tables": true,
    "word_count": 45
  },
  "structured_data": [...]
}
```

### CSV (tabular data)

| Invoice_Number | Date | Item | Price | Quantity | Total |
|----------------|------|------|-------|----------|-------|
| 12345 | 2023-10-25 | Cloud Storage | 50.00 | 1 | 50.00 |
| 12345 | 2023-10-25 | API Access | 100.00 | 1 | 100.00 |

---

## 6. Key features

1. **Multi-format support** — handles 7+ file types with one tool
2. **Table extraction** — automatically finds and preserves tables from PDFs and Word docs
3. **Batch processing** — upload multiple files, process all at once, download as ZIP
4. **Configurable cleaning** — user chooses what to clean (URLs, spaces, etc.)
5. **Multiple output formats** — JSON, CSV, XML, AI Training Format
6. **Data preview** — see what the extraction looks like before downloading
7. **Chatbot** — ask questions about your converted data using natural language

---

## 7. Comparison with alternatives

| | Manual process | Other tools | This tool |
|---|---|---|---|
| Speed | Hours per file | Minutes | Seconds |
| Batch support | Not practical | Limited | Yes |
| Table extraction | Manual copy-paste | Basic | Automatic |
| Format support | One at a time | 2-3 formats | 7+ formats |
| Output options | Manual formatting | 1-2 formats | 4 formats |
| Cleaning | Manual | Basic | Configurable |
| Cost | High (labor) | Subscription | Free |

---

## 8. Possible future improvements

1. OCR for scanned documents/images
2. Cloud storage integration (Google Drive, Dropbox)
3. REST API for programmatic access
4. Custom output templates
5. Auto-detection of document type
6. Support for more formats (PowerPoint, HTML)

---

## 9. Summary

This project addresses a practical problem in AI development: getting data out of documents and into a usable format. It automates extraction, cleaning, and formatting, and adds a chatbot for querying the results.

Technical highlights:
- Modular OOP architecture (easy to extend)
- Multiple parsing strategies per format (PyMuPDF + pdfplumber for PDFs)
- Configurable cleaning pipeline
- Web-based interface with Gradio
- LLM-powered chatbot for data querying

---

## Running the demo

```bash
pip install -r requirements.txt
python app.py
# go to http://localhost:7860
```

---

**Prepared by**: [Your Name]
**Date**: February 2026
**Course**: [Your Course]
**Professor**: [Professor's Name]