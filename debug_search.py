import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def test_config(name, **kwargs):
    print(f"--- Testing {name} ---")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-search-preview",
            messages=[{"role": "user", "content": "What is the weather in San Francisco today?"}],
            max_tokens=50,
            **kwargs
        )
        print("Success!")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Failed: {e}")
    print("\n")

if __name__ == "__main__":
    # Test 1: Just the model
    test_config("Model Only")

    # Test 2: Empty web_search_options
    test_config("Empty web_search_options", web_search_options={})

    # Test 3: web_search_options with search_type (User request)
    test_config("User Request", web_search_options={"search_type": "auto"})
    
    # Test 4: extra_body
    test_config("Extra Body", extra_body={"web_search_options": {"search_type": "auto"}})

    # Test 5: tools web_search
    test_config("Tools web_search", tools=[{"type": "web_search"}])
