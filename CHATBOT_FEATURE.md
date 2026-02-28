# Chatbot Feature

## Overview

After converting a document, you can ask questions about the data using the built-in chatbot. It uses the Groq API (llama-3.3-70b-versatile model) to generate responses based on your converted content.

## How to Use It

1. **Convert a file first** — go to the Single File Converter tab, upload something, and convert it. JSON format works best for chatbot queries.
2. **Switch to the Chat with Data tab** — the chatbot automatically picks up whatever you just converted.
3. **Ask questions** — type in the text box and hit Send or Enter.

The chatbot keeps conversation history so you can ask follow-up questions.

## Example Questions

**For invoices / financial docs:**
- "What's the total amount?"
- "Who is the vendor?"
- "List the line items"

**For reports / articles:**
- "Summarize the main points"
- "What topics are covered?"
- "What conclusions were made?"

**For spreadsheet data:**
- "How many rows are there?"
- "What are the column names?"
- "What's the highest value in the sales column?"

**For text documents:**
- "What is this about?"
- "List all names mentioned"
- "Summarize in a few bullet points"

## Technical Details

- **chatbot.py** — main module, contains the `DataChatbot` class
- **API** — Groq (free tier), key stored in `.env` as `GROQ_API_KEY`
- **Context window** — first 4000 characters of converted data are sent as context
- **History** — keeps last 10 exchanges (20 messages) to stay within token limits
- **Max response** — 1024 tokens per reply

## Limitations

- Large documents get truncated to 4000 characters for the context window
- Responses depend on how well the conversion captured the original data
- Only knows about the most recently converted document
- History resets if you clear the chat or refresh the page

## Tips

- Use JSON as the output format — it gives the chatbot the most structured context
- Be specific with your questions
- Use "Clear Chat" when switching to a different document
- Always convert a file before trying to chat (otherwise it has no data to work with)

## Error Messages

- **"Please load some data first..."** — you haven't converted a file yet
- **"Error getting response..."** — check your internet connection or API key
- **No response** — the converted data might be too large or malformed

## Possible Future Improvements

- Compare multiple documents in one session
- Upload data directly to the chatbot without converting first
- Better handling of very large documents
- Option to pick different AI models
- Export chat history
