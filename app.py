import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Eren'in Asistanı", page_icon="🎤", layout="centered")

st.title("🎙️ Eren'in Sesli Asistanı")
st.markdown("**Gemini - Basit Sesli Mod**")

api_key = st.sidebar.text_input("🔑 Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.warning("Sol taraftan Gemini API Key gir!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ====================== SESLİ KONUŞMA ======================
if st.button("🎤 Konuşmaya Başla", type="primary", use_container_width=True):
    st.info("🔴 Dinliyorum... Konuş ve bitir.")

    st.components.v1.html("""
        <script>
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'tr-TR';
            recognition.interimResults = false;

            recognition.onresult = function(event) {
                const text = event.results[0][0].transcript;
                // Streamlit'e metni göndermek için
                const input = document.createElement('input');
                input.type = 'hidden';
                input.id = 'voice_result';
                input.value = text;
                document.body.appendChild(input);
                input.dispatchEvent(new Event('change'));
            };

            recognition.onerror = function() {
                alert("Ses alınamadı. Tekrar dene kanki.");
            };

            recognition.start();
        </script>
    """, height=0)

# Ses sonucunu yakala
if "voice_result" in st.session_state and st.session_state.voice_result:
    user_text = st.session_state.voice_result

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

    # Sesli cevap
    st.components.v1.html(f"""
        <script>
            const utterance = new SpeechSynthesisUtterance("{cevap.replace('"', '\\"')}");
            utterance.lang = 'tr-TR';
            speechSynthesis.speak(utterance);
        </script>
    """, height=0)

    st.session_state.voice_result = ""

# Yazılı yedek
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

st.caption("Butona bas → konuş → bırak. Metin yazılmazsa sayfayı yenile ve tekrar dene.")