"""
File validator for checking file types and sizes
"""
import os
import magic
from typing import Tuple, List


class FileValidator:
    """Validate uploaded files"""
    
    # Supported file types
    SUPPORTED_EXTENSIONS = {
        '.pdf': 'PDF Document',
        '.docx': 'Word Document',
        '.doc': 'Word Document (Legacy)',
        '.xlsx': 'Excel Spreadsheet',
        '.xls': 'Excel Spreadsheet (Legacy)',
        '.csv': 'CSV File',
        '.txt': 'Text File'
    }
    
    # Maximum file size (50MB)
    MAX_FILE_SIZE = 50 * 1024 * 1024
    
    @staticmethod
    def validate_file(file_path: str) -> Tuple[bool, str]:
        """
        Validate if file is supported and within size limits
        
        Returns:
            Tuple of (is_valid, message)
        """
        # Check if file exists
        if not os.path.exists(file_path):
            return False, "File does not exist"
        
        # Check file extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext not in FileValidator.SUPPORTED_EXTENSIONS:
            return False, f"Unsupported file type: {ext}. Supported types: {', '.join(FileValidator.SUPPORTED_EXTENSIONS.keys())}"
        
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > FileValidator.MAX_FILE_SIZE:
            return False, f"File too large: {file_size / (1024*1024):.2f}MB. Maximum size: {FileValidator.MAX_FILE_SIZE / (1024*1024)}MB"
        
        if file_size == 0:
            return False, "File is empty"
        
        return True, f"Valid {FileValidator.SUPPORTED_EXTENSIONS[ext]}"
    
    @staticmethod
    def get_file_type(file_path: str) -> str:
        """Get the file type description"""
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        return FileValidator.SUPPORTED_EXTENSIONS.get(ext, "Unknown")
    
    @staticmethod
    def is_supported(file_path: str) -> bool:
        """Check if file type is supported"""
        _, ext = os.path.splitext(file_path)
        return ext.lower() in FileValidator.SUPPORTED_EXTENSIONS
    
    @staticmethod
    def get_supported_extensions() -> List[str]:
        """Get list of supported file extensions"""
        return list(FileValidator.SUPPORTED_EXTENSIONS.keys())
