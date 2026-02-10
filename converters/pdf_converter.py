"""
PDF file converter with multiple extraction methods
"""
import fitz  # PyMuPDF
import pdfplumber
from typing import Dict, Any, List
from .base_converter import BaseConverter


class PDFConverter(BaseConverter):
    """Convert PDF files to structured data"""
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.doc = None
        
    def extract(self) -> Dict[str, Any]:
        """Extract text and tables from PDF"""
        try:
            # Use PyMuPDF for text extraction
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
            
            # Extract tables using pdfplumber
            tables = self._extract_tables()
            
            result = {
                "document_type": "PDF",
                "total_pages": len(self.doc),
                "full_text": "\n\n".join(full_text),
                "pages": pages_data,
                "tables": tables,
                "metadata": self.get_metadata()
            }
            
            self.doc.close()
            return result
            
        except Exception as e:
            return {
                "error": f"Failed to extract PDF: {str(e)}",
                "document_type": "PDF"
            }
    
    def _extract_tables(self) -> List[Dict[str, Any]]:
        """Extract tables from PDF using pdfplumber"""
        tables_data = []
        
        try:
            with pdfplumber.open(self.file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    tables = page.extract_tables()
                    
                    for table_idx, table in enumerate(tables):
                        if table:
                            table_data = {
                                "page": page_num + 1,
                                "table_index": table_idx + 1,
                                "rows": len(table),
                                "columns": len(table[0]) if table else 0,
                                "data": table
                            }
                            tables_data.append(table_data)
        except Exception as e:
            pass  # Tables extraction is optional
            
        return tables_data
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get PDF metadata"""
        if not self.doc:
            self.doc = fitz.open(self.file_path)
        
        metadata = self.doc.metadata
        
        return {
            "title": metadata.get("title", "N/A"),
            "author": metadata.get("author", "N/A"),
            "subject": metadata.get("subject", "N/A"),
            "creator": metadata.get("creator", "N/A"),
            "producer": metadata.get("producer", "N/A"),
            "creation_date": metadata.get("creationDate", "N/A"),
            "modification_date": metadata.get("modDate", "N/A")
        }
