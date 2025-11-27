import unittest
from unittest.mock import MagicMock, patch
import os

# Mock env var
os.environ["OPENAI_API_KEY"] = "fake-key"

from chatbot_agent import MentalHealthChatbot

class TestCrisisResponse(unittest.TestCase):
    @patch('chatbot_agent.OpenAI')
    def test_location_in_system_prompt(self, mock_openai):
        # Setup mock
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_completion

        bot = MentalHealthChatbot()
        
        user_input = "I feel hopeless"
        location = "London, UK"
        
        bot.get_response(user_input, user_location=location)
        
        # Verify call args
        call_args = mock_client.chat.completions.create.call_args
        _, kwargs = call_args
        messages = kwargs['messages']
        
        system_message = messages[0]['content']
        
        # Check if location info is injected
        self.assertIn("USER LOCATION INFO:", system_message)
        self.assertIn(location, system_message)
        self.assertIn("suggest searching for or contacting emergency services in London, UK", system_message)
        
        print("\nCrisis location verification passed! System prompt includes location info.")

    @patch('chatbot_agent.OpenAI')
    def test_no_location_no_injection(self, mock_openai):
        # Setup mock
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_completion

        bot = MentalHealthChatbot()
        
        user_input = "I feel hopeless"
        
        bot.get_response(user_input) # No location
        
        # Verify call args
        call_args = mock_client.chat.completions.create.call_args
        _, kwargs = call_args
        messages = kwargs['messages']
        
        system_message = messages[0]['content']
        
        # Check that location info is NOT injected
        self.assertNotIn("USER LOCATION INFO:", system_message)
        
        print("No location verification passed! System prompt is standard.")

if __name__ == '__main__':
    unittest.main()
