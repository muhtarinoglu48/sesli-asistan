import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SpeakZone", page_icon="🧠", layout="centered")

st.title("🧠 SpeakZone")
st.markdown("**Kusursuz Zeki Asistan**")

# ====================== API KEY ======================
API_KEY = "AIzaSyCCSVWIFu-1aRXLr9gETtpSUlwdYIbaihA"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')
# ====================================================

# Güçlü System Prompt
system_prompt = """Sen SpeakZone adlı çok zeki, samimi ve esprili bir yapay zeka asistanısın. 
Kullanıcıyla yakın arkadaş gibi konuş. 
Cevaplarını kısa, net ve doğal tut. 
Espri yapabilirsin. 
Kullanıcıya "kanki", "kral", "reis" gibi samimi kelimeler kullanabilirsin. 
Her soruya mantıklı ve faydalı cevap ver."""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": "Selam kralım! Ben SpeakZone. Ne istiyorsun bugün? 🔥"}
    ]

# Mesajları göster
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Kullanıcı girişi
prompt = st.chat_input("Ne sormak istiyorsun?")

if prompt:
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Düşünüyorum..."):
        try:
            # Tüm sohbet geçmişini modele gönder
            response = model.generate_content(st.session_state.messages)
            cevap = response.text
        except Exception as e:
            cevap = "Bir sorun oluştu, tekrar dener misin kanki?"

    # Asistan cevabını ekle
    st.session_state.messages.append({"role": "assistant", "content": cevap})
    with st.chat_message("assistant"):
        st.markdown(cevap)

st.caption("Sohbet geçmişini hatırlıyorum. İstediğin kadar devam edebilirsin.")
