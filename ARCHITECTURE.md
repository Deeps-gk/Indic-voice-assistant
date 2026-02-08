# Indic Voice Assistant - Architecture & Design

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Language    │  │  Microphone  │  │  Chat        │      │
│  │  Selector    │  │  Recorder    │  │  Interface   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                            │                                 │
│                    REST API (JSON)                           │
│                            │                                 │
└────────────────────────────┼─────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (Python/Flask)                    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Layer (Flask Routes)                            │  │
│  └──────────────────────────────────────────────────────┘  │
│                            │                                 │
│         ┌──────────────────┼──────────────────┐             │
│         ▼                  ▼                  ▼             │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐         │
│  │   ASR    │      │   LLM    │      │   TTS    │         │
│  │ (Whisper)│      │ (Ollama) │      │  (gTTS)  │         │
│  └──────────┘      └──────────┘      └──────────┘         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Request Flow

1. **User speaks** → Frontend captures audio via MediaRecorder API
2. **Audio sent** → POST /api/chat with audio blob + language
3. **Backend processes**:
   - Whisper transcribes audio → text
   - Ollama (llama3) generates response → text
   - gTTS converts response → audio
4. **Response returned** → JSON with transcription, response text, audio base64
5. **Frontend displays** → Shows text + plays audio

## API Contract

### POST /api/chat
**Request:**
```json
{
  "audio": "base64_encoded_audio_blob",
  "language": "kn" | "te" | "hi"
}
```

**Response:**
```json
{
  "transcription": "ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?",
  "response": "ನಾನು ಚೆನ್ನಾಗಿದ್ದೇನೆ, ಧನ್ಯವಾದಗಳು!",
  "audio": "base64_encoded_audio_response",
  "language": "kn"
}
```

### GET /api/health
**Response:**
```json
{
  "status": "healthy",
  "services": {
    "whisper": true,
    "ollama": true,
    "tts": true
  }
}
```

## Design Decisions

### 1. **Why React Functional Components?**
- Modern, hooks-based approach
- Better performance with memoization
- Easier state management
- Industry standard

### 2. **Why MediaRecorder API?**
- Native browser support
- No external dependencies
- Works on mobile browsers
- Low bandwidth (compressed audio)

### 3. **Why Whisper for ASR?**
- Best open-source ASR
- Excellent Indic language support
- Runs locally (privacy)
- Free and open-source

### 4. **Why Ollama + llama3?**
- Local LLM execution
- No API costs
- Privacy-first
- Good multilingual support

### 5. **Why gTTS for TTS?**
- Simple, no C++ dependencies
- Supports Kannada, Telugu, Hindi
- Good voice quality
- Easy to install

### 6. **Base64 Audio Transfer?**
- Simple JSON API
- No file storage needed
- Works with any frontend
- Easy to debug

## Performance Optimizations

1. **Audio Compression**: Use WebM/Opus format (smaller size)
2. **Lazy Loading**: Load models on first request
3. **Caching**: Cache TTS responses for common phrases
4. **Streaming**: Future enhancement for real-time responses
5. **CDN**: Serve static assets from CDN

## Scalability Considerations

1. **Horizontal Scaling**: Stateless API, can add more servers
2. **Load Balancing**: Nginx/HAProxy for traffic distribution
3. **Queue System**: Redis/Celery for async processing
4. **Model Optimization**: Use quantized models for faster inference
5. **Database**: Add PostgreSQL for conversation history

## Security

1. **Rate Limiting**: Prevent abuse (10 requests/minute)
2. **Input Validation**: Validate audio size, format, language
3. **CORS**: Restrict origins in production
4. **HTTPS**: Encrypt data in transit
5. **Sanitization**: Clean user inputs before LLM

## Low-Bandwidth Optimizations

1. **Audio Compression**: WebM Opus codec (10x smaller than WAV)
2. **Progressive Loading**: Show transcription before audio
3. **Offline Mode**: Cache responses locally
4. **Adaptive Quality**: Lower TTS quality on slow networks
5. **Text-First**: Always show text, audio optional

## Accessibility

1. **Keyboard Navigation**: Full keyboard support
2. **Screen Reader**: ARIA labels for all controls
3. **Visual Feedback**: Clear recording/processing states
4. **Error Messages**: Clear, actionable error messages
5. **Language Icons**: Visual language indicators

## Tech Stack Summary

| Layer | Technology | Why? |
|-------|-----------|------|
| Frontend | React 18 | Modern, performant, popular |
| State | React Hooks | Simple, no Redux needed |
| Audio | MediaRecorder | Native, no dependencies |
| Backend | Flask | Lightweight, Python ecosystem |
| ASR | Whisper | Best open-source ASR |
| LLM | Ollama/llama3 | Local, free, multilingual |
| TTS | gTTS | Simple, Indic support |
| API | REST/JSON | Simple, universal |

## Interview Talking Points

1. **Separation of Concerns**: Clear frontend/backend split
2. **Stateless Design**: Easy to scale horizontally
3. **Open Source**: No vendor lock-in, cost-effective
4. **Privacy-First**: All processing local, no data sent to cloud
5. **Progressive Enhancement**: Works without audio, text fallback
6. **Mobile-First**: Responsive, touch-friendly
7. **Error Handling**: Graceful degradation at every layer
8. **Testing**: Unit tests for components, integration tests for API
9. **Monitoring**: Health checks, logging, metrics
10. **Documentation**: Clear API docs, code comments
