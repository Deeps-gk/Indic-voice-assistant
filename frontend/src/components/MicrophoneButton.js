import React from 'react';
import './MicrophoneButton.css';

export const MicrophoneButton = ({ isRecording, isProcessing, onToggle, disabled }) => {
  const getButtonClass = () => {
    if (isProcessing) return 'mic-button processing';
    if (isRecording) return 'mic-button recording';
    return 'mic-button';
  };

  const getStatusText = () => {
    if (isProcessing) return 'Processing...';
    if (isRecording) return 'Recording... Click to stop';
    return 'Click to speak';
  };

  return (
    <div className="mic-container">
      <button
        className={getButtonClass()}
        onClick={onToggle}
        disabled={disabled || isProcessing}
        aria-label={isRecording ? 'Stop recording' : 'Start recording'}
      >
        <svg className="mic-icon" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
          <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
        </svg>
      </button>
      <p className="mic-status">{getStatusText()}</p>
    </div>
  );
};
