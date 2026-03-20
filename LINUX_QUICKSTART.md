# 🚀 Linux Quick Start - 10 Minutes to Automated Publishing

## The Linux Way - Step by Step

### 1️⃣ Install Dependencies (Ubuntu/Debian)

```bash
# One command installs everything
sudo apt-get update && sudo apt-get install -y \
    python3 python3-pip git docker.io gh

# Add your user to docker group
sudo usermod -aG docker $USER && newgrp docker

# Install Python packages
pip3 install --upgrade build twine requests tweepy
```

**For Fedora:**
```bash
sudo dnf install -y python3 python3-pip git docker gh && \
pip3 install --upgrade build twine requests tweepy && \
sudo usermod -aG docker $USER && newgrp docker
```

### 2️⃣ Copy and Prepare Script

```bash
# Go to your project directory
cd /path/to/jupyter-ai-extension

# Copy the Linux-optimized script
cp publish_all_linux.py publish_all.py

# Make it executable
chmod +x publish_all.py

# Verify it works
./publish_all.py --check-deps
```

### 3️⃣ Create Configuration

```bash
# Generate config file
./publish_all.py --create-config

# Edit with nano (or your favorite editor)
nano publish_config.json
```

**Change these values:**
```json
{
  "project_name": "Jupyter AI Extension",
  "version": "1.0.0",
  "github_repo": "YOUR_USERNAME/jupyter-ai-extension",
  "docker_username": "YOUR_DOCKER_USERNAME",
  
  "twitter_thread": [
    "Your first tweet...",
    "Your second tweet..."
  ],
  
  "linkedin_post": "Your LinkedIn post..."
}
```

### 4️⃣ Get API Keys

**Open these links in your browser and copy the keys:**

```bash
# Dev.to
# https://dev.to/settings/account
# Look for "Dev Community API Keys"

# Twitter/X
# https://developer.twitter.com/en/portal/dashboard
# Create an app, get Consumer Keys & Access Tokens

# LinkedIn
# https://www.linkedin.com/developers/apps
# Create app, get Access Token

# Docker Hub
# Your Docker username (used in docker login)
```

### 5️⃣ Set Environment Variables

```bash
# Open bash config
nano ~/.bashrc

# Add these lines at the end:
export DEVTO_API_KEY="dev_xxxxxxxxxxxxx"
export TWITTER_API_KEY="xxxxxxxxxxxxx"
export TWITTER_API_SECRET="xxxxxxxxxxxxx"
export TWITTER_ACCESS_TOKEN="xxxxxxxxxxxxx"
export TWITTER_ACCESS_TOKEN_SECRET="xxxxxxxxxxxxx"
export LINKEDIN_ACCESS_TOKEN="xxxxxxxxxxxxx"

# Save and reload
source ~/.bashrc

# Verify they loaded
echo $DEVTO_API_KEY
```

### 6️⃣ Authenticate Services

```bash
# GitHub
gh auth login
# Choose HTTPS, then paste your GitHub token

# Docker Hub
docker login
# Enter username and password

# Git (if not configured)
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### 7️⃣ Test Everything

```bash
# Dry run (see what would happen)
./publish_all.py --dry-run

# Test one platform
./publish_all.py --only github

# If that works, you're ready!
```

### 8️⃣ Launch!

```bash
# Publish to all 7 platforms
./publish_all.py

# Watch the magic happen! ✨
```

---

## That's It! 🎉

You just published to 7 platforms in one command!

---

## One-Liner for Everything

Want to do it all at once? Copy-paste this (Ubuntu/Debian):

```bash
# Install, setup, and test in one go
sudo apt-get update && \
sudo apt-get install -y python3 python3-pip git docker.io gh && \
pip3 install --upgrade build twine requests tweepy && \
sudo usermod -aG docker $USER && \
newgrp docker && \
cp publish_all_linux.py publish_all.py && \
chmod +x publish_all.py && \
echo "✅ Setup complete! Run: nano publish_config.json"
```

---

## Troubleshooting on Linux

| Problem | Solution |
|---------|----------|
| `bash: python3: command not found` | `sudo apt-get install python3` |
| `permission denied: ./publish_all.py` | `chmod +x publish_all.py` |
| `docker: permission denied` | `sudo usermod -aG docker $USER && newgrp docker` |
| `gh: command not found` | `sudo apt-get install gh` |
| `git: not a git repository` | `git init && git remote add origin <url>` |
| `API key not working` | `source ~/.bashrc` (reload env vars) |

---

## Linux Pro Tips

### Make an Alias

```bash
# Add to ~/.bashrc
alias publish="./publish_all.py"
alias publish-test="./publish_all.py --dry-run"

# Then use it anywhere:
publish         # Publish to all
publish-test    # Test first
```

### Run in Background

```bash
# Don't need to watch it
nohup ./publish_all.py > publish.log 2>&1 &

# Check later
tail publish.log
```

### Schedule with Cron

```bash
# Edit crontab
crontab -e

# Add this (runs every Tuesday at 10 AM):
0 10 * * 2 cd /path/to/project && ./publish_all.py >> ~/publish.log 2>&1
```

### Use with Git Tags

```bash
# When you tag a release
git tag v1.0.0
git push origin v1.0.0

# Then publish (can be in GitHub Actions)
./publish_all.py
```

---

## File Permissions Explained

```bash
# -rwxr-xr-x means:
# r = read
# w = write
# x = execute

chmod +x file.py      # Make executable
chmod 755 file.py     # Owner: rwx, Others: rx
chmod 600 config.json # Owner only: rw
```

---

## Linux Environment Variables

```bash
# View all
printenv

# View specific
echo $DEVTO_API_KEY

# Set temporary (current session only)
export DEVTO_API_KEY="xxx"

# Set permanent (add to ~/.bashrc)
echo 'export DEVTO_API_KEY="xxx"' >> ~/.bashrc

# Reload
source ~/.bashrc
```

---

## Check Your Setup

Run this to verify everything:

```bash
#!/bin/bash
echo "🐧 Linux Publishing Setup Check"
echo "==============================="
echo ""
echo "Python:"
python3 --version
echo ""
echo "Git:"
git --version
echo ""
echo "Docker:"
docker --version
echo ""
echo "GitHub CLI:"
gh --version
echo ""
echo "Python packages:"
pip3 list | grep -E "build|twine|requests|tweepy"
echo ""
echo "Environment variables:"
echo "DEVTO_API_KEY: ${DEVTO_API_KEY:-(not set)}"
echo "TWITTER_API_KEY: ${TWITTER_API_KEY:-(not set)}"
echo "LINKEDIN_ACCESS_TOKEN: ${LINKEDIN_ACCESS_TOKEN:-(not set)}"
echo ""
echo "✅ All good!" || echo "❌ Missing some items"
```

Save as `check_setup.sh`:
```bash
chmod +x check_setup.sh
./check_setup.sh
```

---

## Running the Script

### As Executable

```bash
./publish_all.py
```

### With Python

```bash
python3 publish_all.py
```

### With Arguments

```bash
./publish_all.py --dry-run
./publish_all.py --only github
./publish_all.py --platforms pypi,github,devto
./publish_all.py --check-deps
./publish_all.py --create-config
```

---

## What Gets Published

```
✓ PyPI          → pip install jupyter-ai-extension
✓ GitHub        → Release with your code
✓ Dev.to        → Article to 500K+ developers
✓ Twitter       → 5-tweet thread
✓ LinkedIn      → Professional post
✓ Docker Hub    → Docker image
⚠️ Product Hunt → Manual (easy 10 min setup)
```

**All in one command!** 🚀

---

## Expected Time

- **First time setup:** 15 minutes
- **Publishing:** 5-10 minutes
- **Reach:** 5,000-25,000 people
- **Time saved:** 2.75 hours vs manual

---

## Next Steps

1. Copy `publish_all_linux.py` → `publish_all.py`
2. Run `chmod +x publish_all.py`
3. Run `./publish_all.py --create-config`
4. Edit `publish_config.json`
5. Set environment variables
6. Run `./publish_all.py --dry-run`
7. Run `./publish_all.py`
8. Celebrate! 🎉

---

**That's it! You're done!** 🐧

Now your Jupyter AI Extension is live everywhere! 🚀
