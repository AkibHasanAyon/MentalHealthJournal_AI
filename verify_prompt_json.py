import unittest
from unittest.mock import MagicMock, patch
import os
import json

# Mock env var
os.environ["OPENAI_API_KEY"] = "fake-key"

from prompt_generator import generate_prompt

class TestPromptGenerator(unittest.TestCase):
    @patch('prompt_generator.OpenAI')
    def test_json_output_structure(self, mock_openai):
        # Setup mock
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_completion = MagicMock()
        
        # Mock a valid JSON response
        expected_json = [
            {
                "mood": "happy",
                "questions": [
                    "What made you smile today?",
                    "List three things you are grateful for."
                ]
            }
        ]
        mock_completion.choices[0].message.content = json.dumps(expected_json)
        mock_client.chat.completions.create.return_value = mock_completion

        # Test with a new mood
        mood = "happy"
        result = generate_prompt(mood)
        
        # Verify the result is valid JSON
        try:
            parsed_result = json.loads(result)
        except json.JSONDecodeError:
            self.fail("Result is not valid JSON")
            
        # Verify structure
        self.assertIsInstance(parsed_result, list)
        self.assertEqual(len(parsed_result), 1)
        self.assertIn("mood", parsed_result[0])
        self.assertIn("questions", parsed_result[0])
        self.assertIsInstance(parsed_result[0]["questions"], list)
        
        # Verify call args to check system prompt
        call_args = mock_client.chat.completions.create.call_args
        _, kwargs = call_args
        messages = kwargs['messages']
        system_message = messages[0]['content']
        
        self.assertIn("valid JSON array", system_message)
        self.assertIn("mood", system_message)
        self.assertIn("questions", system_message)
        
        print("\nPrompt JSON verification passed! Output is valid JSON with correct structure.")

if __name__ == '__main__':
    unittest.main()
