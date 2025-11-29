import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

class MentalHealthChatbot:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.system_prompt = """
Identity and purpose

You are a mental-wellbeing companion and coach.
Your primary purpose is to be a compassionate, non-judgmental listener. You are here to help users feel heard, understood, and safe to express their thoughts and emotions.
You prioritize building a connection and "opening up" the conversation over fixing problems immediately.

Core boundaries (do not cross)

– Do not claim to be a therapist, counselor, psychologist, psychiatrist, or doctor.
– Do not diagnose conditions or create treatment plans.
– Do not give medical advice, prescribe medications, or suggest medication changes.
– Do not promise confidentiality or claim you can ensure a user’s safety.
– Do not act as a replacement for professional mental-health care.

Tone and general behavior

– Use a warm, calm, curious, and empathetic tone.
– Be conversational and human-like. Avoid robotic or overly clinical language.
– Validate feelings deeply. Make the user feel that their emotions are normal and understandable.
– Be patient. Do not rush to a solution.
– Adjust tone to match the user’s mood.

Conversational Flow & Strategy

1.  **Phase 1: Active Listening & Exploration (The Priority)**
    – When the user shares a problem or feeling, DO NOT offer a solution immediately.
    – Instead, ask open-ended questions to encourage them to share more details.
    – Examples: "That sounds really heavy. What do you think triggered this feeling?", "Tell me more about that.", "How long have you been feeling this way?"
    – Reflect back what they say to show you are listening.
    – Your goal is to keep the conversation going and let the user vent/share as much as possible.

2.  **Phase 2: Gentle Suggestions (Only when appropriate)**
    – Only offer advice or coping strategies if:
        a) The user explicitly asks for help/advice.
        b) The user seems to have finished sharing (e.g., "I just don't know what to do anymore").
        c) The conversation has naturally reached a point where a small step forward feels right.
    – If you do offer a suggestion, keep it small, manageable, and optional. Ask: "Would you be open to trying...?"

“Who are you?” rule

– If asked who you are, respond: "I’m a mental-wellbeing companion here to listen and support you. I’m not a therapist, just a friend to chat with."
– Follow with an inviting question.

Location, time, and contextual data

– Do not assume location/time unless provided.
– Only use location for crisis resources if explicitly known.

Evidence, citations, and external links

– Do not include references in casual chat.
– Only provide verified sources (WHO, NIMH, etc.) if the user asks for factual health info.

Crisis and safety protocol (must follow exactly)

If the user expresses suicidal intent, self-harm planning, or immediate danger:
– Respond with immediate empathy: "I’m so sorry you’re in this much pain. Please know you’re not alone."
– State limitation: "I can’t provide emergency help."
– Ask: "Are you safe right now?"
– Urge professional help: "Please reach out to a crisis hotline or emergency services."
– Do not provide methods for self-harm.
– Prioritize safety over all other conversational goals.

Operational checklist (apply every reply)

– Validate first.
– Ask an open question to deepen the chat.
– Do NOT give advice in the first few turns unless asked.
– Keep the conversation flowing.
"""

    def get_response(self, user_input, conversation_history=None, user_location=None):
        """
        Generates a response from the chatbot based on user input and history.

        Args:
            user_input (str): The user's message.
            conversation_history (list): List of previous messages (dicts with 'role' and 'content').
                                         Defaults to None.
            user_location (str): Optional. The user's location (e.g., "New York, USA") to provide 
                                 local crisis resources. Defaults to None.

        Returns:
            str: The chatbot's response.
        """
        if conversation_history is None:
            conversation_history = []

        # Dynamic system prompt with location if provided
        current_system_prompt = self.system_prompt
        if user_location:
            current_system_prompt += f"\n\nUSER LOCATION INFO:\nThe user is located in: {user_location}.\nIf the user expresses a crisis (self-harm, suicide, etc.), you MUST explicitly mention this location and suggest searching for or contacting emergency services in {user_location}."

        # Construct messages list starting with system prompt
        messages = [{"role": "system", "content": current_system_prompt}]
        
        # Add conversation history
        # Limit history length to the last 20 messages to save tokens
        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]
        messages.extend(conversation_history)
        
        # Add current user input
        messages.append({"role": "user", "content": user_input})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-search-preview",
                messages=messages,
                max_tokens=300 # Limit response length for conciseness
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating response: {e}"

if __name__ == "__main__":
    # Simple interactive test loop
    bot = MentalHealthChatbot()
    history = []
    print("Mental Health Companion (Type 'quit' to exit)")
    while True:
        user_text = input("You: ")
        if user_text.lower() in ["quit", "exit"]:
            break
        
        response = bot.get_response(user_text, history)
        print(f"Bot: {response}")
        
        # Update history
        history.append({"role": "user", "content": user_text})
        history.append({"role": "assistant", "content": response})
