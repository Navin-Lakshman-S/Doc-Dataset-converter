"""
Base converter class that all file converters inherit from
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import os


class BaseConverter(ABC):
    """Abstract base class for all file converters"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.file_size = os.path.getsize(file_path)
        
    @abstractmethod
    def extract(self) -> Dict[str, Any]:
        """Extract content from the file"""
        pass
    
    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Get file metadata"""
        pass
    
    def get_file_info(self) -> Dict[str, Any]:
        """Get basic file information"""
        return {
            "file_name": self.file_name,
            "file_size": f"{self.file_size / 1024:.2f} KB",
            "file_path": self.file_path
        }
