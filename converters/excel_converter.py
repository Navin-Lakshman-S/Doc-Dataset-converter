"""
Excel spreadsheet converter
"""
import pandas as pd
from typing import Dict, Any, List
from .base_converter import BaseConverter


class ExcelConverter(BaseConverter):
    """Convert Excel files to structured data"""
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
        
    def extract(self) -> Dict[str, Any]:
        """Extract data from Excel spreadsheet"""
        try:
            # Read all sheets
            excel_file = pd.ExcelFile(self.file_path)
            sheet_names = excel_file.sheet_names
            
            sheets_data = []
            all_data = []
            
            for sheet_name in sheet_names:
                df = pd.read_excel(self.file_path, sheet_name=sheet_name)
                
                # Convert DataFrame to structured format
                sheet_data = {
                    "sheet_name": sheet_name,
                    "rows": len(df),
                    "columns": len(df.columns),
                    "column_names": df.columns.tolist(),
                    "data": df.to_dict('records'),
                    "preview": df.head(10).to_dict('records'),
                    "statistics": self._get_statistics(df)
                }
                
                sheets_data.append(sheet_data)
                all_data.extend(df.to_dict('records'))
            
            result = {
                "document_type": "Excel Spreadsheet",
                "total_sheets": len(sheet_names),
                "sheet_names": sheet_names,
                "sheets": sheets_data,
                "all_data": all_data,
                "metadata": self.get_metadata()
            }
            
            return result
            
        except Exception as e:
            return {
                "error": f"Failed to extract Excel file: {str(e)}",
                "document_type": "Excel Spreadsheet"
            }
    
    def _get_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get basic statistics for the DataFrame"""
        stats = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "null_values": df.isnull().sum().to_dict(),
            "data_types": df.dtypes.astype(str).to_dict()
        }
        
        # Add numeric statistics if available
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            stats["numeric_summary"] = df[numeric_cols].describe().to_dict()
        
        return stats
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get Excel file metadata"""
        return {
            "file_type": "Excel Spreadsheet",
            "format": self.file_path.split('.')[-1].upper()
        }
