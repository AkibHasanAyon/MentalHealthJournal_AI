import unittest
from unittest.mock import MagicMock, patch
import os
import json

# Mock env var
os.environ["OPENAI_API_KEY"] = "fake-key"

from backend_interface import process_chat_message, generate_journal_prompts

class TestBackendInterface(unittest.TestCase):
    @patch('chatbot_agent.OpenAI')
    def test_process_chat_message(self, mock_openai):
        # Setup mock
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Chat response"
        mock_client.chat.completions.create.return_value = mock_completion

        response = process_chat_message("Hello", location="Test City")
        
        self.assertEqual(response, "Chat response")
        
        # Verify location was passed down
        call_args = mock_client.chat.completions.create.call_args
        _, kwargs = call_args
        messages = kwargs['messages']
        system_message = messages[0]['content']
        self.assertIn("Test City", system_message)
        print("\nBackend Chatbot interface verification passed!")

    @patch('prompt_generator.OpenAI')
    def test_generate_journal_prompts(self, mock_openai):
        # Setup mock
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_completion = MagicMock()
        expected_json = '[{"mood": "good", "questions": ["Q1"]}]'
        mock_completion.choices[0].message.content = expected_json
        mock_client.chat.completions.create.return_value = mock_completion

        response = generate_journal_prompts("good")
        
        self.assertEqual(response, expected_json)
        print("Backend Prompt Generator interface verification passed!")

if __name__ == '__main__':
    unittest.main()
