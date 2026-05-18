import streamlit as st
from google import genai

api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

st.set_page_config(page_title="ChatBot_App")
st.title("Welcome to ChatBot App 👋")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Enter any question:")

MODELS_LIST = [
    'gemini-2.5-flash',
    'gemini-1.5-flash',
    'gemini-1.5-flash-8b',
    'gemini-1.5-pro'
]

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    reply = ""
    for model_name in MODELS_LIST:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            reply = response.text
            break
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                continue
            else:
                reply = f"Error: {str(e)}"
                break
    
    if not reply:
        reply = "⚠️ Sorry, all free Google models have exhausted their daily quota. Please try again later!"

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    with st.chat_message("assistant"):
        st.markdown(reply)
