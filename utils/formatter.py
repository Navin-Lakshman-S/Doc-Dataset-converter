"""
Data formatter for converting to various output formats
"""
import json
import csv
from typing import Dict, Any, List
import os


class DataFormatter:
    """Format extracted data into various output formats"""
    
    @staticmethod
    def to_json(data: Dict[str, Any], pretty: bool = True) -> str:
        """Convert data to JSON format"""
        if pretty:
            return json.dumps(data, indent=2, ensure_ascii=False, default=str)
        else:
            return json.dumps(data, ensure_ascii=False, default=str)
    
    @staticmethod
    def to_csv(data: List[Dict[str, Any]], output_path: str) -> str:
        """Convert data to CSV format"""
        if not data:
            return "No data to convert to CSV"
        
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = list(data[0].keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for row in data:
                    # Convert nested structures to strings
                    cleaned_row = {
                        k: json.dumps(v) if isinstance(v, (dict, list)) else v 
                        for k, v in row.items()
                    }
                    writer.writerow(cleaned_row)
            
            return output_path
        except Exception as e:
            return f"Error creating CSV: {str(e)}"
    
    @staticmethod
    def to_xml(data: Dict[str, Any], root_name: str = "document") -> str:
        """Convert data to XML format"""
        def dict_to_xml(d, root):
            xml_str = f"<{root}>\n"
            
            for key, value in d.items():
                safe_key = key.replace(' ', '_').replace('-', '_')
                
                if isinstance(value, dict):
                    xml_str += f"  {DataFormatter.dict_to_xml_helper(value, safe_key, 2)}\n"
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            xml_str += f"  {DataFormatter.dict_to_xml_helper(item, safe_key, 2)}\n"
                        else:
                            xml_str += f"  <{safe_key}>{item}</{safe_key}>\n"
                else:
                    xml_str += f"  <{safe_key}>{value}</{safe_key}>\n"
            
            xml_str += f"</{root}>"
            return xml_str
        
        return f'<?xml version="1.0" encoding="UTF-8"?>\n{dict_to_xml(data, root_name)}'
    
    @staticmethod
    def dict_to_xml_helper(d, tag, indent_level):
        """Helper function for XML conversion with proper indentation"""
        indent = "  " * indent_level
        xml_str = f"<{tag}>\n"
        
        for key, value in d.items():
            safe_key = key.replace(' ', '_').replace('-', '_')
            
            if isinstance(value, dict):
                xml_str += f"{indent}  {DataFormatter.dict_to_xml_helper(value, safe_key, indent_level + 1)}\n"
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        xml_str += f"{indent}  {DataFormatter.dict_to_xml_helper(item, safe_key, indent_level + 1)}\n"
                    else:
                        xml_str += f"{indent}  <{safe_key}>{item}</{safe_key}>\n"
            else:
                xml_str += f"{indent}  <{safe_key}>{value}</{safe_key}>\n"
        
        xml_str += f"{indent}</{tag}>"
        return xml_str
    
    @staticmethod
    def create_ai_training_format(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a standardized format optimized for AI training
        
        Returns a structure with:
        - input: The main content
        - metadata: Document metadata
        - features: Extracted features for ML
        """
        ai_format = {
            "input_text": "",
            "metadata": {},
            "features": {},
            "structured_data": []
        }
        
        # Extract main text content
        if "full_text" in data:
            ai_format["input_text"] = data["full_text"]
        
        # Extract metadata
        if "metadata" in data:
            ai_format["metadata"] = data["metadata"]
        
        # Extract features
        ai_format["features"] = {
            "document_type": data.get("document_type", "unknown"),
            "word_count": len(data.get("full_text", "").split()),
            "has_tables": "tables" in data and len(data.get("tables", [])) > 0,
            "has_structure": "pages" in data or "paragraphs" in data
        }
        
        # Extract structured data (tables, lists, etc.)
        if "tables" in data:
            ai_format["structured_data"] = data["tables"]
        elif "data" in data:
            ai_format["structured_data"] = data["data"]
        
        return ai_format
    
    @staticmethod
    def get_statistics(data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate statistics about the extracted data"""
        stats = {
            "document_type": data.get("document_type", "Unknown"),
            "total_size": 0,
            "text_length": 0,
            "word_count": 0,
            "has_tables": False,
            "table_count": 0
        }
        
        # Text statistics
        if "full_text" in data:
            text = data["full_text"]
            stats["text_length"] = len(text)
            stats["word_count"] = len(text.split())
        
        # Table statistics
        if "tables" in data:
            stats["has_tables"] = True
            stats["table_count"] = len(data["tables"])
        
        # Page/section count
        if "total_pages" in data:
            stats["total_pages"] = data["total_pages"]
        elif "total_paragraphs" in data:
            stats["total_paragraphs"] = data["total_paragraphs"]
        
        return stats
