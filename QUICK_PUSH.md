# Quick GitHub Push (Copy-Paste Commands)

## One-Time Setup

```powershell
# Navigate to project
cd c:\Users\Deeps\Desktop\indic-voice-assistant

# Initialize git
git init

# Configure git (replace with your info)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Add all files
git add .

# Create commit
git commit -m "Initial commit: Indic Voice Assistant - Multilingual speech-to-speech chatbot"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/indic-voice-assistant.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## After First Push

```powershell
# Make changes, then:
git add .
git commit -m "Your commit message"
git push
```

## Verify Success

```powershell
# Check status
git status

# Should show: "On branch main" and "Your branch is up to date with 'origin/main'"
```

---

## Steps to Create GitHub Repo

1. Go to https://github.com/new
2. Name: `indic-voice-assistant`
3. Description: `Production-ready speech-to-speech chatbot for Kannada, Telugu, Hindi`
4. Public
5. Don't initialize with README
6. Create repository
7. Copy the HTTPS URL
8. Use in `git remote add origin` command above

---

## If You Get Authentication Error

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: `git-token`
4. Check `repo` scope
5. Generate and copy token
6. Use token as password when git asks

---

## Done! 🎉

Your project is now on GitHub!
