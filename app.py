import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Eren'in Asistanı", page_icon="🧠", layout="centered")

st.title("SpeakZone")
st.markdown("**SpeakZone - Kusursuz Mod**")

# ====================== API KEY ======================
API_KEY = "AIzaSyCCSVWIFu-1aRXLr9gETtpSUlwdYIbaihA"   # ← Buraya kendi key'ini yapıştır

if API_KEY == "BURAYA_KENDİ_GEMINI_API_KEYİNİ_YAPISTIR":
    st.error("API Key henüz ayarlanmadı.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')
# ====================================================

# Güçlü System Prompt (zeka + kişilik)
system_prompt = """Sen Eren'in yakın arkadaşı gibi konuşan, çok zeki, samimi, esprili ve yardımcı bir asistanısın.

Kurallar:
- Cevaplarını doğal, akıcı ve samimi tut.
- Kısa ve öz ol, gereksiz uzun yazma.
- Espri ve mizah yapabilirsin.
- Kullanıcıya "kanki", "kral" gibi samimi kelimeler kullan.
- Her soruya mantıklı ve faydalı cevap ver.

Senin adın "Erenin tabancası"."""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": "Selam kralım! Artık daha zeki ve kusursuz moddayım. Ne istiyorsun? 🔥"}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

prompt = st.chat_input("Ne sormak istiyorsun kanki?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Düşünüyorum..."):
        try:
            response = model.generate_content(st.session_state.messages)
            cevap = response.text
        except Exception as e:
            cevap = "Reis şuan tadilat var azdan gel"

    st.session_state.messages.append({"role": "assistant", "content": cevap})
    with st.chat_message("assistant"):
        st.markdown(cevap)

st.caption("Şu an en zeki moddayım. İstediğin her şeyi sorabilirsin.")
