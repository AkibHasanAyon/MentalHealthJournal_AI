import unittest
from unittest.mock import MagicMock, patch
import os

# Mock env var before importing if needed, though load_dotenv handles it safely usually
os.environ["OPENAI_API_KEY"] = "fake-key"

from chatbot_agent import MentalHealthChatbot

class TestContextHandling(unittest.TestCase):
    @patch('chatbot_agent.OpenAI')
    def test_context_passed_correctly(self, mock_openai):
        # Setup mock
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_completion

        bot = MentalHealthChatbot()
        
        history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"}
        ]
        
        user_input = "How are you?"
        
        bot.get_response(user_input, history)
        
        # Verify call args
        call_args = mock_client.chat.completions.create.call_args
        _, kwargs = call_args
        messages = kwargs['messages']
        
        # Expected messages: System + History + User
        # System prompt is at index 0
        self.assertEqual(messages[0]['role'], 'system')
        
        # History should follow
        self.assertEqual(messages[1], history[0])
        self.assertEqual(messages[2], history[1])
        
        # Current user input should be last
        self.assertEqual(messages[3]['role'], 'user')
        self.assertEqual(messages[3]['content'], user_input)
        
        print("\nContext handling verification passed! Messages structure is correct.")

    @patch('chatbot_agent.OpenAI')
    def test_history_limit(self, mock_openai):
        # Setup mock
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_completion

        bot = MentalHealthChatbot()
        
        # Create a history with 25 messages
        history = [{"role": "user", "content": f"msg {i}"} for i in range(25)]
        
        user_input = "New input"
        
        bot.get_response(user_input, history)
        
        # Verify call args
        call_args = mock_client.chat.completions.create.call_args
        _, kwargs = call_args
        messages = kwargs['messages']
        
        # Expected: System (1) + History (20) + User (1) = 22 messages
        self.assertEqual(len(messages), 22)
        
        # First message should be system
        self.assertEqual(messages[0]['role'], 'system')
        
        # First history message in payload should be the 6th message from original history (index 5)
        # because we took the last 20: history[5] to history[24]
        self.assertEqual(messages[1]['content'], "msg 5")
        
        # Last history message should be the last one
        self.assertEqual(messages[20]['content'], "msg 24")
        
        # Final message is user input
        self.assertEqual(messages[21]['content'], user_input)
        
        print("History limit verification passed! Only last 20 messages retained.")

if __name__ == '__main__':
    unittest.main()
