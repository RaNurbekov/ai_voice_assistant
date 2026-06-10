import streamlit as st
import os
import io
from dotenv import load_dotenv
from groq import Groq
from gtts import gTTS

# ── Page config ───────────────────────────────────────────
st.set_page_config(
    page_title="Voice AI Banker",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Voice AI Banker — Kaspi Assistant")
st.write(
    "Full voice pipeline: Speech → Whisper STT → "
    "Llama 3 → gTTS. Supports Russian & English."
)

# ── Load API key ──────────────────────────────────────────
load_dotenv()
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("🚨 GROQ_API_KEY not found! Check .env file")
    st.stop()

client = Groq(api_key=api_key)

system_prompt = (
    "You are a friendly voice assistant for Kaspi Bank Kazakhstan. "
    "Answer BRIEFLY and naturally — your text will be spoken aloud. "
    "No lists, asterisks or tables. Speak like a live phone operator. "
    "Support both Russian and English languages."
)

# ── Chat memory ───────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Sidebar ───────────────────────────────────────────────
st.sidebar.title("⚙️ Settings")
language = st.sidebar.selectbox(
    "TTS Language",
    ["ru", "en"],
    index=0,
    help="Language for voice response"
)
if st.sidebar.button("🗑️ Clear conversation"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.divider()
st.sidebar.subheader("💡 Example questions")
st.sidebar.info("🇷🇺 Какой у меня баланс?")
st.sidebar.info("🇷🇺 Как открыть вклад?")
st.sidebar.info("🇬🇧 What are your loan rates?")

# ── Chat history ──────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Input method ──────────────────────────────────────────
st.divider()
input_method = st.radio(
    "Input method:",
    ["🎤 Voice", "⌨️ Text"],
    horizontal=True
)

if input_method == "🎤 Voice":
    audio_bytes = st.audio_input("🎤 Click microphone and ask your question:")
    user_input = None

    if audio_bytes:
        with st.spinner("🎧 Transcribing with Whisper..."):
            try:
                transcription = client.audio.transcriptions.create(
                    file=("audio.wav", audio_bytes.read()),
                    model="whisper-large-v3",
                    prompt="Это диалог клиента с банком.",
                    response_format="text"
                )
                user_input = transcription.strip()
                st.success(f"📝 You said: **{user_input}**")
            except Exception as e:
                st.error(f"STT Error: {e}")
else:
    user_input = st.chat_input("Type your question...")

# ── Process input ─────────────────────────────────────────
if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # ── LLM Response ──────────────────────────────────────
    with st.chat_message("assistant"):
        with st.spinner("🧠 Thinking..."):
            try:
                ai_messages = [
                    {"role": "system", "content": system_prompt}
                ]
                for msg in st.session_state.messages:
                    ai_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })

                response = client.chat.completions.create(
                    messages=ai_messages,
                    model="llama-3.3-70b-versatile",
                    temperature=0.3,
                    max_tokens=200
                )
                bot_text = response.choices[0].message.content
                st.markdown(bot_text)
                st.session_state.messages.append(
                    {"role": "assistant", "content": bot_text}
                )
            except Exception as e:
                st.error(f"LLM Error: {e}")
                st.stop()

    # ── TTS Response ──────────────────────────────────────
    with st.spinner("🔊 Generating voice response..."):
        try:
            tts = gTTS(text=bot_text, lang=language)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            st.audio(
                audio_buffer,
                format="audio/mp3",
                autoplay=True
            )
        except Exception as e:
            st.warning(f"TTS unavailable: {e}")

# ── Footer ─────────────────────────────────────────────────
st.divider()
st.caption(
    "🎙️ Voice AI Banker | "
    "Whisper Large v3 (STT) → Llama 3.3-70B (LLM) → gTTS (TTS) | "
    "Built by Rashid Nurbekov 🇰🇿"
)