import uuid
import openai
import streamlit as st

# Initialize OpenAI API client
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Skiilar Immigration Assistant ✈️")

# Simplified and flexible instructions for Skiilar, the Immigration Assistant
system_message_content = """
You are Skiilar, a helpful and knowledgeable immigration assistant. Your main goals are to provide clear, accurate, and friendly assistance regarding visa applications. Here are your guiding principles:

General Behavior and Tone
- Be polite, friendly, and supportive.
- Always thank users for their questions and express readiness to help.
- Provide clear and concise information.
- Use structured responses for clarity when needed.
- Be patient and understanding.
- Offer encouragement and ensure users feel supported.

Specific Visa Process Instructions
- For different visa types (student, business, work, travel), provide relevant information about requirements and procedures.
- If specific resources are mentioned (like guides), inform users where they can find them.

Interaction Flow
- Greet users and offer assistance.
- Understand the user's needs by asking relevant questions.
- Provide structured and clear information based on the user's responses.
- Offer additional information and resources proactively.
- Close conversations by ensuring the user has all the needed information and offering further assistance if required.

Remember to be flexible and adapt to the user's needs, providing the best possible assistance for their specific situation.
"""

# Initialize session_state.messages if it doesn't exist
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Add detailed instructions to the initial system message if not already added
if not any(message["role"] == "system" for message in st.session_state["messages"]):
    st.session_state.messages.append({"role": "system", "content": system_message_content})

st.sidebar.title("Navigator")
if st.sidebar.button("Go to Home Page"):
    # redirect to the home page
    st.sidebar.markdown("[Go to Home Page](http://www.yourwebsite.com)", unsafe_allow_html=True)
    st.write("Redirecting to the home page...")

if st.sidebar.button("Clear Session History"):
    # Logic to clear session history
    st.session_state["messages"] = []
    st.write("Session history cleared.")

# Generate a unique thread_id for each user session
thread_id = str(uuid.uuid4())

# Display the chat messages
for message in st.session_state.messages:
    if message["role"] != "system":  # Do not display system messages to users
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Temporarily using a general model ID
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            assistant_message = response['choices'][0]['message']['content']
            st.markdown(assistant_message)
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    except openai.error.InvalidRequestError as e:
        st.error(f"Invalid Request Error: {e}")
        st.session_state.messages.append({"role": "system", "content": f"Error: {e}"})
    except openai.error.AuthenticationError as e:
        st.error(f"Authentication Error: {e}")
        st.session_state.messages.append({"role": "system", "content": f"Error: {e}"})
    except openai.error.OpenAIError as e:  # Catching all OpenAI errors
        st.error(f"OpenAI Error: {e}")
        st.session_state.messages.append({"role": "system", "content": f"Error: {e}"})
    except Exception as e:  # Catch all other exceptions
        st.error(f"Unexpected Error: {e}")
        st.session_state.messages.append({"role": "system", "content": f"Error: {e}"})

# Output the session state for debugging
st.write("Current session state:", st.session_state)
