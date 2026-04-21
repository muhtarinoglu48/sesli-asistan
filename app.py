import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SpeakZone", page_icon="🎤", layout="centered")

st.title("SpeakZone")
st.markdown("**SpeakZone-Basit Komutlu**")

# ====================== API KEY ======================
API_KEY = "AIzaSyCCSVWIFu-1aRXLr9gETtpSUlwdYIbaihA"   # ← Buraya kendi key'ini yapıştır

if API_KEY == "BURAYA_KENDİ_API_KEYİNİ_YAPISTIR":
    st.error("API Key henüz ayarlanmadı.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')
# ====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

st.write("### Sesli Konuşma")

col1, col2 = st.columns(2)

with col1:
    if st.button("🎤 Konuşmaya Başla", type="primary", use_container_width=True):
        st.session_state.listening = True
        st.rerun()

with col2:
    if st.button("⏹️ Durdur", type="secondary", use_container_width=True):
        st.session_state.listening = False
        st.rerun()

if st.session_state.get("listening", False):
    st.info("🔴 Dinliyorum... Konuş ve 'Durdur' butonuna bas.")

    st.components.v1.html("""
        <script>
            let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'tr-TR';
            recognition.continuous = false;
            recognition.interimResults = false;

            recognition.onresult = function(event) {
                const text = event.results[0][0].transcript;
                const input = document.createElement("input");
                input.type = "hidden";
                input.id = "voice_input";
                input.value = text;
                document.body.appendChild(input);
                input.dispatchEvent(new Event("change"));
            };

            recognition.onerror = function() {
                alert("Ses alınamadı. Tekrar deneyin.");
            };

            recognition.start();
        </script>
    """, height=0)

# Ses metnini yakala
if "voice_input" in st.session_state and st.session_state.voice_input and not st.session_state.get("listening", False):
    user_text = st.session_state.voice_input

    if user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})
        with st.chat_message("user"):
            st.markdown(user_text)

        with st.spinner("Gemini cevap veriyor..."):
            try:
                response = model.generate_content(user_text)
                cevap = response.text
            except:
                cevap = "SpeakZone cevap veremedi."

        st.session_state.messages.append({"role": "assistant", "content": cevap})
        with st.chat_message("assistant"):
            st.markdown(cevap)

        st.components.v1.html(f"""
            <script>
                const utterance = new SpeechSynthesisUtterance("{cevap.replace('"', '\\"')}");
                utterance.lang = 'tr-TR';
                speechSynthesis.speak(utterance);
            </script>
        """, height=0)

        st.session_state.voice_input = ""

# Yazılı giriş
prompt = st.chat_input("Veya buraya yaz...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Gemini düşünüyor..."):
        response = model.generate_content(prompt)
        cevap = response.text

    st.session_state.messages.append({"role": "assistant", "content": cevap})
    with st.chat_message("assistant"):
        st.markdown(cevap)

    st.components.v1.html(f"""
        <script>
            const utterance = new SpeechSynthesisUtterance("{cevap.replace('"', '\\"')}");
            utterance.lang = 'tr-TR';
            speechSynthesis.speak(utterance);
        </script>
    """, height=0)

st.caption("SpeakZone")
