import React, { useRef, useEffect } from 'react';
import './ChatWindow.css';

export const ChatWindow = ({ messages }) => {
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const playAudio = (audioBase64) => {
    const audio = new Audio(`data:audio/mp3;base64,${audioBase64}`);
    audio.play().catch(err => console.error('Audio playback failed:', err));
  };

  return (
    <div className="chat-window">
      {messages.length === 0 ? (
        <div className="empty-state">
          <p>Start a conversation by clicking the microphone</p>
        </div>
      ) : (
        messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <div className="message-header">
              <span className="message-role">
                {msg.role === 'user' ? '👤 You' : '🤖 Assistant'}
              </span>
              <span className="message-language">{msg.language.toUpperCase()}</span>
            </div>
            <div className="message-content">{msg.text}</div>
            {msg.audio && msg.role === 'assistant' && (
              <button
                className="audio-replay-btn"
                onClick={() => playAudio(msg.audio)}
                aria-label="Replay audio"
              >
                🔊 Replay
              </button>
            )}
          </div>
        ))
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};
