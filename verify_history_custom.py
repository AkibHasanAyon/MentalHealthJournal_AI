from chatbot_agent import MentalHealthChatbot

def test_chatbot():
    bot = MentalHealthChatbot()
    history = []

    # Turn 1
    user_input_1 = "I'm feeling really overwhelmed today."
    print(f"User: {user_input_1}")
    response_1 = bot.get_response(user_input_1, history)
    print(f"Bot: {response_1}")
    history.append({"role": "user", "content": user_input_1})
    history.append({"role": "assistant", "content": response_1})

    # Turn 2
    user_input_2 = "It's just too much work and I can't focus."
    print(f"\nUser: {user_input_2}")
    response_2 = bot.get_response(user_input_2, history)
    print(f"Bot: {response_2}")
    history.append({"role": "user", "content": user_input_2})
    history.append({"role": "assistant", "content": response_2})

    # Turn 3 - Check History
    user_input_3 = "What was my last text?"
    print(f"\nUser: {user_input_3}")
    response_3 = bot.get_response(user_input_3, history)
    print(f"Bot: {response_3}")
    
    # Verification
    if "too much work" in response_3.lower() or "focus" in response_3.lower():
        print("\n[PASS] History tracking verified.")
    else:
        print("\n[FAIL] History tracking might be broken.")

if __name__ == "__main__":
    test_chatbot()
