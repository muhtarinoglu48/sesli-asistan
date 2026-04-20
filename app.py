import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Eren'in Asistanı", page_icon="🎤", layout="centered")

st.title("🎙️ Eren'in Sesli Asistanı")
st.markdown("**Gemini ile - Paylaşımlı Versiyon**")

# ================== SENİN API KEY'İN BURAYA ==================
# Buraya kendi Gemini API Key'ini yapıştır
API_KEY = AIzaSyCe2vaOP8dJVx7psMGX6uso2lbPzxf2qNE

if API_KEY == AIzaSyCe2vaOP8dJVx7psMGX6uso2lbPzxf2qNE:
    st.error("API Key henüz ayarlanmadı. Lütfen geliştiriciyle iletişime geçin.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')
# ===========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Sesli Konuşma
if st.button("🎤 Konuşmaya Başla", type="primary", use_container_width=True):
    st.info("🔴 Dinliyorum... Konuş ve bitir.")

    st.components.v1.html("""
        <script>
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'tr-TR';
            recognition.interimResults = false;

            recognition.onresult = function(event) {
                const text = event.results[0][0].transcript;
                document.getElementById("spoken").value = text;
                document.getElementById("spoken").dispatchEvent(new Event('input'));
            };

            recognition.start();
        </script>
        <input id="spoken" type="hidden">
    """, height=0)

# Ses metnini işle
if "spoken" in st.session_state and st.session_state.spoken:
    user_text = st.session_state.spoken

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.spinner("Gemini cevap veriyor..."):
        try:
            response = model.generate_content(user_text)
            cevap = response.text
        except:
            cevap = "Gemini şu anda cevap veremedi. Kota dolmuş olabilir."

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

    st.session_state.spoken = ""

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

st.caption("Bu uygulama Eren tarafından paylaşılmıştır.")
