"""
Chatbot module for querying converted data using Groq API
"""

import os
import json
from typing import List, Tuple
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

class DataChatbot:
    """Chatbot that can answer questions about converted data using Groq API"""
    
    def __init__(self):
        """Initialize the chatbot with Groq API"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
        
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"  # Groq's default model
        self.data_context = None
        self.chat_history = []
    
    def load_data(self, data_content: str, data_format: str = "json"):
        """
        Load converted data to use as context
        
        Args:
            data_content: The converted data as string
            data_format: Format of the data (json, csv, xml, etc.)
        """
        self.data_context = {
            "content": data_content,
            "format": data_format
        }
        self.chat_history = []  # Reset chat history when new data is loaded
    
    def get_response(self, user_message: str) -> str:
        """
        Get a response from the chatbot based on the user's question
        
        Args:
            user_message: User's question about the data
            
        Returns:
            Chatbot's response
        """
        if not self.data_context:
            return "Please load some data first by converting a file."
        
        # Create system message with data context
        system_message = f"""You are a helpful assistant that answers questions about document data.
        
The user has converted a document into the following data format ({self.data_context['format']}):

```
{self.data_context['content'][:4000]}  # Limit context to avoid token limits
```

Answer the user's questions based on this data. Be specific and reference actual values from the data.
If the data is too large to show completely, it may be truncated - mention this if relevant.
Keep your answers concise and helpful."""

        # Build messages list with history
        messages = [{"role": "system", "content": system_message}]
        
        # Add chat history
        for role, content in self.chat_history:
            messages.append({"role": role, "content": content})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Get response from Groq
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.7,
                max_tokens=1024,
            )
            
            response = chat_completion.choices[0].message.content
            
            # Update chat history
            self.chat_history.append(("user", user_message))
            self.chat_history.append(("assistant", response))
            
            # Keep only last 10 exchanges to avoid token limits
            if len(self.chat_history) > 20:
                self.chat_history = self.chat_history[-20:]
            
            return response
            
        except Exception as e:
            return f"Error getting response from chatbot: {str(e)}"
    
    def clear_history(self):
        """Clear chat history"""
        self.chat_history = []
    
    def get_chat_history(self) -> List[dict]:
        """
        Get chat history in format suitable for Gradio Chatbot component (Gradio 6.0+)
        
        Returns:
            List of dicts with 'role' and 'content' keys
        """
        history = []
        for role, content in self.chat_history:
            history.append({"role": role, "content": content})
        return history
