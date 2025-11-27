import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Client initialized inside function

def generate_prompt(mood):
    """
    Generates a reflective journal prompt based on the user's mood.
    
    Args:
        mood (str): The user's mood. Expected values: 'excellent', 'very good', 'good', 'okay', 'neutral', 'slightly off', 'low', 'stressed', 'sad', 'awful'.
        
    Returns:
        str: A generated journal prompt question.
    """
    
    # Validate mood (optional, but good for debugging)
    # New 10 moods as requested
    valid_moods = [
        "excellent", "very good", "good", "okay", "neutral", 
        "slightly off", "low", "stressed", "sad", "awful"
    ]
    
    # Normalize input mood to lowercase and remove potential numbering/emojis if passed loosely
    # For now, we assume the input is the text part, but we'll do a simple check
    cleaned_mood = mood.lower().strip()
    
    if cleaned_mood not in valid_moods:
        # Fallback or warning, but we'll proceed with the input as is for flexibility
        pass

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    except Exception as e:
        return f"Error initializing OpenAI client: {e}"

    system_prompt = (
        "You are a helpful mental health journaling assistant. "
        "Your goal is to generate a list of 6 to 8 thoughtful and open-ended journal prompt questions "
        "based on the user's current mood. "
        "The questions should encourage the user to explore their feelings, daily happenings, "
        "and gain perspective. "
        "Keep the tone supportive and appropriate for the mood. "
        "You MUST output the result as a valid JSON array containing a single object with the following structure:\n"
        "[\n"
        "  {\n"
        "    \"mood\": \"<current_mood>\",\n"
        "    \"questions\": [\n"
        "      \"<Question 1>\",\n"
        "      \"<Question 2>\",\n"
        "      ...\n"
        "    ]\n"
        "  }\n"
        "]\n"
        "Do NOT include any markdown formatting (like ```json). Just the raw JSON string."
    )
    
    user_message = f"The user's mood is '{mood}'. Please suggest 6-8 journal prompt questions."

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500,
            response_format={"type": "json_object"} # Enforce JSON mode
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating prompt: {e}"

if __name__ == "__main__":
    # Test the function
    test_mood = "fair"
    print(f"Mood: {test_mood}")
    print(f"Prompt: {generate_prompt(test_mood)}")
