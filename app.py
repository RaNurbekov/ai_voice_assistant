import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
from gtts import gTTS

# 1. Настройка страницы
st.set_page_config(page_title="Голосовой Диалог", page_icon="🎙️", layout="centered")
st.title("🎙️ Голосовой ИИ-Банкир (С памятью)")
st.write("Теперь вы можете вести полноценный диалог. ИИ помнит контекст беседы!")

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("🚨 Ключ Groq API не найден! Проверь файл .env")
    st.stop()

client = Groq(api_key=api_key)

system_prompt = (
    "Ты — дружелюбный голосовой ассистент банка Kaspi. "
    "Отвечай КРАТКО, вежливо и по-человечески, так как твой текст будет озвучиваться голосом. "
    "Не используй сложные списки, звездочки или таблицы. Говори как живой собеседник по телефону."
)

# 2. Инициализация ПАМЯТИ (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Отрисовка всей истории чата на экране
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Виджет микрофона (всегда висит внизу)
audio_bytes = st.audio_input("Нажмите на микрофон, чтобы ответить:")

if audio_bytes:
    # --- ШАГ А: УШИ (Whisper) ---
    with st.spinner("🎧 Слушаю вас..."):
        try:
            transcription = client.audio.transcriptions.create(
                file=("audio.wav", audio_bytes.read()),
                model="whisper-large-v3",
                prompt="Это диалог клиента с банком на русском языке.",
                response_format="text"
            )
            user_text = transcription.strip()
        except Exception as e:
            st.error(f"Ошибка распознавания речи: {e}")
            st.stop()
            
    # Сохраняем вопрос в память и рисуем на экране
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    # --- ШАГ Б: МОЗГ (Llama 3) ---
    with st.chat_message("assistant"):
        with st.spinner("🧠 Думаю..."):
            try:
                # ВАЖНО: Передаем нейросети ВСЮ ИСТОРИЮ сообщений!
                ai_messages = [{"role": "system", "content": system_prompt}]
                for msg in st.session_state.messages:
                    ai_messages.append({"role": msg["role"], "content": msg["content"]})
                
                chat_completion = client.chat.completions.create(
                    messages=ai_messages,
                    model="llama-3.3-70b-versatile",
                    temperature=0.3,
                )
                bot_text = chat_completion.choices[0].message.content
                
                st.markdown(bot_text)
                # Сохраняем ответ бота в память
                st.session_state.messages.append({"role": "assistant", "content": bot_text})
            except Exception as e:
                st.error(f"Ошибка ИИ: {e}")
                st.stop()
                
        # --- ШАГ В: ГОЛОС (Google TTS) ---
        with st.spinner("🔊 Озвучиваю..."):
            try:
                tts = gTTS(text=bot_text, lang='ru')
                audio_file = "response.mp3"
                tts.save(audio_file)
                # Автоматически проигрываем голос
                st.audio(audio_file, format="audio/mp3", autoplay=True)
            except Exception as e:
                st.error(f"Ошибка озвучки: {e}")