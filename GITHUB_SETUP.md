# GitHub Setup & Push Instructions

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `indic-voice-assistant`
3. Description: `Production-ready speech-to-speech chatbot for Kannada, Telugu, and Hindi`
4. Choose: **Public** (for portfolio)
5. **DO NOT** initialize with README (we have one)
6. Click "Create repository"

## Step 2: Initialize Git Locally

Open PowerShell in project root (`c:\Users\Deeps\Desktop\indic-voice-assistant`):

```powershell
# Initialize git repository
git init

# Configure git (one-time setup)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify configuration
git config --global user.name
git config --global user.email
```

## Step 3: Add Files to Git

```powershell
# Add all files
git add .

# Verify files are staged
git status

# You should see:
# - frontend/ folder
# - backend/ folder
# - README.md
# - ARCHITECTURE.md
# - INTERVIEW_GUIDE.md
# - .gitignore
# - LICENSE
# - .gitattributes
```

## Step 4: Create Initial Commit

```powershell
git commit -m "Initial commit: Indic Voice Assistant - Full-stack multilingual chatbot

- React frontend with audio recording and chat UI
- Flask backend with Whisper ASR, Ollama LLM, gTTS TTS
- Support for Kannada, Telugu, Hindi languages
- Production-ready with error handling and logging"
```

## Step 5: Add Remote Repository

Replace `YOUR_USERNAME` with your GitHub username:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/indic-voice-assistant.git

# Verify remote
git remote -v
# Should show:
# origin  https://github.com/YOUR_USERNAME/indic-voice-assistant.git (fetch)
# origin  https://github.com/YOUR_USERNAME/indic-voice-assistant.git (push)
```

## Step 6: Push to GitHub

```powershell
# Push to main branch
git branch -M main
git push -u origin main

# First time will ask for authentication:
# - Use GitHub username
# - Use Personal Access Token (not password)
```

## Step 7: Generate Personal Access Token (if needed)

If authentication fails:

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name: `git-push-token`
4. Expiration: 90 days
5. Scopes: Check `repo` (full control of private repositories)
6. Click "Generate token"
7. Copy token (you won't see it again!)
8. Use token as password when git asks

## Step 8: Verify Push

```powershell
# Check if push was successful
git log --oneline

# Should show your commit
# Should say "On branch main" and "Your branch is up to date with 'origin/main'"
```

## Step 9: Add GitHub Topics (Optional)

On GitHub repository page:
- Click "Add topics"
- Add: `voice-assistant`, `multilingual`, `indic-languages`, `react`, `flask`, `whisper`, `ollama`, `ai`

## Step 10: Add Repository Description

On GitHub repository page:
- Click "Edit" (pencil icon)
- Add description: "Production-ready speech-to-speech chatbot for Kannada, Telugu, and Hindi with React frontend and Flask backend"
- Add website: (if you have one)

---

## Subsequent Commits

After making changes:

```powershell
# Check what changed
git status

# Stage changes
git add .

# Commit with message
git commit -m "Description of changes"

# Push to GitHub
git push
```

## Common Commands

```powershell
# View commit history
git log --oneline

# View changes before committing
git diff

# View staged changes
git diff --staged

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Create new branch
git checkout -b feature-name

# Switch branch
git checkout main

# Merge branch
git merge feature-name

# Delete branch
git branch -d feature-name
```

## Troubleshooting

**Error: "fatal: not a git repository"**
- Run `git init` in project root

**Error: "fatal: 'origin' does not appear to be a 'git' repository"**
- Run `git remote add origin https://github.com/YOUR_USERNAME/indic-voice-assistant.git`

**Error: "Permission denied (publickey)"**
- Use HTTPS instead of SSH
- Or set up SSH keys: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

**Error: "fatal: The current branch main has no upstream branch"**
- Run `git push -u origin main`

**Error: "Updates were rejected because the tip of your current branch is behind"**
- Run `git pull origin main` first, then `git push`

---

## After Pushing to GitHub

1. **Add to Portfolio**: Link to GitHub repo in your resume/portfolio
2. **Create README Badge**: Add build status, language badges
3. **Add Screenshots**: Upload demo screenshots to README
4. **Create Releases**: Tag versions (v1.0.0, v1.1.0, etc.)
5. **Enable GitHub Pages**: Host documentation
6. **Add CI/CD**: GitHub Actions for automated testing

---

## GitHub Profile Tips

- Pin this repository to your profile
- Add to your GitHub bio
- Share on LinkedIn
- Include in interview discussions
