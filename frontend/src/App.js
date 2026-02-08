import React, { useState, useCallback } from 'react';
import { LanguageSelector } from './components/LanguageSelector';
import { MicrophoneButton } from './components/MicrophoneButton';
import { ChatWindow } from './components/ChatWindow';
import { useAudioRecorder } from './hooks/useAudioRecorder';
import { chatAPI } from './services/api';
import './App.css';

function App() {
  const [selectedLanguage, setSelectedLanguage] = useState('kn');
  const [messages, setMessages] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [textInput, setTextInput] = useState('');

  const {
    isRecording,
    audioBlob,
    startRecording,
    stopRecording,
    resetRecording
  } = useAudioRecorder();

  const handleToggleRecording = useCallback(async () => {
    if (isRecording) {
      stopRecording();
    } else {
      try {
        setError(null);
        await startRecording();
      } catch (err) {
        setError('Microphone access denied. Please allow microphone access.');
      }
    }
  }, [isRecording, startRecording, stopRecording]);

  const processAudio = useCallback(async (blob) => {
    setIsProcessing(true);
    setError(null);

    try {
      const response = await chatAPI.sendAudio(blob, selectedLanguage);

      // Add user message
      setMessages(prev => [...prev, {
        role: 'user',
        text: response.transcription,
        language: response.language
      }]);

      // Add assistant message
      setMessages(prev => [...prev, {
        role: 'assistant',
        text: response.response,
        language: response.language,
        audio: response.audio
      }]);

      // Auto-play response
      const audio = new Audio(`data:audio/mp3;base64,${response.audio}`);
      audio.play().catch(err => console.error('Auto-play failed:', err));

    } catch (err) {
      setError(err.response?.data?.error || 'Failed to process audio. Check if backend is running.');
    } finally {
      setIsProcessing(false);
      resetRecording();
    }
  }, [selectedLanguage, resetRecording]);

  const handleTextSubmit = useCallback(async (e) => {
    e.preventDefault();
    if (!textInput.trim() || isProcessing) return;

    setIsProcessing(true);
    setError(null);

    try {
      // Add user message immediately
      setMessages(prev => [...prev, {
        role: 'user',
        text: textInput,
        language: selectedLanguage
      }]);

      const userText = textInput;
      setTextInput('');

      const response = await chatAPI.sendText(userText, selectedLanguage);

      // Add assistant message
      setMessages(prev => [...prev, {
        role: 'assistant',
        text: response.response,
        language: response.language,
        audio: response.audio
      }]);

      // Auto-play response
      const audio = new Audio(`data:audio/mp3;base64,${response.audio}`);
      audio.play().catch(err => console.error('Auto-play failed:', err));

    } catch (err) {
      setError(err.response?.data?.error || 'Failed to process text. Check if backend is running.');
    } finally {
      setIsProcessing(false);
    }
  }, [textInput, selectedLanguage, isProcessing]);

  // Process audio when recording stops
  React.useEffect(() => {
    if (audioBlob && !isRecording) {
      processAudio(audioBlob);
    }
  }, [audioBlob, isRecording, processAudio]);

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎙️ Indic Voice Assistant</h1>
        <p className="subtitle">Speak naturally in your language</p>
      </header>

      <main className="app-main">
        <LanguageSelector
          selectedLanguage={selectedLanguage}
          onLanguageChange={setSelectedLanguage}
        />

        <ChatWindow messages={messages} />

        {error && (
          <div className="error-message" role="alert">
            ⚠️ {error}
          </div>
        )}

        <div className="input-container">
          <form onSubmit={handleTextSubmit} className="text-input-form">
            <input
              type="text"
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              placeholder="Type your message..."
              disabled={isProcessing || isRecording}
              className="text-input"
            />
            <button
              type="submit"
              disabled={!textInput.trim() || isProcessing || isRecording}
              className="send-button"
            >
              📤
            </button>
          </form>

          <div className="divider">
            <span>OR</span>
          </div>

          <MicrophoneButton
            isRecording={isRecording}
            isProcessing={isProcessing}
            onToggle={handleToggleRecording}
            disabled={isProcessing}
          />
        </div>
      </main>

      <footer className="app-footer">
        <p>Powered by Whisper • Ollama • gTTS</p>
      </footer>
    </div>
  );
}

export default App;
