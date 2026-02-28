# Quick Start Guide

## Running the Application

### Option 1: Use the setup script

```bash
chmod +x setup.sh
./setup.sh
python app.py
```

### Option 2: Manual setup

```bash
# create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# install dependencies
pip install -r requirements.txt

# test the setup (optional)
python test_setup.py

# run the app
python app.py
```

### Option 3: If dependencies are already installed

```bash
python app.py
```

---

## Accessing the App

Once it starts, you'll see something like:

```
Running on local URL:  http://0.0.0.0:7860
```

Open **http://localhost:7860** in your browser.

---

## Quick Test

1. Upload a file (PDF, Word, Excel, or text)
2. Pick an output format (JSON is a good default)
3. Click Convert
4. Check the preview and download the result

---

## Troubleshooting

**"Module not found" error:**
```bash
pip install -r requirements.txt
```

**Port 7860 already in use:**
Either kill the process using that port, or change it in app.py:
```python
interface.launch(server_port=7861)
```

**PDF extraction not working:**
```bash
pip install --upgrade PyMuPDF
```

---

## Test Files

You can test with pretty much any file:
- PDF: invoices, reports, whatever
- Word: any .docx file
- Excel: any .xlsx spreadsheet
- Text: .txt or .csv files

There are also sample files in the `test_data/` folder.

---

## Notes

- Max file size: 50MB
- All processing happens locally, nothing gets sent to external servers
- Check the Documentation tab in the app for more details
