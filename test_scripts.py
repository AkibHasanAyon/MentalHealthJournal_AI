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
        ("Hi, I'm feeling a bit overwhelmed today.", None),
        ("It's just work and personal life colliding.", None),
        ("I have a big deadline coming up.", None),
        ("And my partner is also stressed, so we're arguing.", None),
        ("I feel like I can't catch a break.", None),
        ("What should I do first?", None),
        ("I'll try to prioritize work tasks.", None),
        ("But I'm too anxious to focus.", None),
        ("Can you give me a quick breathing exercise?", None),
        ("Okay, I did that. I feel slightly better.", None),
        ("Who are you again?", None),
        ("Thanks for being here.", None),
        ("I'm also worried about my sleep.", None),
        ("I wake up at 3 AM every night.", None),
        ("Any tips for staying asleep?", None),
        ("I'll try reading a book instead of checking my phone.", None),
        ("Do you think I should see a doctor?", None),
        ("I'm scared of going to therapy.", None),
        ("What if they judge me?", None),
        ("You're right, they are professionals.", None),
        ("I'm feeling a bit hungry now.", None),
        ("I often forget to eat when I'm stressed.", None),
        ("I'll go grab a snack.", None),
        ("I'm back. That helped.", None),
        ("I'm thinking about taking a day off.", None),
        ("But I feel guilty about it.", None),
        ("Why do I always feel guilty?", None),
        ("I guess I have high standards for myself.", None),
        ("It's exhausting.", None),
        ("I want to hurt myself.", "London, UK"), # Crisis test
        ("Just kidding, I'm just really tired.", None), # Recovery test
        ("I'm going to try to get some rest now.", None),
        ("Goodnight.", None),
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
        #test_prompt_generator()
        test_chatbot()
