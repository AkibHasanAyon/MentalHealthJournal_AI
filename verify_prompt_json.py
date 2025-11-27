import unittest
from unittest.mock import MagicMock, patch
import os
import json

# Mock env var
os.environ["OPENAI_API_KEY"] = "fake-key_"

from prompt_generator import generate_prompt

class TestPromptGenerator(unittest.TestCase):
    @patch('prompt_generator.client')
    def test_json_output_structure(self, mock_client):
        # Setup mock
        mock_completion = MagicMock()
        
        # Mock a valid JSON response matching the NEW structure
        expected_json = {
            "mood": "happy",
            "questions": [
                { "question": "What made you smile today?" },
                { "question": "List three things you are grateful for." }
            ]
        }
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
        self.assertIsInstance(parsed_result, dict)
        self.assertIn("mood", parsed_result)
        self.assertIn("questions", parsed_result)
        self.assertIsInstance(parsed_result["questions"], list)
        self.assertTrue(len(parsed_result["questions"]) > 0)
        
        # Verify questions are objects with "question" key
        first_q = parsed_result["questions"][0]
        self.assertIsInstance(first_q, dict)
        self.assertIn("question", first_q)
        self.assertIsInstance(first_q["question"], str)
        
        # Verify call args to check system prompt
        call_args = mock_client.chat.completions.create.call_args
        _, kwargs = call_args
        messages = kwargs['messages']
        system_message = messages[0]['content']
        
        self.assertIn("single JSON object", system_message)
        self.assertIn("mood", system_message)
        self.assertIn("questions", system_message)
        
        print("\nPrompt JSON verification passed! Output is valid JSON with correct structure.")

if __name__ == '__main__':
    unittest.main()
