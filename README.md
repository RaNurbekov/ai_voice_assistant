# 🎙️ Voice Bank Assistant (STT → LLM → TTS)

> **Полноценный голосовой AI-ассистент банка с памятью диалога**
> Whisper v3 (распознавание) → Llama 3 (генерация) → gTTS (синтез речи)

---

## 🛠 Стек технологий

| Компонент | Технология |
|---|---|
| **Speech-to-Text (STT)** | OpenAI Whisper Large v3 (через Groq API) |
| **LLM Engine** | Llama 3.3-70B (через Groq API) |
| **Text-to-Speech (TTS)** | Google TTS (`gTTS`) |
| **Conversation Memory** | Streamlit `session_state` |
| **Frontend** | Streamlit (`st.audio_input`, `st.audio` autoplay) |

---

## ⚙️ Архитектура Voice Pipeline

```
🎤 Микрофон (браузер)
        │
        ▼
┌─────────────────────────────┐
│   ШАГ А: УШИ (Whisper)     │
│                             │
│  Whisper Large v3 (Groq)   │
│  wav/mp3 → текст            │
│  Фильтрация шумов и акцентов│
└──────────────┬──────────────┘
               │ user_text
               ▼
┌─────────────────────────────┐
│   ШАГ Б: МОЗГ (Llama 3)   │
│                             │
│  System Prompt (роль банкира│
│  Kaspi)                     │
│  + ВСЯ история диалога      │
│  → Llama 3.3-70B (Groq)    │
│  temperature=0.3            │
└──────────────┬──────────────┘
               │ bot_text
               ▼
┌─────────────────────────────┐
│   ШАГ В: ГОЛОС (gTTS)      │
│                             │
│  text → response.mp3        │
│  st.audio(autoplay=True)    │
│  Автовоспроизведение в      │
│  браузере                   │
└─────────────────────────────┘
```

---

## 🔑 Ключевые особенности

### 1. Полная история диалога в каждом запросе
Каждый запрос к Llama 3 содержит **всю историю** разговора через `st.session_state` — бот помнит имя клиента, предыдущие вопросы и контекст беседы:

```python
ai_messages = [{"role": "system", "content": system_prompt}]
for msg in st.session_state.messages:
    ai_messages.append({"role": msg["role"], "content": msg["content"]})
```

### 2. System Prompt оптимизирован под голос
Промпт специально настроен для TTS-сценария — бот отвечает кратко, без списков и таблиц, как живой оператор по телефону:

```python
system_prompt = (
    "Ты — дружелюбный голосовой ассистент банка Kaspi. "
    "Отвечай КРАТКО и по-человечески, так как твой текст будет озвучиваться голосом. "
    "Не используй списки, звёздочки или таблицы. Говори как живой собеседник по телефону."
)
```

### 3. Whisper с банковским контекстом
Транскрибация настроена с доменным промптом для лучшего распознавания банковских терминов:

```python
transcription = client.audio.transcriptions.create(
    file=("audio.wav", audio_bytes.read()),
    model="whisper-large-v3",
    prompt="Это диалог клиента с банком на русском языке.",
)
```

---

## 🚀 Быстрый старт

### 1. Настройка ключей
Получите бесплатный API ключ на [console.groq.com](https://console.groq.com/).
Создайте файл `.env` в корне проекта:

```env
GROQ_API_KEY=ваш_ключ
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Запуск
```bash
streamlit run app.py
```
> ⚠️ Разрешите браузеру доступ к микрофону при первом запуске

---

## 📁 Структура проекта

```
voice-bank-assistant/
├── app.py              # Полный Voice Pipeline: STT → LLM → TTS
├── requirements.txt    # Зависимости
├── .env                # API ключи (не коммитить!)
├── .gitignore
└── README.md
```

---

## 🔮 Возможные улучшения

| Улучшение | Эффект |
|---|---|
| **ElevenLabs вместо gTTS** | Человеческий голос вместо роботизированного |
| **RAG + Qdrant** | Бот отвечает по реальным документам банка |
| **WebRTC (реальный стриминг)** | Устранение задержки записи через кнопку |
| **FastAPI бэкенд** | Отделение логики от UI для production |

---

## 🔗 Связанные проекты

- [**bank-ai-assistant**](https://github.com/RaNurbekov/llm_bot-ai_bank_assistant-) — текстовый RAG-бот (Qdrant + Llama 3)
- [**bank-llm-finetuning**](https://github.com/RaNurbekov/bank_llm_finetuning) — Fine-Tuning LLM (LoRA/PEFT)

> 💡 **Эволюция:** текстовый чат (`bank-ai-assistant`) → голосовой диалог (этот проект). Следующий шаг — интеграция RAG в голосовой пайплайн для ответов строго по документам банка.
