"""
Quick test script to verify all converters are working
"""
import os
import sys

# Test imports
print("=" * 60)
print("🧪 AI Data Conversion Tool - Component Test")
print("=" * 60)
print()

def test_import(module_name, display_name):
    """Test if a module can be imported"""
    try:
        __import__(module_name)
        print(f"✅ {display_name:30} OK")
        return True
    except ImportError as e:
        print(f"❌ {display_name:30} FAILED: {e}")
        return False

# Test core dependencies
print("📦 Testing Core Dependencies:")
print("-" * 60)

results = []
results.append(test_import("gradio", "Gradio"))
results.append(test_import("pandas", "Pandas"))
results.append(test_import("numpy", "NumPy"))
results.append(test_import("fitz", "PyMuPDF"))
results.append(test_import("docx", "python-docx"))
results.append(test_import("openpyxl", "OpenPyXL"))
results.append(test_import("pdfplumber", "pdfplumber"))

print()
print("🔧 Testing Project Modules:")
print("-" * 60)

# Test project modules
results.append(test_import("converters.pdf_converter", "PDF Converter"))
results.append(test_import("converters.word_converter", "Word Converter"))
results.append(test_import("converters.excel_converter", "Excel Converter"))
results.append(test_import("converters.text_converter", "Text Converter"))
results.append(test_import("utils.cleaner", "Data Cleaner"))
results.append(test_import("utils.formatter", "Data Formatter"))
results.append(test_import("utils.validator", "File Validator"))

print()
print("=" * 60)

# Summary
total = len(results)
passed = sum(results)
failed = total - passed

print(f"📊 Test Summary:")
print(f"   Total Tests: {total}")
print(f"   ✅ Passed: {passed}")
print(f"   ❌ Failed: {failed}")
print("=" * 60)

if failed == 0:
    print()
    print("🎉 All tests passed! The system is ready to run.")
    print()
    print("To start the application, run:")
    print("   python app.py")
    print()
    sys.exit(0)
else:
    print()
    print("⚠️  Some tests failed. Please check your installation.")
    print()
    print("Try running:")
    print("   pip install -r requirements.txt")
    print()
    sys.exit(1)
