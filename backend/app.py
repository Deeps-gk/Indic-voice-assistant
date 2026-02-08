from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import requests
from gtts import gTTS
import base64
import io
import os
import logging
import tempfile
from functools import lru_cache

# Add ffmpeg to PATH for Windows
ffmpeg_path = r"C:\Users\Deeps\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
if os.path.exists(ffmpeg_path):
    os.environ["PATH"] += os.pathsep + ffmpeg_path
    print(f"Added ffmpeg to PATH: {ffmpeg_path}")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'huihui_ai/hunyuan-mt-abliterated')
WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'tiny')

# Global model instances
whisper_model = None
model_load_error = None

def initialize_models():
    """Initialize ML models on startup"""
    global whisper_model, model_load_error
    try:
        logger.info("="*60)
        logger.info("INITIALIZING MODELS")
        logger.info(f"Loading Whisper model: {WHISPER_MODEL}")
        logger.info(f"Python executable: {os.sys.executable}")
        logger.info(f"Whisper module location: {whisper.__file__}")
        
        whisper_model = whisper.load_model(WHISPER_MODEL)
        
        logger.info("✓ Whisper model loaded successfully")
        logger.info(f"Model type: {type(whisper_model)}")
        logger.info("="*60)
    except Exception as e:
        model_load_error = str(e)
        logger.error("="*60)
        logger.error("❌ WHISPER MODEL LOADING FAILED")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error message: {e}")
        logger.error(f"Full traceback:", exc_info=True)
        logger.error("="*60)

# Initialize models
initialize_models()

# Language-specific system prompts
SYSTEM_PROMPTS = {
    'kn': 'You are a helpful assistant. Respond ONLY in Kannada language. Keep responses concise and natural.',
    'te': 'You are a helpful assistant. Respond ONLY in Telugu language. Keep responses concise and natural.',
    'hi': 'You are a helpful assistant. Respond ONLY in Hindi language. Keep responses concise and natural.'
}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Check Ollama
        ollama_healthy = False
        try:
            response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
            ollama_healthy = response.status_code == 200
        except:
            pass

        return jsonify({
            'status': 'healthy' if whisper_model and ollama_healthy else 'degraded',
            'services': {
                'whisper': whisper_model is not None,
                'ollama': ollama_healthy,
                'tts': True
            },
            'error': model_load_error
        }), 200 if whisper_model and ollama_healthy else 503
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint - processes audio and returns response"""
    try:
        logger.info("\n" + "="*60)
        logger.info("NEW CHAT REQUEST RECEIVED")
        
        # Validate request
        if 'audio' not in request.files:
            logger.error("No audio file in request")
            return jsonify({'error': 'No audio file provided'}), 400
        
        language = request.form.get('language', 'kn')
        logger.info(f"Language: {language}")
        
        if language not in SYSTEM_PROMPTS:
            logger.error(f"Unsupported language: {language}")
            return jsonify({'error': f'Unsupported language: {language}'}), 400

        # Check if models are loaded
        logger.info(f"Whisper model status: {whisper_model is not None}")
        if whisper_model is None:
            logger.error(f"Whisper model is None. Error: {model_load_error}")
            return jsonify({'error': f'Whisper model not loaded. Error: {model_load_error}'}), 503

        audio_file = request.files['audio']
        logger.info(f"Audio file received: {audio_file.filename}, size: {audio_file.content_length} bytes")
        
        # Save audio temporarily (Windows-compatible)
        audio_path = os.path.join(tempfile.gettempdir(), 'input_audio.webm')
        audio_file.save(audio_path)
        logger.info(f"✓ Audio saved: {audio_path}")

        # Step 1: Transcribe audio (ASR)
        logger.info("\n[STEP 1] Starting audio transcription...")
        try:
            logger.info("Calling whisper.transcribe()...")
            transcription_result = whisper_model.transcribe(audio_path, language=language, fp16=False)
            logger.info("✓ Transcription completed")
        except Exception as e:
            logger.error(f"❌ Transcription error: {e}")
            logger.info("Attempting fallback: converting to WAV...")
            # Try loading audio directly from bytes
            audio_file.seek(0)
            audio_bytes = audio_file.read()
            temp_wav = os.path.join(tempfile.gettempdir(), 'input_audio.wav')
            with open(temp_wav, 'wb') as f:
                f.write(audio_bytes)
            logger.info(f"Retrying transcription with WAV file: {temp_wav}")
            transcription_result = whisper_model.transcribe(temp_wav, language=language, fp16=False)
            audio_path = temp_wav
            logger.info("✓ Transcription completed (fallback)")
        
        transcription = transcription_result['text'].strip()
        detected_language = transcription_result.get('language', language)
        logger.info(f"✓ Transcription: '{transcription}'")
        logger.info(f"✓ Detected language: {detected_language}")

        if not transcription:
            return jsonify({'error': 'Could not transcribe audio. Please speak clearly.'}), 400

        # Step 2: Generate LLM response
        logger.info("\n[STEP 2] Generating LLM response...")
        logger.info(f"Ollama URL: {OLLAMA_URL}")
        logger.info(f"Model: {OLLAMA_MODEL}")
        system_prompt = SYSTEM_PROMPTS.get(detected_language, SYSTEM_PROMPTS['kn'])
        full_prompt = f"{system_prompt}\n\nUser: {transcription}\nAssistant:"

        try:
            ollama_response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    'model': OLLAMA_MODEL,
                    'prompt': full_prompt,
                    'stream': False
                },
                timeout=120
            )
            
            if ollama_response.status_code != 200:
                return jsonify({'error': 'Ollama server error. Make sure Ollama is running.'}), 500
            
            response_text = ollama_response.json()['response'].strip()
            logger.info(f"✓ LLM Response: '{response_text[:100]}...'")

        except requests.exceptions.ConnectionError:
            return jsonify({'error': 'Cannot connect to Ollama. Run: ollama serve'}), 500
        except requests.exceptions.Timeout:
            return jsonify({'error': 'Ollama request timeout. Try again.'}), 500

        # Step 3: Generate speech (TTS)
        logger.info("\n[STEP 3] Generating speech (TTS)...")
        tts = gTTS(text=response_text, lang=detected_language, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Convert to base64
        audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode('utf-8')
        logger.info(f"✓ Audio generated, size: {len(audio_base64)} bytes (base64)")

        # Cleanup
        try:
            if os.path.exists(audio_path):
                os.remove(audio_path)
            temp_wav = os.path.join(tempfile.gettempdir(), 'input_audio.wav')
            if os.path.exists(temp_wav):
                os.remove(temp_wav)
        except:
            pass

        logger.info("\n✅ REQUEST COMPLETED SUCCESSFULLY")
        logger.info("="*60 + "\n")
        return jsonify({
            'transcription': transcription,
            'response': response_text,
            'audio': audio_base64,
            'language': detected_language
        }), 200

    except Exception as e:
        logger.error("\n" + "="*60)
        logger.error("❌ REQUEST FAILED")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error message: {e}")
        logger.error("Full traceback:", exc_info=True)
        logger.error("="*60 + "\n")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/chat/text', methods=['POST'])
def chat_text():
    """Text chat endpoint - processes text and returns response with audio"""
    try:
        logger.info("\n" + "="*60)
        logger.info("NEW TEXT CHAT REQUEST RECEIVED")
        
        
        data = request.get_json()
        text = data.get('text', '').strip()
        language = data.get('language', 'kn')
        
        logger.info(f"Text: '{text}'")
        logger.info(f"Language: {language}")
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        if language not in SYSTEM_PROMPTS:
            return jsonify({'error': f'Unsupported language: {language}'}), 400

        # Generate LLM response
        logger.info("\n[STEP 1] Generating LLM response...")
        system_prompt = SYSTEM_PROMPTS.get(language, SYSTEM_PROMPTS['kn'])
        full_prompt = f"{system_prompt}\n\nUser: {text}\nAssistant:"

        try:
            ollama_response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    'model': OLLAMA_MODEL,
                    'prompt': full_prompt,
                    'stream': False
                },
                timeout=120
            )
            
            if ollama_response.status_code != 200:
                return jsonify({'error': 'Ollama server error. Make sure Ollama is running.'}), 500
            
            response_text = ollama_response.json()['response'].strip()
            logger.info(f"✓ LLM Response: '{response_text[:100]}...'")

        except requests.exceptions.ConnectionError:
            return jsonify({'error': 'Cannot connect to Ollama. Run: ollama serve'}), 500
        except requests.exceptions.Timeout:
            return jsonify({'error': 'Ollama request timeout. Try again.'}), 500

        # Generate speech (TTS)
        logger.info("\n[STEP 2] Generating speech (TTS)...")
        tts = gTTS(text=response_text, lang=language, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Convert to base64
        audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode('utf-8')
        logger.info(f"✓ Audio generated, size: {len(audio_base64)} bytes (base64)")

        logger.info("\n✅ REQUEST COMPLETED SUCCESSFULLY")
        logger.info("="*60 + "\n")
        return jsonify({
            'response': response_text,
            'audio': audio_base64,
            'language': language
        }), 200

    except Exception as e:
        logger.error("\n" + "="*60)
        logger.error("❌ REQUEST FAILED")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error message: {e}")
        logger.error("Full traceback:", exc_info=True)
        logger.error("="*60 + "\n")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'Audio file too large. Maximum size: 16MB'}), 413

@app.errorhandler(500)
def internal_server_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("="*60)
    logger.info("Starting Indic Voice Assistant Backend")
    logger.info(f"Ollama URL: {OLLAMA_URL}")
    logger.info(f"Ollama Model: {OLLAMA_MODEL}")
    logger.info(f"Whisper Model: {WHISPER_MODEL}")
    logger.info("="*60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
