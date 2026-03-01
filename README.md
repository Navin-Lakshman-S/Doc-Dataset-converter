# Document to Dataset Converter

Converts PDFs, Word docs, Excel sheets, text files, and CSVs into structured data (JSON, CSV, XML) you can use for AI training or analysis. Also has a chatbot so you can ask questions about your converted data.

---

## Why I built this

Getting data out of documents manually is painful. You open a PDF, copy text, paste it somewhere, clean it up, repeat. If you have 50 files to process, that's hours of work. This tool does all of that in a few seconds.

---

## What it supports

**Input formats:** PDF, DOCX, XLSX, XLS, TXT, CSV

**Output formats:** JSON, CSV, XML, AI Training Format

**Other stuff:**
- Extracts tables from PDFs and Word docs automatically
- Cleans up junk like page numbers, headers, extra whitespace
- Batch processing (upload multiple files, get a ZIP back)
- Preview your data before downloading
- Chat with your converted data using Groq AI

---

## Setup

You need Python 3.8+ installed.

```bash
# clone the repo
git clone <your-repo-url>
cd Doc-Dataset-converter

# create a virtual environment
python3 -m venv venv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run it
python app.py
```

Opens at `http://localhost:7860`

If you want to use the chatbot feature, add your Groq API key to a `.env` file:
```
GROQ_API_KEY=your_key_here
```

---

## How to use

### Single file
1. Go to "Single File Converter" tab
2. Upload your file
3. Pick an output format
4. Click "Convert to Dataset"
5. Download the result

### Batch processing
1. Go to "Batch Converter" tab
2. Upload multiple files
3. Same deal — pick format, click process
4. Download the ZIP

### Chatbot
1. Convert a file first
2. Go to "Chat with Data" tab
3. Ask questions like "what's the total?" or "summarize this"

---

## Project structure

```
Doc-Dataset-converter/
├── app.py                  # main app (Gradio UI + logic)
├── chatbot.py              # chatbot using Groq API
├── requirements.txt        # dependencies
├── .env                    # API key (not committed)
│
├── converters/             # one converter per file type
│   ├── base_converter.py   # abstract base class
│   ├── pdf_converter.py    # PDF extraction (PyMuPDF + pdfplumber)
│   ├── word_converter.py   # DOCX extraction (python-docx)
│   ├── excel_converter.py  # Excel extraction (pandas)
│   └── text_converter.py   # TXT/CSV extraction
│
├── utils/                  # helper modules
│   ├── cleaner.py          # text cleaning (regex-based)
│   ├── formatter.py        # output formatting (JSON/CSV/XML)
│   └── validator.py        # file validation (type, size)
│
├── test_data/              # sample files for testing
└── output/                 # where converted files go
```

---

## Tech stack

| What | Library | Why |
|------|---------|-----|
| Language | Python 3.8+ | Main language |
| UI | Gradio | Quick web interface |
| PDF parsing | PyMuPDF, pdfplumber | Text + table extraction |
| Word parsing | python-docx | DOCX files |
| Excel parsing | pandas, openpyxl | Spreadsheets |
| Text cleaning | regex | Pattern matching |
| Chatbot | Groq API (llama-3.3-70b) | Querying converted data |
| Encoding detection | chardet | Handle different encodings |

---

## How it works internally

```
Upload file → Validate (type, size) → Extract content → Clean text → Format output → Save file
```

1. **Validation** — checks if the file type is supported and under 50MB
2. **Extraction** — picks the right converter based on file extension, pulls out text + tables + metadata
3. **Cleaning** — optional step, removes URLs, extra spaces, page numbers, etc.
4. **Formatting** — converts the extracted data into your chosen format
5. **Output** — saves the file and shows a preview

The converters all inherit from `BaseConverter`, which defines the interface (`extract()` and `get_metadata()`). Each file type has its own implementation.

---

## Example output

**Input:** A PDF invoice

**JSON output:**
```json
{
  "document_type": "PDF",
  "total_pages": 2,
  "full_text": "Invoice #12345\nDate: 2024-01-15\n...",
  "tables": [
    {
      "page": 1,
      "rows": 5,
      "columns": 4,
      "data": [
        ["Item", "Quantity", "Price", "Total"],
        ["Cloud Storage", "1", "50.00", "50.00"]
      ]
    }
  ],
  "metadata": {
    "author": "Company Inc.",
    "created": "2024-01-15"
  }
}
```

---

## Limitations

- Password-protected files won't work
- Max file size is 50MB
- Complex PDF layouts might not extract perfectly
- Chatbot context is limited to first 4000 chars of converted data
- Very large Excel files might be slow

---

## License

MIT
