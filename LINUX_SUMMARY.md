# 🐧 Linux Automated Publishing - Complete Summary

## What You Have for Linux

I've created **3 Linux-optimized files** specifically for you:

### 1. **publish_all_linux.py** - Main Script
- Linux-optimized automated publishing script
- Automatic dependency checking
- Perfect error handling for Linux environments
- Can run as `./publish_all.py` after `chmod +x`

### 2. **LINUX_QUICKSTART.md** - 10-Minute Setup
- Copy-paste friendly commands for Linux
- Works on Ubuntu, Fedora, Arch, and other Linux distros
- Step-by-step with expected output

### 3. **LINUX_PUBLISHING_GUIDE.md** - Complete Reference
- Comprehensive Linux guide
- Troubleshooting specific to Linux
- Systemd, cron, aliases, and more
- CI/CD with GitHub Actions

---

## The Linux Way - 3 Steps

### Step 1: One Command to Install Everything

**Ubuntu/Debian:**
```bash
sudo apt-get update && sudo apt-get install -y \
    python3 python3-pip git docker.io gh && \
pip3 install --upgrade build twine requests tweepy && \
sudo usermod -aG docker $USER && newgrp docker
```

**Fedora:**
```bash
sudo dnf install -y python3 python3-pip git docker gh && \
pip3 install --upgrade build twine requests tweepy && \
sudo usermod -aG docker $USER && newgrp docker
```

**Arch:**
```bash
sudo pacman -S --noconfirm python python-pip git docker github-cli && \
pip install --upgrade build twine requests tweepy && \
sudo usermod -aG docker $USER && newgrp docker
```

### Step 2: Setup (5 minutes)

```bash
# Copy script
cp publish_all_linux.py publish_all.py
chmod +x publish_all.py

# Create config
./publish_all.py --create-config
nano publish_config.json  # Edit your details

# Set environment variables
nano ~/.bashrc
# Add: export DEVTO_API_KEY="..."
source ~/.bashrc

# Authenticate
gh auth login
docker login
```

### Step 3: Publish!

```bash
# Test first
./publish_all.py --dry-run

# Then publish
./publish_all.py
```

**Done!** 🎉

---

## Quick Reference

### Essential Commands

```bash
# Check dependencies
./publish_all.py --check-deps

# Create config
./publish_all.py --create-config

# Dry run (test)
./publish_all.py --dry-run

# Publish to all
./publish_all.py

# Publish to specific
./publish_all.py --platforms pypi,github,devto

# Test one platform
./publish_all.py --only github
```

### File Permissions

```bash
# Make executable
chmod +x publish_all.py

# Verify
ls -l publish_all.py
# Should show: -rwxr-xr-x
```

### Environment Variables

```bash
# Add to ~/.bashrc
export DEVTO_API_KEY="dev_xxxxx"
export TWITTER_API_KEY="xxxxx"
export TWITTER_API_SECRET="xxxxx"
export TWITTER_ACCESS_TOKEN="xxxxx"
export TWITTER_ACCESS_TOKEN_SECRET="xxxxx"
export LINKEDIN_ACCESS_TOKEN="xxxxx"

# Reload
source ~/.bashrc

# Verify
echo $DEVTO_API_KEY  # Should show your key
```

### Aliases (Optional)

```bash
# Add to ~/.bashrc
alias publish="./publish_all.py"
alias publish-test="./publish_all.py --dry-run"
alias publish-github="./publish_all.py --only github"

# Use
publish           # Publishes to all
publish-test      # Test first
publish-github    # Just GitHub
```

---

## Linux Distribution Support

| Distro | Install Command | Status |
|--------|-----------------|--------|
| Ubuntu/Debian | `sudo apt-get install ...` | ✅ Fully supported |
| Fedora/RHEL | `sudo dnf install ...` | ✅ Fully supported |
| Arch | `sudo pacman -S ...` | ✅ Fully supported |
| CentOS | `sudo yum install ...` | ✅ Should work |
| Alpine | `apk add ...` | ⚠️ May need adjustments |
| WSL (Windows) | Same as Ubuntu | ✅ Fully supported |

---

## Directory Structure

```
your-project/
├── publish_all.py              # Executable script
├── publish_config.json         # Your configuration
├── setup.py                    # Python package
├── requirements.txt            # Dependencies
├── Dockerfile                  # For Docker publishing
├── jupyter_ai_extension/
│   ├── __init__.py
│   ├── extension.py
│   └── llm_providers.py
├── .gitignore                  # Includes publish_config.json
└── .github/
    └── workflows/
        └── publish.yml         # Optional: CI/CD
```

---

## Systemd Service (Advanced)

Make publishing a Linux service:

```bash
# Create service file
sudo nano /etc/systemd/system/publish-jupyter-ai.service
```

Paste:
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
# Enable and test
sudo systemctl daemon-reload
sudo systemctl enable publish-jupyter-ai.service
sudo systemctl start publish-jupyter-ai.service

# Check status
sudo systemctl status publish-jupyter-ai.service

# View logs
sudo journalctl -u publish-jupyter-ai.service -f
```

---

## Cron Jobs (Automation)

Publish automatically on a schedule:

```bash
# Edit crontab
crontab -e

# Examples:
# Publish every Tuesday at 10 AM
0 10 * * 2 cd /path/to/project && ./publish_all.py >> ~/publish.log 2>&1

# Publish on the 1st of every month
0 10 1 * * cd /path/to/project && ./publish_all.py >> ~/publish.log 2>&1

# Publish every day at midnight
0 0 * * * cd /path/to/project && ./publish_all.py >> ~/publish.log 2>&1
```

View cron logs:
```bash
# Linux
grep CRON /var/log/syslog

# Or check your log file
tail ~/publish.log
```

---

## Docker on Linux

### Common Issues

**Docker permission denied:**
```bash
sudo usermod -aG docker $USER
newgrp docker
# May need to restart or logout/login
```

**Docker daemon not running:**
```bash
# Start it
sudo systemctl start docker

# Enable on boot
sudo systemctl enable docker

# Check status
sudo systemctl status docker
```

**Using rootless Docker:**
```bash
# Install
dockerd-rootless-setuptool.sh install

# Use normally (no sudo needed)
docker run hello-world
```

---

## GitHub Actions (CI/CD on Linux)

Auto-publish when you push a tag:

```bash
# Create workflow directory
mkdir -p .github/workflows

# Create workflow file
nano .github/workflows/publish.yml
```

Paste:
```yaml
name: Publish
on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: |
          pip install build twine requests tweepy
          git config --global user.name "GitHub Actions"
          git config --global user.email "actions@github.com"
      - run: python3 publish_all.py
        env:
          DEVTO_API_KEY: ${{ secrets.DEVTO_API_KEY }}
          TWITTER_API_KEY: ${{ secrets.TWITTER_API_KEY }}
          TWITTER_API_SECRET: ${{ secrets.TWITTER_API_SECRET }}
          TWITTER_ACCESS_TOKEN: ${{ secrets.TWITTER_ACCESS_TOKEN }}
          TWITTER_ACCESS_TOKEN_SECRET: ${{ secrets.TWITTER_ACCESS_TOKEN_SECRET }}
          LINKEDIN_ACCESS_TOKEN: ${{ secrets.LINKEDIN_ACCESS_TOKEN }}
```

Then:
```bash
git add .github/workflows/publish.yml
git commit -m "Add automated publishing workflow"
git push

# When ready to publish, just tag:
git tag v1.0.1
git push origin v1.0.1
# GitHub Actions will run automatically!
```

---

## Logging & Debugging

### View Output

```bash
# Run normally
./publish_all.py

# Verbose output
./publish_all.py --verbose

# Save to file
./publish_all.py > publish.log 2>&1

# View file
cat publish.log

# Or follow in real-time
tail -f publish.log
```

### Troubleshooting

```bash
# Check Python
python3 --version
which python3

# Check git
git config --global --list

# Check Docker
docker ps
docker info

# Check GitHub CLI
gh auth status

# Check environment
printenv | grep -E "DEVTO|TWITTER|LINKEDIN"

# Test internet
ping api.github.com
```

---

## Time Savings

| Task | Manual | Automated | Saved |
|------|--------|-----------|-------|
| PyPI | 30 min | 30 sec | 29.5 min |
| GitHub | 15 min | 15 sec | 14.75 min |
| Dev.to | 45 min | 10 sec | 44.9 min |
| Twitter | 30 min | 20 sec | 29.67 min |
| LinkedIn | 20 min | 10 sec | 19.83 min |
| Docker | 15 min | 2 min | 13 min |
| Product Hunt | 20 min | manual | - |
| **TOTAL** | **175 min** | **10 min** | **165 min** |

---

## Success Checklist

### Before Publishing

- [ ] `publish_all_linux.py` copied and made executable
- [ ] `./publish_all.py --check-deps` shows all green ✓
- [ ] `./publish_all.py --create-config` created config
- [ ] `publish_config.json` edited with your details
- [ ] Environment variables added to `~/.bashrc`
- [ ] `source ~/.bashrc` reloaded variables
- [ ] `gh auth login` authenticated GitHub
- [ ] `docker login` authenticated Docker
- [ ] `git config --global user.name` set

### Testing

- [ ] `./publish_all.py --dry-run` works without errors
- [ ] `./publish_all.py --only github` publishes to GitHub
- [ ] `./publish_all.py --only pypi` publishes to PyPI
- [ ] `./publish_all.py --only devto` publishes to Dev.to

### Go Live

- [ ] All tests passed
- [ ] `./publish_all.py` publishes to all 7 platforms
- [ ] Check each platform for your content
- [ ] Engage with community! 💬

---

## File Sizes

- `publish_all_linux.py` - ~30 KB (full-featured)
- `publish_config.json` - ~3 KB (your config)
- `LINUX_QUICKSTART.md` - ~8 KB (quick reference)
- `LINUX_PUBLISHING_GUIDE.md` - ~25 KB (comprehensive)

---

## Frequently Asked Questions

**Q: Can I run on WSL?**
A: Yes! WSL is fully supported. Works exactly like native Linux.

**Q: Do I need sudo?**
A: Not after running `sudo usermod -aG docker $USER` and `newgrp docker`.

**Q: How do I update the script?**
A: Just `cp publish_all_linux.py publish_all.py` again.

**Q: Can I schedule automatic publishing?**
A: Yes! Use cron jobs or GitHub Actions (see above).

**Q: What if a platform fails?**
A: The script continues with other platforms. Fix and re-run.

**Q: How do I change settings for the next release?**
A: Edit `publish_config.json` and update version, then run again.

---

## Next Steps

1. **Read:** `LINUX_QUICKSTART.md` (10 min)
2. **Setup:** Follow the installation commands (15 min)
3. **Configure:** Edit `publish_config.json` (5 min)
4. **Test:** Run with `--dry-run` (2 min)
5. **Publish:** Run `./publish_all.py` (5-10 min)
6. **Verify:** Check all 7 platforms (5 min)
7. **Celebrate:** You're live! 🎉

---

## Support

- **Quick reference:** See `LINUX_QUICKSTART.md`
- **Detailed guide:** See `LINUX_PUBLISHING_GUIDE.md`
- **Script help:** `./publish_all.py --help`
- **Check deps:** `./publish_all.py --check-deps`

---

## Final Notes

This Linux version of the publishing script:
- ✅ Is fully optimized for Linux
- ✅ Checks system dependencies automatically
- ✅ Provides Linux-specific error messages
- ✅ Works with all major Linux distros
- ✅ Supports Systemd, cron, and CI/CD
- ✅ Can be run as executable script

**Everything is ready to go!** 🚀

---

**Happy publishing on Linux!** 🐧

Questions? See the comprehensive guide in `LINUX_PUBLISHING_GUIDE.md`
