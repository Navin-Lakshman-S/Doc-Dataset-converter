# Quick Cheat Sheet

## What Each File Does

```
app.py              - main app, coordinates everything
pdf_converter.py    - reads PDFs, gets text and tables
word_converter.py   - reads Word docs
excel_converter.py  - reads Excel sheets
text_converter.py   - reads plain text / CSV files
cleaner.py          - removes junk from text
formatter.py        - converts to JSON/CSV/XML
validator.py        - checks if file is valid before processing
```

## Processing Flow

```
File Upload -> Validate -> Pick Converter -> Extract -> Clean -> Format -> Download
```

## Key Python Concepts

### Classes and Objects
```python
class Dog:
    def __init__(self, name):
        self.name = name
    def bark(self):
        print(f"{self.name} says woof!")

my_dog = Dog("Buddy")
my_dog.bark()  # "Buddy says woof!"
```

### Inheritance
```python
class Animal:           # Parent
    def eat(self):
        print("Eating...")

class Dog(Animal):      # Child inherits eat()
    def bark(self):
        print("Woof!")
```

### Dictionaries
```python
person = {"name": "John", "age": 25, "city": "NYC"}
print(person["name"])                   # "John"
print(person.get("job", "Unknown"))     # "Unknown" (safe default)
```

### List Comprehension
```python
# long way
squares = []
for x in range(10):
    squares.append(x**2)

# short way
squares = [x**2 for x in range(10)]
```

### Try-Except
```python
try:
    risky_operation()
except Exception as e:
    print(f"Oops: {e}")
```

## Library Quick Reference

```python
# Gradio - web UI
import gradio as gr
button = gr.Button("Click me")

# PyMuPDF - read PDFs
import fitz
doc = fitz.open("file.pdf")
text = doc[0].get_text()

# python-docx - read Word files
from docx import Document
doc = Document("file.docx")
text = doc.paragraphs[0].text

# pandas - read Excel/CSV
import pandas as pd
df = pd.read_excel("file.xlsx")
df = pd.read_csv("file.csv")

# regex - text cleaning
import re
clean = re.sub(r'http\S+', '', text)  # remove URLs
```

## Common Regex Patterns

```python
r'\d+'              # numbers
r'\s+'              # whitespace
r'http[s]?://\S+'   # URLs
r'\S+@\S+'          # emails
r'[^a-zA-Z0-9\s]'   # special characters
```

## Debugging

```python
print(type(data))           # check type
print(data)                 # see contents
print(dir(data))            # list all methods

if "key" in dictionary:     # check before accessing
    print("Found it")

value = d.get("key", "default")  # safe access
```

## File Operations

```python
# read
with open("file.txt", 'r') as f:
    content = f.read()

# write
with open("file.txt", 'w') as f:
    f.write("Hello world")

# check existence
import os
if os.path.exists("file.txt"):
    print("File exists")

# get size
size = os.path.getsize("file.txt")
```

## Gradio UI Patterns

```python
import gradio as gr

file = gr.File(label="Upload")
btn = gr.Button("Click me", variant="primary")
text = gr.Textbox(label="Enter text")
radio = gr.Radio(choices=["A", "B", "C"], value="A")

btn.click(fn=my_function, inputs=[file], outputs=[text])
```

## JSON Operations

```python
import json

# dict to JSON string
data = {"name": "John", "age": 25}
json_str = json.dumps(data, indent=2)

# JSON string to dict
data = json.loads(json_str)

# save to file
with open("data.json", 'w') as f:
    json.dump(data, f, indent=2)

# load from file
with open("data.json", 'r') as f:
    data = json.load(f)
```

## Quick Answers for Common Questions

**Q: What did you build?**
A file converter that takes PDFs, Word docs, and Excel files and turns them into structured data (JSON, CSV, XML).

**Q: Tech stack?**
Python, PyMuPDF for PDFs, python-docx for Word, pandas for Excel, Gradio for the web UI, Groq API for the chatbot.

**Q: What was hard?**
PDF table extraction — PDFs don't store tables as tables, just positioned text. Used pdfplumber to detect alignment and reconstruct structure.

**Q: How would you improve it?**
Async processing with Celery, caching, REST API, OCR for scanned docs, Docker for deployment.

## Project Stats

- Lines of code: ~1500
- Language: Python
- Libraries: 8+ (Gradio, PyMuPDF, pandas, etc.)
- Input formats: PDF, DOCX, XLSX, TXT, CSV
- Output formats: JSON, CSV, XML, AI Training
- Processing time: ~2 seconds per file
