import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SpeakZone", page_icon="🧠", layout="centered")

st.title("🧠 SpeakZone")
st.markdown("**Zeki Asistan**")

# API KEY
API_KEY = "AIzaSyCCSVWIFu-1aRXLr9gETtpSUlwdYIbaihA"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# System Prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "content": "Sen SpeakZone adlı zeki, samimi ve esprili bir asistansın. Kullanıcıyla arkadaş gibi konuş. Cevaplarını kısa ve doğal tut."},
        {"role": "model", "content": "Tamam kralım, anlaştık. Ne istiyorsun?"}
    ]

for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    elif msg["role"] == "model":
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

prompt = st.chat_input("Ne sormak istiyorsun?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Düşünüyorum..."):
        try:
            # Daha stabil yöntem
            chat = model.start_chat(history=st.session_state.messages[:-1])
            response = chat.send_message(prompt)
            cevap = response.text
        except Exception as e:
            cevap = f"Bir hata oluştu: {str(e)}"

    st.session_state.messages.append({"role": "model", "content": cevap})
    with st.chat_message("assistant"):
        st.markdown(cevap)

st.caption("SpeakZone - Sohbet devam ediyor")
