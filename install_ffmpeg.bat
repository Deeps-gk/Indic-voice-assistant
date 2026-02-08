@echo off
echo Installing FFmpeg for Windows...
echo.

REM Check if winget is available
winget --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Using winget to install FFmpeg...
    winget install --id=Gyan.FFmpeg -e
    goto :done
)

REM Check if choco is available
choco --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Using Chocolatey to install FFmpeg...
    choco install ffmpeg -y
    goto :done
)

echo.
echo ========================================
echo MANUAL INSTALLATION REQUIRED
echo ========================================
echo.
echo Please install FFmpeg manually:
echo 1. Download from: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
echo 2. Extract to C:\ffmpeg
echo 3. Add C:\ffmpeg\bin to your PATH
echo.
echo OR install Chocolatey first:
echo    https://chocolatey.org/install
echo    Then run: choco install ffmpeg
echo.
pause
exit /b 1

:done
echo.
echo ========================================
echo FFmpeg installed successfully!
echo ========================================
echo.
echo Please RESTART your terminal and run:
echo    python app.py
echo.
pause
