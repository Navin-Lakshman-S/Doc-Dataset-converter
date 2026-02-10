# Quick Start Guide

## 🚀 Running the AI Data Conversion Tool

### Option 1: Quick Start (Recommended)

```bash
# Make the setup script executable
chmod +x setup.sh

# Run the setup script
./setup.sh

# Start the application
python app.py
```

### Option 2: Manual Setup

```bash
# 1. Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate     # On Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Test the setup (optional)
python test_setup.py

# 4. Run the application
python app.py
```

### Option 3: Direct Run (if dependencies already installed)

```bash
python app.py
```

---

## 🌐 Accessing the Application

Once the application starts, you'll see output like:

```
Running on local URL:  http://0.0.0.0:7860
```

Open your web browser and navigate to:
- **http://localhost:7860**

---

## 📝 Quick Test

1. **Upload a file**: Click "Upload Document" and select any PDF, Word, Excel, or text file
2. **Choose format**: Select your preferred output format (JSON recommended for first test)
3. **Click Convert**: Hit the "🚀 Convert to Dataset" button
4. **View Results**: See the preview and download your converted file

---

## 🐛 Troubleshooting

### Issue: "Module not found" error

**Solution**:
```bash
pip install -r requirements.txt
```

### Issue: "Port 7860 already in use"

**Solution**: Kill the process using that port or change the port in `app.py`:
```python
interface.launch(server_port=7861)  # Change to different port
```

### Issue: PDF extraction not working

**Solution**: Make sure PyMuPDF is properly installed:
```bash
pip install --upgrade PyMuPDF
```

---

## 📚 Sample Files for Testing

You can test the tool with:
- **PDF**: Any invoice, report, or document
- **Word**: Any .docx file
- **Excel**: Any .xlsx spreadsheet
- **Text**: Any .txt or .csv file

---

## 🔒 Security Note

- Maximum file size: 50MB
- Supported formats only: PDF, DOCX, XLSX, TXT, CSV
- Files are processed locally (not sent to external servers)

---

## 📞 Need Help?

Check the **Documentation** tab in the application for detailed information about:
- Features and capabilities
- Output format examples
- Use cases and best practices

---

## 🎓 For Professor's Review

### Quick Demo Script

1. **Start the app**: `python app.py`
2. **Open browser**: Navigate to http://localhost:7860
3. **Demo Feature 1 - Single File**:
   - Upload a sample PDF
   - Show extraction preview
   - Demonstrate statistics
   - Download JSON output

4. **Demo Feature 2 - Batch Processing**:
   - Switch to "Batch Converter" tab
   - Upload multiple files
   - Show batch results
   - Download ZIP file

5. **Demo Feature 3 - Cleaning Options**:
   - Show text cleaning toggles
   - Compare cleaned vs uncleaned output

6. **Demo Feature 4 - Multiple Formats**:
   - Show JSON output
   - Show CSV output
   - Show AI Training Format

7. **Highlight Documentation Tab**:
   - Show comprehensive documentation
   - Explain use cases
   - Discuss technical stack

---

**Estimated Demo Time**: 10-15 minutes
**Key Points to Emphasize**: 
- Solves real-world problem
- Multiple file format support
- Production-ready code
- Comprehensive documentation
