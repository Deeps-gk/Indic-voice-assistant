import React from 'react';
import './LanguageSelector.css';

const LANGUAGES = [
  { code: 'kn', name: 'ಕನ್ನಡ', label: 'Kannada' },
  { code: 'te', name: 'తెలుగు', label: 'Telugu' },
  { code: 'hi', name: 'हिंदी', label: 'Hindi' }
];

export const LanguageSelector = ({ selectedLanguage, onLanguageChange }) => {
  return (
    <div className="language-selector">
      <label htmlFor="language-select" className="language-label">
        Select Language
      </label>
      <select
        id="language-select"
        value={selectedLanguage}
        onChange={(e) => onLanguageChange(e.target.value)}
        className="language-dropdown"
      >
        {LANGUAGES.map(lang => (
          <option key={lang.code} value={lang.code}>
            {lang.name} ({lang.label})
          </option>
        ))}
      </select>
    </div>
  );
};
