# Learning Guide

This doc walks through the concepts used in the project so you actually understand what's going on, not just how to run it.

---

## Part 1: Core Python Concepts

### Object-Oriented Programming (OOP)

OOP is basically organizing your code into classes (blueprints) and objects (instances of those blueprints). Instead of having a bunch of loose functions floating around, you group related data and behavior together.

```python
class Converter:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract(self):
        # each subclass handles this differently
        pass
```

In our project, every converter is a class. PDFConverter, WordConverter, etc. They all share a common parent class.

### Inheritance

Inheritance lets you create a base class with shared functionality, then have child classes that build on top of it.

```python
class BaseConverter(ABC):
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)

    @abstractmethod
    def extract(self):
        pass

class PDFConverter(BaseConverter):
    def extract(self):
        # PDF-specific extraction logic
        doc = fitz.open(self.file_path)
        # ...
```

The `@abstractmethod` decorator means child classes MUST implement that method. If you forget, Python throws an error. This is how we enforce consistency — every converter has an `extract()` method with the same interface.

### Type Hints

Python doesn't require you to declare types, but type hints make code way easier to read:

```python
def process_file(file_path: str, output_format: str) -> Tuple[str, str]:
    # now anyone reading this knows what goes in and comes out
```

We use these throughout the project. They don't actually enforce anything at runtime — they're just documentation that your IDE can use for autocomplete and error checking.

### Dictionaries

Dicts are the main data structure we pass around. Extracted data, metadata, options — it's all dicts.

```python
extracted = {
    "document_type": "PDF",
    "total_pages": 5,
    "full_text": "...",
    "tables": [...],
    "metadata": {...}
}

# safe access with defaults
value = options.get('remove_urls', True)
```

The `.get()` method is used everywhere because it returns a default instead of crashing when a key doesn't exist.

---

## Part 2: Libraries Used

### Gradio

Gradio handles the web interface. You define input/output components and wire them to Python functions.

```python
import gradio as gr

with gr.Blocks() as demo:
    file_input = gr.File(label="Upload")
    btn = gr.Button("Convert")
    output = gr.Textbox(label="Result")

    btn.click(fn=process, inputs=[file_input], outputs=[output])

demo.launch()
```

It takes care of all the HTML/JS/CSS — you just think in terms of components and callbacks.

### PyMuPDF (fitz)

This is the main PDF library. Despite the import name being `fitz`, you install it as `PyMuPDF`.

```python
import fitz

doc = fitz.open("file.pdf")
for page in doc:
    text = page.get_text()
```

It's fast and handles most PDFs well. We use it for general text extraction.

### pdfplumber

pdfplumber is specifically good at extracting tables from PDFs. Regular PDF readers just see positioned text — pdfplumber uses algorithms to figure out which text blocks are aligned into rows and columns.

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    page = pdf.pages[0]
    tables = page.extract_tables()
```

We use both PyMuPDF and pdfplumber because they're good at different things.

### python-docx

Handles Word documents. Gives you access to paragraphs, tables, and styling info.

```python
from docx import Document

doc = Document("file.docx")
for para in doc.paragraphs:
    print(para.text)
```

### pandas

pandas is the go-to library for tabular data. We use it for Excel and CSV files.

```python
import pandas as pd

df = pd.read_excel("file.xlsx")
data = df.to_dict('records')  # list of dicts, one per row
```

It handles all the messy stuff like multiple sheets, data types, missing values, etc.

### regex (re module)

Regular expressions are used in the cleaner to find and remove patterns like URLs, emails, extra whitespace.

```python
import re

# remove URLs
text = re.sub(r'http[s]?://\S+', '', text)

# collapse multiple spaces into one
text = re.sub(r'\s+', ' ', text)
```

---

## Part 3: Project Structure

Here's how the files are organized:

```
kavproj1/
    app.py                  # main application, runs the UI
    chatbot.py              # Groq API chatbot for querying data
    requirements.txt        # pip dependencies
    .env                    # API keys
    
    converters/
        __init__.py
        base_converter.py   # abstract parent class
        pdf_converter.py    # PDF handling
        word_converter.py   # Word handling
        excel_converter.py  # Excel handling
        text_converter.py   # plain text / CSV handling
    
    utils/
        __init__.py
        cleaner.py          # text cleaning functions
        formatter.py        # output format conversion
        validator.py        # file validation
    
    output/                 # converted files go here
    test_data/              # sample files for testing
```

The separation is intentional: converters deal with reading files, utils deal with processing and formatting, and app.py ties everything together with the UI.

---

## Part 4: How a File Gets Processed

Here's what happens when someone uploads a PDF and clicks convert:

**Step 1 — Validation**

```python
is_valid, message = self.validator.validate_file(file_path)
# checks: does the file exist? is it a supported format? is it under 50MB?
```

**Step 2 — Pick the right converter**

```python
ext = os.path.splitext(file_path)[1].lower()
if ext == '.pdf':
    converter = PDFConverter(file_path)
elif ext == '.docx':
    converter = WordConverter(file_path)
# ... etc
```

This is basically a factory pattern — we decide which class to use based on the file extension.

**Step 3 — Extract data**

```python
extracted_data = converter.extract()
# returns a dict with text content, tables, metadata, page info
```

**Step 4 — Clean text**

```python
if cleaning_enabled:
    cleaned = self.cleaner.clean_text(text, cleaning_options)
    # removes URLs, extra whitespace, special characters, etc.
```

**Step 5 — Format output**

```python
if output_format == "JSON":
    result = self.formatter.to_json(extracted_data)
elif output_format == "CSV":
    result = self.formatter.to_csv(extracted_data, output_path)
```

**Step 6 — Return to the user**

The formatted data gets saved to the output folder, and the user gets a preview plus a download link.

---

## Part 5: Key Components Explained

### Base Converter

```python
class BaseConverter(ABC):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.file_size = os.path.getsize(file_path)

    @abstractmethod
    def extract(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        pass
```

ABC stands for Abstract Base Class. You can't create a `BaseConverter` object directly — you have to subclass it. The abstract methods force every child to implement `extract()` and `get_metadata()`. This way all converters have the same interface.

### PDF Converter

```python
class PDFConverter(BaseConverter):
    def extract(self) -> Dict[str, Any]:
        try:
            self.doc = fitz.open(self.file_path)
            pages_data = []
            full_text = []

            for page_num in range(len(self.doc)):
                page = self.doc[page_num]
                text = page.get_text()
                page_data = {
                    "page_number": page_num + 1,
                    "text": text,
                    "word_count": len(text.split())
                }
                pages_data.append(page_data)
                full_text.append(text)

            tables = self._extract_tables()

            return {
                "document_type": "PDF",
                "total_pages": len(self.doc),
                "full_text": "\n\n".join(full_text),
                "pages": pages_data,
                "tables": tables,
                "metadata": self.get_metadata()
            }
        except Exception as e:
            return {"error": f"Failed: {str(e)}"}
```

The try-except wrapper is important because PDFs can be corrupted or password-protected. Instead of crashing, we return a dict with an error key that gets handled gracefully upstream.

### Data Cleaner

```python
class DataCleaner:
    @staticmethod
    def clean_text(text: str, options: Dict[str, bool]) -> str:
        cleaned_text = text

        if options.get('remove_urls', True):
            cleaned_text = re.sub(
                r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+])+',
                '', cleaned_text
            )

        if options.get('remove_extra_spaces', True):
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
            cleaned_text = cleaned_text.strip()

        return cleaned_text
```

`@staticmethod` means you don't need an instance — you call it like `DataCleaner.clean_text(...)`. Makes sense here since the cleaner doesn't hold any state.

### Data Formatter

```python
class DataFormatter:
    @staticmethod
    def to_json(data: Dict[str, Any], pretty: bool = True) -> str:
        if pretty:
            return json.dumps(data, indent=2, ensure_ascii=False)
        return json.dumps(data, ensure_ascii=False)

    @staticmethod
    def to_csv(data: List[Dict], output_path: str) -> str:
        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = list(data[0].keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        return output_path
```

`json.dumps()` converts a Python dict to a JSON string. `indent=2` makes it readable. `csv.DictWriter` takes a list of dicts and writes them as rows in a CSV.

---

## Part 6: Other Concepts Worth Knowing

### Context Managers (the `with` statement)

```python
# without context manager — risky if an error happens mid-read
file = open("data.txt", 'r')
content = file.read()
file.close()

# with context manager — file always closes, even on errors
with open("data.txt", 'r') as file:
    content = file.read()
```

We use this pattern everywhere: opening PDFs, writing output files, etc. It's just cleaner and safer.

### List Comprehensions

```python
# regular loop
words = []
for page in pages:
    words.append(len(page.text.split()))

# same thing, one line
words = [len(page.text.split()) for page in pages]
```

### F-strings

```python
name = "invoice"
output_path = f"{name}_converted.json"
# result: "invoice_converted.json"
```

Way more readable than string concatenation or `.format()`.

### Try-Except

```python
try:
    data = converter.extract()
except FileNotFoundError:
    print("File not found")
except Exception as e:
    print(f"Something went wrong: {e}")
```

We wrap most extraction calls in try-except because we're dealing with user-uploaded files and you never know what you'll get.

---

## Part 7: Design Patterns

A few patterns show up in this project:

### Factory Pattern

When we pick the right converter based on file extension — that's a factory. The caller doesn't need to know which specific class gets created.

```python
def get_converter(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return PDFConverter(file_path)
    elif ext == '.docx':
        return WordConverter(file_path)
```

### Strategy Pattern

The cleaning options work like strategies. You pass in a dict of flags, and the cleaner applies different processing steps based on what's enabled.

```python
options = {
    'remove_urls': True,
    'lowercase': False,
    'remove_numbers': False
}
cleaned = cleaner.clean_text(text, options)
```

### Template Method

The base converter defines the overall structure (extract, get_metadata), and each child fills in the specifics. That's the template method pattern.

---

## Part 8: Debugging Tips

Some stuff that helps when things break:

```python
# check what type something is
print(type(data))

# see what's inside a dict
print(data.keys())

# check if a key exists before accessing it
if "error" in extracted_data:
    # handle the error case
    pass

# safe dictionary access
value = config.get("key", "default_value")
```

The most common issues:
- Wrong file type uploaded (validator catches this)
- Corrupted PDF (try-except catches this)
- Missing dependencies (requirements.txt handles this)

---

## How to Talk About This Project

If someone asks you about it, here's a natural way to explain:

**"What did you build?"**
"It's a tool that takes documents like PDFs and Word files and converts them into structured data formats — JSON, CSV, XML — so the data is actually usable for things like machine learning or analysis."

**"How does it work?"**
"You upload a file through a web interface, it figures out what type of file it is, uses the right library to pull out the text and tables, cleans it up, and converts it to whatever format you need."

**"What was hard about it?"**
"Extracting tables from PDFs. PDFs don't actually store table structure — it's just text placed at specific coordinates. I used pdfplumber which has algorithms to detect alignment and reconstruct the table layout."

**"What would you change?"**
"For something bigger, I'd add async processing so multiple files can be handled at once, maybe a database to track conversions, and probably Docker for deployment."

---

That covers pretty much everything in the codebase. If something doesn't make sense, look at the actual source files — the code is commented and fairly readable.
