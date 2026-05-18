import streamlit as st
from google import genai
API_KEY = st.secrets["AIzaSyB2C9AkFZAy0W3WH2fPy-vVhuJNiB1Ell0"]
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="ChatBot_App")

st.title("Welcome to ChatBot App 👋")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Enter any question:")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        reply = response.text

    except Exception as e:
        reply = f"Error: {str(e)}"

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    with st.chat_message("assistant"):
        st.markdown(reply)
