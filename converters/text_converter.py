"""
Text file converter (TXT, CSV, etc.)
"""
import csv
import chardet
from typing import Dict, Any
from .base_converter import BaseConverter


class TextConverter(BaseConverter):
    """Convert text files to structured data"""
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.encoding = self._detect_encoding()
        
    def _detect_encoding(self) -> str:
        """Detect file encoding"""
        try:
            with open(self.file_path, 'rb') as file:
                raw_data = file.read()
                result = chardet.detect(raw_data)
                return result['encoding'] or 'utf-8'
        except:
            return 'utf-8'
    
    def extract(self) -> Dict[str, Any]:
        """Extract text content"""
        try:
            # Check if it's a CSV file
            if self.file_path.lower().endswith('.csv'):
                return self._extract_csv()
            else:
                return self._extract_plain_text()
                
        except Exception as e:
            return {
                "error": f"Failed to extract text file: {str(e)}",
                "document_type": "Text File"
            }
    
    def _extract_plain_text(self) -> Dict[str, Any]:
        """Extract plain text file"""
        with open(self.file_path, 'r', encoding=self.encoding) as file:
            content = file.read()
            lines = content.split('\n')
            
            result = {
                "document_type": "Text File",
                "encoding": self.encoding,
                "total_lines": len(lines),
                "total_characters": len(content),
                "word_count": len(content.split()),
                "full_text": content,
                "lines": [{"line_number": i+1, "text": line} for i, line in enumerate(lines) if line.strip()],
                "metadata": self.get_metadata()
            }
            
            return result
    
    def _extract_csv(self) -> Dict[str, Any]:
        """Extract CSV file"""
        rows = []
        
        with open(self.file_path, 'r', encoding=self.encoding) as file:
            csv_reader = csv.DictReader(file)
            headers = csv_reader.fieldnames
            
            for row in csv_reader:
                rows.append(row)
        
        result = {
            "document_type": "CSV File",
            "encoding": self.encoding,
            "total_rows": len(rows),
            "total_columns": len(headers) if headers else 0,
            "headers": headers,
            "data": rows,
            "preview": rows[:10] if rows else [],
            "metadata": self.get_metadata()
        }
        
        return result
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get text file metadata"""
        return {
            "encoding": self.encoding,
            "file_extension": self.file_path.split('.')[-1].upper()
        }
