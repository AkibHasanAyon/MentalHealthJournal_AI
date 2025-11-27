import os
from prompt_generator import generate_prompt
from chatbot_agent import MentalHealthChatbot

def test_prompt_generator():
    print("--- Testing Prompt Generator ---")
    moods = ["excellent", "happy", "fair", "poor", "worst"]
    for mood in moods:
        print(f"Mood: {mood}")
        try:
            prompt = generate_prompt(mood)
            print(f"Generated Prompt: {prompt}")
        except Exception as e:
            print(f"Error: {e}")
        print("-" * 20)

def test_chatbot():
    print("\n--- Testing Chatbot Agent ---")
    bot = MentalHealthChatbot()
    history = []
    
    test_inputs = [
        "I'm feeling really stressed about work today.",
        "I don't know if I can handle it.",
        "It's just that my boss expects too much from me.",
        "I try to tell him, but he doesn't listen.",
        "I don't know what to do.",
        "what was my previous text?",
        "I feel like quitting, but I need the money.",
        "What are some ways I can calm down right now?",
        "I'll try the breathing exercise. What else?",
        "Thanks, that helps a bit."
    ]
    
    for user_input in test_inputs:
        print(f"User: {user_input}")
        try:
            response = bot.get_response(user_input, history)
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
