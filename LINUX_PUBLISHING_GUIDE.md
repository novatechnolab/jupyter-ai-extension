# 🐧 Linux Automated Publishing Guide

## Quick Setup (5 Minutes on Linux)

### Step 1: Copy the Script

```bash
# Copy the Linux-optimized script to your project
cp publish_all_linux.py your-project/publish_all.py

# Make it executable
chmod +x your-project/publish_all.py
```

### Step 2: Check Dependencies

```bash
cd your-project

# Check system dependencies
python3 publish_all.py --check-deps

# Or manually check:
git --version
docker --version
gh --version
python3 --version
```

### Step 3: Install Missing Tools (if needed)

**For Ubuntu/Debian:**
```bash
# Update package lists
sudo apt-get update

# Install tools
sudo apt-get install -y \
    python3 \
    python3-pip \
    git \
    docker.io \
    gh

# Add your user to docker group (so you don't need sudo)
sudo usermod -aG docker $USER

# Apply new group membership (restart may be needed)
newgrp docker
```

**For Fedora:**
```bash
sudo dnf install -y \
    python3 \
    python3-pip \
    git \
    docker \
    gh

sudo usermod -aG docker $USER
newgrp docker
```

**For Arch Linux:**
```bash
sudo pacman -S \
    python \
    python-pip \
    git \
    docker \
    github-cli

sudo usermod -aG docker $USER
newgrp docker
```

### Step 4: Install Python Dependencies

```bash
# Install required Python packages
pip3 install --upgrade \
    build \
    twine \
    requests \
    tweepy
```

### Step 5: Create Configuration

```bash
# Generate config file
python3 publish_all.py --create-config

# Edit with your details
nano publish_config.json
```

Update these fields:
- `project_name`
- `version`
- `github_repo`
- `docker_username`
- `twitter_thread`
- `linkedin_post`

### Step 6: Set Environment Variables

```bash
# Open your shell config file
nano ~/.bashrc  # or ~/.zshrc if using zsh

# Add these lines at the end:
export DEVTO_API_KEY="your_key_from_dev_to"
export TWITTER_API_KEY="your_twitter_key"
export TWITTER_API_SECRET="your_twitter_secret"
export TWITTER_ACCESS_TOKEN="your_twitter_token"
export TWITTER_ACCESS_TOKEN_SECRET="your_twitter_token_secret"
export LINKEDIN_ACCESS_TOKEN="your_linkedin_token"

# Save and reload
source ~/.bashrc  # or source ~/.zshrc
```

### Step 7: Authenticate with Services

```bash
# GitHub CLI
gh auth login

# Docker Hub
docker login

# Git (if not already configured)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 8: Test and Publish

```bash
# Test without publishing (dry run)
python3 publish_all.py --dry-run

# Test single platform
python3 publish_all.py --only github

# Publish to all platforms
python3 publish_all.py
```

---

## Running the Script

### Basic Usage

```bash
# Make executable (one time)
chmod +x publish_all.py

# Publish to all platforms
./publish_all.py

# Or use python3 directly
python3 publish_all.py
```

### Advanced Usage

```bash
# Check dependencies
python3 publish_all.py --check-deps

# Create config
python3 publish_all.py --create-config

# Test without publishing
python3 publish_all.py --dry-run

# Publish to specific platforms
python3 publish_all.py --platforms pypi,github,devto

# Publish to only one platform (for testing)
python3 publish_all.py --only github

# Verbose output
python3 publish_all.py --verbose

# Custom config file
python3 publish_all.py --config my_config.json
```

---

## Linux-Specific Features

### Automatic Dependency Checking

The script automatically checks for required tools:
- ✅ Git
- ✅ Docker
- ✅ GitHub CLI
- ✅ Python 3.8+

If tools are missing, it provides installation instructions.

### Docker Daemon Management

The script checks if Docker daemon is running:
```bash
# If Docker is not running
sudo systemctl start docker

# To start Docker on login
sudo systemctl enable docker
```

### File Permissions

The script respects Linux file permissions:
```bash
# Make script executable
chmod +x publish_all.py

# Run it
./publish_all.py
```

### Git Configuration

Linux-friendly git setup:
```bash
# Global config
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Per-repo config
git config user.name "Your Name"
git config user.email "your@email.com"
```

---

## Troubleshooting on Linux

### "Permission Denied" When Running Script

```bash
# Make the script executable
chmod +x publish_all.py

# Then run it
./publish_all.py
```

### "Python3 Not Found"

```bash
# Check Python installation
which python3
python3 --version

# Install Python3
sudo apt-get install python3 python3-pip
```

### "Docker Daemon Not Running"

```bash
# Start Docker daemon
sudo systemctl start docker

# Make it start on boot
sudo systemctl enable docker

# Or start it in background
sudo dockerd &
```

### "Permission Denied" for Docker

```bash
# Add your user to docker group
sudo usermod -aG docker $USER

# Apply group changes
newgrp docker

# Verify
docker ps
```

### "Git Not Configured"

```bash
# Configure git globally
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Verify
git config --global --list
```

### "gh CLI Not Authenticated"

```bash
# Authenticate
gh auth login

# Choose HTTPS protocol when prompted

# Verify
gh auth status
```

### "API Keys Not Working"

```bash
# Verify environment variables are set
echo $DEVTO_API_KEY
echo $TWITTER_API_KEY

# If empty, re-source your shell config
source ~/.bashrc
source ~/.zshrc

# Verify again
echo $DEVTO_API_KEY
```

### "Module Not Found" (Python)

```bash
# Install missing Python modules
pip3 install requests tweepy

# Or upgrade all dependencies
pip3 install --upgrade build twine requests tweepy
```

---

## Complete Setup Script

Save this as `setup_publishing.sh`:

```bash
#!/bin/bash
set -e

echo "🐧 Setting up Jupyter AI Extension Publishing on Linux"
echo "======================================================"

# Detect Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "Cannot detect Linux distribution"
    exit 1
fi

echo "📍 Detected: $OS"

# Install dependencies based on distro
case $OS in
    ubuntu|debian)
        echo "📦 Installing dependencies for Ubuntu/Debian..."
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip git docker.io gh
        ;;
    fedora)
        echo "📦 Installing dependencies for Fedora..."
        sudo dnf install -y python3 python3-pip git docker gh
        ;;
    arch)
        echo "📦 Installing dependencies for Arch..."
        sudo pacman -S --noconfirm python python-pip git docker github-cli
        ;;
    *)
        echo "⚠️  Unsupported distribution. Please install manually:"
        echo "   - Python 3.8+"
        echo "   - pip"
        echo "   - git"
        echo "   - docker"
        echo "   - gh CLI"
        exit 1
        ;;
esac

# Add user to docker group
echo "🐳 Configuring Docker..."
sudo usermod -aG docker $USER
newgrp docker

# Install Python packages
echo "🐍 Installing Python packages..."
pip3 install --upgrade build twine requests tweepy

# Configure git if needed
echo "📝 Configuring Git..."
if [ -z "$(git config --global user.name)" ]; then
    read -p "Enter your name for git: " git_name
    git config --global user.name "$git_name"
fi

if [ -z "$(git config --global user.email)" ]; then
    read -p "Enter your email for git: " git_email
    git config --global user.email "$git_email"
fi

# Create publishing script
echo "📄 Creating publishing script..."
cat > publish_all.py << 'SCRIPT_EOF'
#!/usr/bin/env python3
# [Script content would go here - same as publish_all_linux.py]
SCRIPT_EOF

chmod +x publish_all.py

# Create config
echo "⚙️  Creating configuration..."
python3 publish_all.py --create-config

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit publish_config.json:"
echo "   nano publish_config.json"
echo ""
echo "2. Get API keys from:"
echo "   - Dev.to: https://dev.to/settings/account"
echo "   - Twitter: https://developer.twitter.com/"
echo "   - LinkedIn: https://linkedin.com/developers/apps"
echo ""
echo "3. Set environment variables:"
echo "   nano ~/.bashrc"
echo "   [Add: export DEVTO_API_KEY='...']"
echo "   source ~/.bashrc"
echo ""
echo "4. Test and publish:"
echo "   python3 publish_all.py --dry-run"
echo "   python3 publish_all.py"
```

Make it executable and run:
```bash
chmod +x setup_publishing.sh
./setup_publishing.sh
```

---

## Environment Variables Management

### Permanent Setup

Add to `~/.bashrc` (or `~/.zshrc` for Zsh):

```bash
# Jupyter AI Extension Publishing Keys
export DEVTO_API_KEY="dev_xxxxxxxxxxxxxxxx"
export TWITTER_API_KEY="xxxxxxxxxxxxxxxx"
export TWITTER_API_SECRET="xxxxxxxxxxxxxxxx"
export TWITTER_ACCESS_TOKEN="xxxxxxxxxxxxxxxx"
export TWITTER_ACCESS_TOKEN_SECRET="xxxxxxxxxxxxxxxx"
export LINKEDIN_ACCESS_TOKEN="xxxxxxxxxxxxxxxx"
```

Then reload:
```bash
source ~/.bashrc
```

### Temporary Setup

For current terminal session only:
```bash
export DEVTO_API_KEY="your_key"
export TWITTER_API_KEY="your_key"
# ... etc
```

### Using .env File

Create `.env` file:
```
DEVTO_API_KEY=your_key
TWITTER_API_KEY=your_key
# ... etc
```

Load it before running:
```bash
source .env
python3 publish_all.py
```

---

## Cron Job for Automated Publishing

Schedule publishing for automatic release days:

```bash
# Edit crontab
crontab -e

# Add this line (publishes every Tuesday at 10 AM)
0 10 * * 2 cd /path/to/your/project && /path/to/publish_all.py

# Or for scheduled releases (first Tuesday of each month)
0 10 1-7 * 2 [ $(date +\%u) = 3 ] && cd /path/to/project && /path/to/publish_all.py
```

---

## GitHub Actions for CI/CD

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to All Platforms

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine requests tweepy
      
      - name: Configure Git
        run: |
          git config --global user.name "GitHub Actions"
          git config --global user.email "actions@github.com"
      
      - name: Publish
        env:
          DEVTO_API_KEY: ${{ secrets.DEVTO_API_KEY }}
          TWITTER_API_KEY: ${{ secrets.TWITTER_API_KEY }}
          TWITTER_API_SECRET: ${{ secrets.TWITTER_API_SECRET }}
          TWITTER_ACCESS_TOKEN: ${{ secrets.TWITTER_ACCESS_TOKEN }}
          TWITTER_ACCESS_TOKEN_SECRET: ${{ secrets.TWITTER_ACCESS_TOKEN_SECRET }}
          LINKEDIN_ACCESS_TOKEN: ${{ secrets.LINKEDIN_ACCESS_TOKEN }}
        run: python3 publish_all.py
```

---

## Quick Reference Commands

```bash
# Check dependencies
python3 publish_all.py --check-deps

# Create config
python3 publish_all.py --create-config

# Test without publishing
python3 publish_all.py --dry-run

# Test single platform
python3 publish_all.py --only pypi

# Publish to specific platforms
python3 publish_all.py --platforms pypi,github,devto

# Publish to all
python3 publish_all.py

# Reload shell config
source ~/.bashrc

# Check environment variables
printenv | grep DEVTO

# View git config
git config --global --list

# Check Docker status
docker ps

# Start Docker if not running
sudo systemctl start docker

# Authenticate with GitHub
gh auth login
```

---

## Linux-Specific Tips

### Use Aliases

Add to `.bashrc`:
```bash
alias publish="python3 publish_all.py"
alias publish-test="python3 publish_all.py --dry-run"
alias publish-github="python3 publish_all.py --only github"
```

Then use:
```bash
publish           # Publish to all
publish-test      # Test first
publish-github    # Just GitHub
```

### Background Execution

```bash
# Run in background
nohup python3 publish_all.py &

# Check background jobs
jobs

# Disown a job (so it survives terminal close)
disown %1
```

### Redirect Output to Log File

```bash
# Save output to file
python3 publish_all.py > publish.log 2>&1

# View log
tail -f publish.log

# Email yourself when done
python3 publish_all.py && mail -s "Publishing complete" you@example.com < /dev/null
```

### Monitor with Systemd

Create `/etc/systemd/system/publish-ai-ext.service`:

```ini
[Unit]
Description=Publish Jupyter AI Extension
After=network.target

[Service]
Type=oneshot
User=$USER
WorkingDirectory=/path/to/project
ExecStart=/path/to/publish_all.py

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable publish-ai-ext.service
```

---

## Success Checklist

- [ ] `chmod +x publish_all.py` - Script is executable
- [ ] `python3 publish_all.py --check-deps` - All dependencies installed
- [ ] `python3 publish_all.py --create-config` - Config created
- [ ] `nano publish_config.json` - Config edited with your details
- [ ] API keys added to `~/.bashrc` - Environment variables set
- [ ] `source ~/.bashrc` - Variables loaded
- [ ] `python3 publish_all.py --dry-run` - Dry run successful
- [ ] `python3 publish_all.py --only pypi` - Single platform test
- [ ] `python3 publish_all.py` - Full publishing successful!

---

## Next Steps

1. Run `./publish_all.py --check-deps`
2. Install any missing dependencies
3. Run `./publish_all.py --create-config`
4. Edit `publish_config.json`
5. Set environment variables
6. Run `./publish_all.py --dry-run`
7. Run `./publish_all.py` to publish!

---

**Happy publishing on Linux!** 🐧🚀
