# Mood Tracker AI Backend Documentation

This project provides two main AI components for the Mood Tracker application:
1.  **Mental Health Chatbot**: An empathetic AI companion.
2.  **Journal Prompt Generator**: Generates personalized journal questions based on mood.

## Interface File: `backend_interface.py`

This file serves as the main entry point for backend integration.

### 1. Chatbot

**Function:** `process_chat_message(user_input, history=None, location=None)`

Use this function to send a user's message to the AI and get a response.

**Arguments:**
*   `user_input` (str): The text message sent by the user.
*   `history` (list, optional): A list of previous message objects to maintain conversation context.
    *   Format: `[{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]`
    *   **Note:** The system automatically limits the history to the last 20 messages to manage token usage.
*   `location` (str, optional): The user's location (e.g., "London, UK").
    *   **Usage:** If provided, the AI will use this to suggest *local* emergency services if the user expresses a crisis (self-harm, suicide, etc.).

**Returns:**
*   (str): The AI's text response.

**Example Usage:**
```python
from backend_interface import process_chat_message

history = [{"role": "user", "content": "Hi"}]
response = process_chat_message("I feel sad", history=history, location="New York, USA")
print(response)
```

### 2. Journal Prompt Generator

**Function:** `generate_journal_prompts(mood)`

Use this function to generate reflective journal questions.

**Arguments:**
*   `mood` (str): The user's current mood.
    *   **Valid Values:**
        *   `excellent`
        *   `very good`
        *   `good`
        *   `okay`
        *   `neutral`
        *   `slightly off`
        *   `low`
        *   `stressed`
        *   `sad`
        *   `awful`

**Returns:**
*   (str): A JSON-formatted string containing the mood and a list of questions.

**Output Format:**
```json
[
  {
    "mood": "happy",
    "questions": [
      "What made you smile today?",
      "List three things you are grateful for."
    ]
  }
]
```

**Example Usage:**
```python
from backend_interface import generate_journal_prompts
import json

json_response = generate_journal_prompts("good")
data = json.loads(json_response)
print(data[0]['questions'])
```

## Setup & Configuration

*   **Environment Variables:** Ensure a `.env` file is present in the root directory with your OpenAI API key:
    ```
    OPENAI_API_KEY=sk-...
    ```
*   **Dependencies:**
    *   `openai`
    *   `python-dotenv`
