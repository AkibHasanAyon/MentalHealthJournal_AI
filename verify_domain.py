from chatbot_agent import MentalHealthChatbot

def test_domain_restriction():
    bot = MentalHealthChatbot()
    history = []

    print("--- Test 1: Off-topic (Trivia) ---")
    user_input_1 = "What is the capital of France?"
    print(f"User: {user_input_1}")
    response_1 = bot.get_response(user_input_1, history)
    print(f"Bot: {response_1}")
    
    if "mental" in response_1.lower() or "support" in response_1.lower() or "can't help" in response_1.lower():
        print("[PASS] Off-topic refused.")
    else:
        print("[FAIL] Off-topic NOT refused.")

    print("\n--- Test 2: On-topic (Mental Health) ---")
    user_input_2 = "I'm feeling really anxious about my job."
    print(f"User: {user_input_2}")
    response_2 = bot.get_response(user_input_2, history)
    print(f"Bot: {response_2}")

    if "anxious" in response_2.lower() or "job" in response_2.lower() or "hear" in response_2.lower():
        print("[PASS] On-topic accepted.")
    else:
        print("[FAIL] On-topic response seems weird.")

    print("\n--- Test 3: Borderline (Coding Stress) ---")
    user_input_3 = "I can't fix this bug in my python code and it's making me panic."
    print(f"User: {user_input_3}")
    response_3 = bot.get_response(user_input_3, history)
    print(f"Bot: {response_3}")

    if "code" in response_3.lower() and ("panic" in response_3.lower() or "stress" in response_3.lower()):
        print("[PASS] Borderline handled correctly (focused on panic/stress).")
    elif "def " in response_3 or "import " in response_3:
        print("[FAIL] Bot provided code instead of support.")
    else:
        print("[PASS] Borderline handled (likely focused on emotion).")

if __name__ == "__main__":
    test_domain_restriction()
