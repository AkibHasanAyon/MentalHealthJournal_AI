import os
import json
from prompt_generator import generate_prompt
from chatbot_agent import MentalHealthChatbot

def test_prompt_generator():
    print("--- Testing Prompt Generator ---")
    moods = [
        "Excited", "Happy", "Calm", "Neutral", "Tired", 
        "Slightly Off", "Anxious", "Stressed", "Sad", "Awful"
    ]
    # Test a subset to save time/tokens, or all if preferred. Let's test a few distinct ones.
    test_moods = ["Happy", "Stressed", "Awful"] 
    
    for mood in test_moods:
        print(f"Mood: {mood}")
        try:
            response = generate_prompt(mood)
            print(f"Raw Response: {response}")
                
        except json.JSONDecodeError:
            print(f"Error: Response was not valid JSON. Raw: {response}")
        except Exception as e:
            print(f"Error: {e}")
        print("-" * 20)

def test_chatbot():
    print("\n--- Testing Chatbot Agent ---")
    bot = MentalHealthChatbot()
    history = []
    
    test_inputs = [
        ("I'm feeling really stressed about work today.", None),
        ("I don't know if I can handle it.", None),
        ("I feel like quitting, but I need the money.", "New York, USA"), # Test location
        ("I want to hurt myself.", "London, UK"), # Test crisis with location
    ]
    
    for user_input, location in test_inputs:
        print(f"User: {user_input} (Location: {location})")
        try:
            response = bot.get_response(user_input, history, user_location=location)
            print(f"Bot: {response}")
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": response})
        except Exception as e:
            print(f"Error: {e}")
        print("-" * 20)

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your API key to run actual tests.")
    else:
        test_prompt_generator()
        #test_chatbot()
