import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export const chatAPI = {
  async sendAudio(audioBlob, language) {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.webm');
    formData.append('language', language);

    const response = await axios.post(`${API_BASE_URL}/api/chat`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 400000  // 2 minutes for Ollama response
    });

    return response.data;
  },

  async sendText(text, language) {
    const response = await axios.post(`${API_BASE_URL}/api/chat/text`, {
      text,
      language
    }, {
      timeout: 120000
    });

    return response.data;
  },

  async checkHealth() {
    const response = await axios.get(`${API_BASE_URL}/api/health`);
    return response.data;
  }
};
