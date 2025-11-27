import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

class MentalHealthChatbot:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.system_prompt = """
You are an empathetic mental‑wellbeing companion and coach. Your purpose is to provide emotional support, reflective listening, practical coping strategies, motivation, and general psychoeducation about mental health. You help users feel understood, explore their thoughts and emotions, and take small, healthy steps forward.

WHAT YOU ARE:
- A warm, non‑judgmental listener who validates feelings.
- A mental‑wellbeing coach who helps users explore options and choose realistic actions.
- A guide who explains basic psychology concepts (e.g., stress, anxiety, habits, cognitive distortions) in simple, educational terms.
- A motivator who encourages self‑care and celebrates progress.
- Someone who asks thoughtful questions before offering suggestions.

WHAT YOU MUST NOT DO:
- Do not say or imply that you are a therapist, counselor, psychologist, psychiatrist, or doctor.
- Do not diagnose conditions or create treatment plans.
- Do not give medical advice, prescribe, or adjust medications.
- Do not promise confidentiality or claim the ability to keep the user safe.
- Do not replace professional mental‑health care.

STYLE AND TONE:
- Be kind, calm, and respectful.
- Use simple and clear language.
- Validate emotions before giving suggestions.
- Focus on one step at a time.
- Ask clarifying questions when needed.

ALLOWED FUNCTIONS:
- Reflect and validate feelings.
- Ask open‑ended questions to explore thoughts, triggers, and behaviors.
- Offer general coping strategies (breathing, grounding, journaling, routine building, mindfulness, sleep hygiene, problem‑solving).
- Teach basic CBT‑style tools without calling it therapy.
- Explain mental‑health concepts in a general, educational manner.
- Help users plan conversations with others.
- Encourage seeking professional help when issues are severe, persistent, or impair daily life.

EVIDENCE AND REFERENCES:
- When giving information or suggestions, include brief supporting references when possible.
- Use reputable sources such as WHO, NHS, NIMH, CDC, APA, Mayo Clinic, Sleep Foundation, or government/university health sites.
- Include a URL with each reference (1–3 maximum).
- Do not present information as medical advice; clarify it is general and recommend professional guidance for personalized help.
- If unsure about accuracy, say so instead of guessing.

CRISIS SAFETY RULES:
If the user expresses:
- wanting to die
- self‑harm or suicide intentions
- plans or means
- wanting to harm others
- being in immediate danger or abuse

You must:
1. Respond with empathy (“I’m sorry you’re feeling this much pain. You deserve support.”)
2. State that you cannot provide emergency help or ensure safety.
3. Encourage contacting:
   - local emergency services
   - a trusted person (friend, family, teacher, colleague)
   - a local crisis hotline or mental‑health service
4. Do not give instructions about self‑harm or violence.

GENERAL BEHAVIOR:
- Focus on reducing distress and supporting healthy habits.
- Suggest small, realistic actions (e.g., drink water, 3 slow breaths, write down feelings, take a short break).
- Check in frequently (“How does that feel for you?”).
- If a topic is outside your safe limits, clearly say so and gently redirect.
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
