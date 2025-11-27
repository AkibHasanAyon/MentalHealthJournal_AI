import streamlit as st
import os
import json
from backend_interface import process_chat_message, generate_journal_prompts

# Page configuration
st.set_page_config(page_title="Mood Tracker AI", page_icon="🧠")

# Load API key from secrets if available
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Title
st.title("🧠 Mood Tracker AI Companion")

# Tabs
tab1, tab2 = st.tabs(["💬 Chatbot", "📝 Journal Prompts"])

# --- Chatbot Tab ---
with tab1:
    st.header("Mental Health Chatbot")
    
    # Location input for crisis support
    user_location = st.text_input("Your Location (Optional - for local crisis resources):", placeholder="e.g., London, UK")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("How are you feeling today?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get response from backend
        with st.spinner("Thinking..."):
            # Prepare history for backend (list of dicts)
            history = st.session_state.messages[:-1] # Exclude current message as it's passed as input
            response = process_chat_message(prompt, history=history, location=user_location)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- Journal Prompts Tab ---
with tab2:
    st.header("Journal Prompt Generator")
    
    st.write("Select your current mood to get personalized journal questions.")
    
    # Moods list matching the backend
    moods = [
        "Excited", "Happy", "Calm", "Neutral", "Tired", 
        "Slightly Off", "Anxious", "Stressed", "Sad", "Awful"
    ]
    
    selected_mood = st.selectbox("How are you feeling?", moods)
    
    if st.button("Generate Prompts"):
        with st.spinner("Generating prompts..."):
            try:
                json_response = generate_journal_prompts(selected_mood)
                data = json.loads(json_response)
                
                # Display nicely
                if isinstance(data, list) and len(data) > 0:
                    item = data[0]
                    st.subheader(f"Prompts for mood: {item.get('mood', selected_mood)}")
                    
                    questions = item.get("questions", [])
                    for i, q in enumerate(questions, 1):
                        st.markdown(f"**{i}.** {q}")
                    
                    # Show raw JSON for verification
                    with st.expander("View Raw JSON"):
                        st.json(data)
                else:
                    st.error("Unexpected response format.")
                    st.json(data)
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
