# Presentation Guide

How to walk your professor through the project.

---

## Opening (30 seconds)

"So this project is a document-to-dataset converter. The idea is — if you want to train an AI model, you need structured data. But most real data is in PDFs, Word docs, spreadsheets. This tool extracts the data, cleans it up, and gives you JSON, CSV, or XML that you can actually use."

---

## The problem (45 seconds)

"In any AI project, most of the time goes into preparing data, not building the model. If you have a bunch of PDFs you want to use for training, you'd normally have to open each one, copy-paste the text, clean it up, format it — that takes forever. This automates all of that."

---

## Live demo — single file (3 minutes)

This is the most important part. Show it actually working.

1. Open the app (should already be running at localhost:7860)
2. Go to "Single File Converter" tab
3. Upload a PDF from test_data/ (the invoice works well)
4. Pick JSON as output format
5. Click "Convert to Dataset"
6. Walk through the results:
   - Status message shows it worked
   - Statistics section shows word count, pages, etc.
   - Preview shows the actual JSON output
   - Download button lets you save the file
7. Then go to "Chat with Data" tab
8. Ask something like "What's the total amount?" or "List the items"
9. Show that the chatbot answers based on the converted data

---

## Live demo — batch processing (1-2 minutes)

1. Go to "Batch Converter" tab
2. Upload 2-3 files (mix of PDF, Word, Excel)
3. Click "Process Batch"
4. Show the results summary (how many succeeded/failed)
5. Download the ZIP

Say something like: "If you had 500 files to process, same thing — upload them all, hit process, download the ZIP."

---

## Technical walkthrough (2 minutes)

Explain the architecture briefly:

"The project is modular. There's a base converter class, and each file type (PDF, Word, Excel, text) has its own converter that inherits from it. So adding a new format would just mean writing a new converter class."

"For PDFs specifically, I use two libraries — PyMuPDF for text and pdfplumber for tables — because no single library handles both well."

"The cleaning module uses regex patterns to strip out things like page numbers, headers, URLs."

"The chatbot uses Groq's API with the llama-3.3-70b model. After converting a file, the data gets passed as context to the LLM so you can ask questions about it."

Tech stack if asked:
- Python
- Gradio (web UI)
- PyMuPDF + pdfplumber (PDFs)
- python-docx (Word)
- pandas (Excel)
- Groq API (chatbot)

---

## Use cases (1 minute)

Pick 2-3 that feel relevant:

- "A law firm with thousands of contracts could convert them all into structured data and train an AI to flag risky clauses."
- "Researchers could convert a bunch of papers into a dataset for systematic review."
- "A company with years of invoices in PDF could extract all the financial data for analysis."

---

## Challenges you solved (1 minute)

If the professor asks about challenges:

1. **PDF tables** — "PDFs don't store tables as actual tables, they're just positioned text. I used pdfplumber specifically for detecting table layouts."

2. **File encoding** — "Different files use different character encodings. I added automatic detection with chardet so it handles international characters."

3. **Consistent output** — "Each file type gives you different raw data. The base converter pattern standardizes the output so the rest of the pipeline doesn't care what the input was."

4. **Chatbot context limits** — "LLMs have token limits, so I truncate the data to 4000 characters for the context and keep chat history to the last 10 exchanges."

---

## Wrapping up (30 seconds)

"So basically — upload documents, get structured data out. Works with the common file types, handles batch processing, cleans up the data, and you can chat with the results. Happy to answer any questions."

---

## Potential questions and answers

**Q: Why Gradio instead of Flask?**
"Gradio is built for ML tools — file upload, preview components, tabs — all out of the box. Flask would have needed a lot more frontend work for the same result."

**Q: How do you handle errors?**
"Every converter has try-catch, and the app shows the user a clear message instead of a traceback. In batch mode, if one file fails, the rest still process."

**Q: Can it handle large files?**
"There's a 50MB limit. Small files process in 1-2 seconds, larger ones in 5-10 seconds."

**Q: What about security?**
"All conversion happens locally. Files don't leave the machine. The chatbot sends data to Groq's API, but the file conversion itself is entirely local."

**Q: Could you add more file types?**
"Yeah, the architecture makes that straightforward. You'd create a new converter class inheriting from BaseConverter, implement extract() and get_metadata(), and register it in the main app."

---

## Before the presentation

- Make sure the app is running (`python app.py`)
- Have sample files ready in test_data/
- Do a test run of the demo flow once
- Make sure the chatbot works (needs internet for Groq API)
- If the demo breaks during presentation, explain what would have happened and show the code instead