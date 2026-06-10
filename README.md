# 🎙️ Voice AI Banker — Kaspi Assistant

> **Full voice pipeline: Speech-to-Text → LLM → Text-to-Speech**
> Whisper Large v3 → Llama 3.3-70B → gTTS | Supports Russian & English

---

## 🚀 Live Demo

🔗 **[aivoiceassistant.streamlit.app](https://aivoiceassistant-9uqgi56eevhbe266yyntfz.streamlit.app)**

---

## 🎯 What It Does

A fully voice-driven AI bank assistant — speak your question, get a spoken answer. No typing needed.

```
🎤 User speaks
        │
        ▼
👂 Whisper Large v3 (Groq)
   Speech → Text transcription
   Optimized for Russian banking context
        │
        ▼
🧠 Llama 3.3-70B (Groq)
   Full conversation history passed on every request
   System prompt optimized for TTS — short, natural answers
   No lists, no asterisks — speaks like a phone operator
        │
        ▼
🔊 gTTS (Google Text-to-Speech)
   Text → MP3 audio
   Auto-plays in browser
   Supports Russian & English
```

---

## 🛠 Tech Stack

| Component | Technology |
|---|---|
| **Speech-to-Text** | Whisper Large v3 via Groq API |
| **LLM Engine** | Llama 3.3-70B via Groq API |
| **Text-to-Speech** | gTTS (Google Text-to-Speech) |
| **Conversation Memory** | Streamlit `session_state` |
| **Frontend** | Streamlit (`st.audio_input`, `st.audio`) |
| **Deployment** | Streamlit Cloud |

---

## 🔑 Key Features

### 1. Full Conversation Memory
Every request to Llama 3 includes the **complete conversation history** — the bot remembers the client's name, previous questions and context:

```python
ai_messages = [{"role": "system", "content": system_prompt}]
for msg in st.session_state.messages:
    ai_messages.append({"role": msg["role"], "content": msg["content"]})
```

### 2. TTS-Optimized System Prompt
The prompt is specifically designed for voice output — short answers without lists or formatting, like a live phone operator:

```python
system_prompt = (
    "You are a friendly voice assistant for Kaspi Bank Kazakhstan. "
    "Answer BRIEFLY and naturally — your text will be spoken aloud. "
    "No lists, asterisks or tables. Speak like a live phone operator."
)
```

### 3. BytesIO Audio (Cloud-Compatible)
Audio is generated in memory — no file system writes. Works on Streamlit Cloud:

```python
tts = gTTS(text=bot_text, lang=language)
audio_buffer = io.BytesIO()
tts.write_to_fp(audio_buffer)
audio_buffer.seek(0)
st.audio(audio_buffer, format="audio/mp3", autoplay=True)
```

### 4. Bilingual Support
Switch between Russian and English TTS in the sidebar — same Whisper model handles both languages automatically.

---

## 💡 Example Questions

| Language | Question |
|---|---|
| 🇷🇺 Russian | Какой у меня баланс? |
| 🇷🇺 Russian | Как открыть вклад в Kaspi? |
| 🇷🇺 Russian | Какие у вас условия по кредиту? |
| 🇬🇧 English | What are your loan interest rates? |
| 🇬🇧 English | How do I open a savings account? |

---

## 🚀 Quick Start (Local)

### 1. Clone the repository
```bash
git clone https://github.com/RaNurbekov/ai_voice_assistant.git
cd ai_voice_assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get free Groq API key
Sign up at [console.groq.com](https://console.groq.com) — it's free.

### 4. Create `.env` file
```env
GROQ_API_KEY=your_key_here
```

### 5. Run
```bash
streamlit run app.py
```
> ⚠️ Allow microphone access in your browser on first launch

---

## 📁 Project Structure

```
ai_voice_assistant/
├── app.py              # Full Voice Pipeline: STT → LLM → TTS
├── requirements.txt
├── .env                # API keys (never commit!)
├── .gitignore
└── README.md
```

---

## 🔮 Roadmap

| Feature | Description |
|---|---|
| **RAG Integration** | Connect Qdrant — bot answers strictly from bank documents |
| **ElevenLabs TTS** | Human-quality voice instead of gTTS |
| **WebRTC Streaming** | Real-time streaming without record button |
| **FastAPI Backend** | Separate ML logic from UI for production |

---

## 🔗 Related Projects

Part of a Fintech AI ecosystem:

- [**bank-ai-assistant**](https://github.com/RaNurbekov/llm_bot-ai_bank_assistant-) — Text RAG chatbot (Qdrant + Llama 3)
- [**bank-llm-finetuning**](https://github.com/RaNurbekov/bank_llm_finetuning) — Fine-Tuning LLM (LoRA/PEFT)
- [**pfm-ai-assistant**](https://github.com/RaNurbekov/pfm_ai_assistant) — Personal Finance Manager with Voice Insights

> 💡 **Evolution:** text chat (`bank-ai-assistant`) → voice dialog (this project) → RAG + voice (next step).

---

## 📫 Author

**Rashid Nurbekov** — ML Engineer | Fintech & Generative AI | Almaty, Kazakhstan 🇰🇿

[![Telegram](https://img.shields.io/badge/Telegram-@RaNurbek-2CA5E0?style=flat&logo=telegram&logoColor=white)](https://t.me/RaNurbek)
[![Email](https://img.shields.io/badge/Email-nurbekovrashidjob@gmail.com-D14836?style=flat&logo=gmail&logoColor=white)](mailto:nurbekovrashidjob@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-RaNurbekov-181717?style=flat&logo=github&logoColor=white)](https://github.com/RaNurbekov)
