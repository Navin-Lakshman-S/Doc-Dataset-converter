"""
Data cleaning utility for removing noise and formatting text
"""
import re
from typing import List, Dict, Any


class DataCleaner:
    """Clean and preprocess extracted data"""
    
    @staticmethod
    def clean_text(text: str, options: Dict[str, bool] = None) -> str:
        """
        Clean text based on specified options
        
        Args:
            text: Input text to clean
            options: Dictionary of cleaning options
                - remove_extra_spaces: Remove multiple spaces
                - remove_special_chars: Remove special characters
                - remove_numbers: Remove numeric characters
                - lowercase: Convert to lowercase
                - remove_urls: Remove URLs
                - remove_emails: Remove email addresses
                - remove_phone_numbers: Remove phone numbers
        """
        if options is None:
            options = {
                'remove_extra_spaces': True,
                'remove_special_chars': False,
                'remove_numbers': False,
                'lowercase': False,
                'remove_urls': True,
                'remove_emails': False,
                'remove_phone_numbers': False
            }
        
        cleaned_text = text
        
        # Remove URLs
        if options.get('remove_urls', True):
            cleaned_text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', cleaned_text)
        
        # Remove email addresses
        if options.get('remove_emails', False):
            cleaned_text = re.sub(r'\S+@\S+', '', cleaned_text)
        
        # Remove phone numbers (basic pattern)
        if options.get('remove_phone_numbers', False):
            cleaned_text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '', cleaned_text)
            cleaned_text = re.sub(r'\b\d{10}\b', '', cleaned_text)
        
        # Remove special characters
        if options.get('remove_special_chars', False):
            cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', cleaned_text)
        
        # Remove numbers
        if options.get('remove_numbers', False):
            cleaned_text = re.sub(r'\d+', '', cleaned_text)
        
        # Convert to lowercase
        if options.get('lowercase', False):
            cleaned_text = cleaned_text.lower()
        
        # Remove extra spaces
        if options.get('remove_extra_spaces', True):
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
            cleaned_text = cleaned_text.strip()
        
        return cleaned_text
    
    @staticmethod
    def remove_headers_footers(text: str) -> str:
        """Remove common headers and footers patterns"""
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Skip common header/footer patterns
            if re.match(r'^Page \d+ of \d+$', line.strip(), re.IGNORECASE):
                continue
            if re.match(r'^\d+$', line.strip()):  # Page numbers alone
                continue
            if len(line.strip()) < 3:  # Very short lines
                continue
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    @staticmethod
    def remove_duplicates(items: List[Any]) -> List[Any]:
        """Remove duplicate items while preserving order"""
        seen = set()
        result = []
        
        for item in items:
            # Handle dictionaries
            if isinstance(item, dict):
                item_key = str(sorted(item.items()))
            else:
                item_key = item
            
            if item_key not in seen:
                seen.add(item_key)
                result.append(item)
        
        return result
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Normalize all whitespace to single spaces"""
        return ' '.join(text.split())
    
    @staticmethod
    def remove_empty_entries(data: List[Dict]) -> List[Dict]:
        """Remove entries with all empty values"""
        return [
            entry for entry in data 
            if any(str(value).strip() for value in entry.values())
        ]
