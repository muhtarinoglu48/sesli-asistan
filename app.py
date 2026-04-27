import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SpeakZone", page_icon="🧠", layout="centered")

st.title("🧠 SpeakZone")
st.markdown("**Yardımcı Asistan**")

# ====================== API KEY ======================
API_KEY = "AIzaSyA0loFU1S9HOnREY49Gqqb_4V2lJ7V5aF8"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')
# ====================================================

# Sohbet geçmişini başlat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Mesajları göster
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ne sormak istiyorsun?")

if prompt:
    # Kullanıcı mesajını göster
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Düşünüyorum..."):
        try:
            # Doğru formatta mesaj gönderiyoruz
            response = model.generate_content(
                contents=[{"role": "user", "parts": [{"text": prompt}]}]
            )
            cevap = response.text
        except Exception as e:
            cevap = f"Hata oluştu: {str(e)}"

    # Asistan cevabını ekle
    st.session_state.chat_history.append({"role": "assistant", "content": cevap})
    with st.chat_message("assistant"):
        st.markdown(cevap)
