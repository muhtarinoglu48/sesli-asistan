import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Eren'in Asistanı", page_icon="🎤", layout="centered")

st.title("🎙️ Eren'in Sesli Asistanı")
st.markdown("**Gemini ile - İki Butonlu Sesli Mod**")

# ====================== API KEY ======================
API_KEY = "AIzaSyCe2vaOP8dJVx7psMGX6uso2lbPzxf2qNE"   # ← Buraya kendi key'ini yapıştır

if API_KEY.startswith("BURAYA"):
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

# İki Buton
col1, col2 = st.columns(2)

with col1:
    if st.button("🎤 Konuşmaya Başla", type="primary", use_container_width=True):
        st.session_state.listening = True
        st.rerun()

with col2:
    if st.button("⏹️ Durdur", type="secondary", use_container_width=True):
        st.session_state.listening = False
        st.rerun()

# Mikrofon aktifken
if st.session_state.get("listening", False):
    st.info("🔴 Kayıt başladı... Konuş ve 'Durdur' butonuna bas.")

    st.components.v1.html("""
        <script>
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'tr-TR';
            recognition.continuous = true;
            recognition.interimResults = true;

            recognition.onresult = function(event) {
                let transcript = '';
                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    transcript += event.results[i][0].transcript + ' ';
                }
                document.getElementById("voice_text").value = transcript.trim();
                document.getElementById("voice_text").dispatchEvent(new Event('input'));
            };

            recognition.start();
        </script>
        <input id="voice_text" type="hidden">
    """, height=0)

# Konuşma bitince cevap ver
if "voice_text" in st.session_state and st.session_state.voice_text and not st.session_state.get("listening", False):
    user_text = st.session_state.voice_text.strip()

    if user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})
        with st.chat_message("user"):
            st.markdown(user_text)

        with st.spinner("Gemini cevap veriyor..."):
            try:
                response = model.generate_content(user_text)
                cevap = response.text
            except:
                cevap = "Gemini şu anda cevap veremedi."

        st.session_state.messages.append({"role": "assistant", "content": cevap})
        with st.chat_message("assistant"):
            st.markdown(cevap)

        # Sesli cevap oku
        st.components.v1.html(f"""
            <script>
                const utterance = new SpeechSynthesisUtterance("{cevap.replace('"', '\\"')}");
                utterance.lang = 'tr-TR';
                speechSynthesis.speak(utterance);
            </script>
        """, height=0)

        st.session_state.voice_text = ""

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

st.caption("Konuşmaya Başla → Konuş → Durdur butonuna bas")
