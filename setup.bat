@echo off
echo ========================================
echo Indic Voice Assistant - Setup
echo ========================================
echo.

echo [1/3] Setting up Backend...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
cd ..

echo.
echo [2/3] Setting up Frontend...
cd frontend
call npm install
cd ..

echo.
echo [3/3] Checking Ollama...
curl http://localhost:11434/api/tags
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Ollama not running!
    echo Please run: ollama serve
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the application:
echo   Terminal 1: ollama serve
echo   Terminal 2: cd backend ^&^& venv\Scripts\activate ^&^& python app.py
echo   Terminal 3: cd frontend ^&^& npm start
echo.
pause
