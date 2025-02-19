import streamlit as st
from groq import Groq

# Initialize Groq client
client = Groq(api_key="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")

# Streamlit UI
st.subheader("AI Chat - NE", divider="rainbow", anchor=False)

# Initialize session state for chat history and model selection
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "llama3-8b-8192"  # Default model

# Function to limit chat history to avoid token overflow
MAX_MESSAGES = 5  # Adjust to keep the most recent conversations
st.session_state.messages = st.session_state.messages[-MAX_MESSAGES:]

# User input
default_text = """Check the following statement if there is any ambiguity. It should be clinically Correct. Any Clinical Errors Correct it. Provide the correct statement after modification and information should be clinically correct with scientific evidence."""

user_input = st.text_area("You:", default_text, height=200)

if st.button("Send") and user_input:
    # Add user input to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # Call Groq API with streaming enabled to reduce token load
        response = client.chat.completions.create(
            model=st.session_state.selected_model,
            messages=st.session_state.messages,
            stream=True,
        )

        # Display AI response with streaming
        ai_response = ""
        for chunk in response:
            ai_response += chunk.choices[0].delta.content or ""

        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

        # Show AI response
        st.write(f"**AI:** {ai_response}")

    except Exception as e:
        st.error(f"Error: {str(e)} - Please try reducing input size.")

