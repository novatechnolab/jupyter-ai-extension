#!/usr/bin/env python3
"""
Automated Multi-Platform Publishing Script for Jupyter AI Extension
Linux-Optimized Version

This script automates publishing to multiple platforms:
- PyPI
- GitHub
- Product Hunt API
- Dev.to API
- Medium (via API)
- Twitter/X (via Tweepy)
- LinkedIn (via API)
- Docker Hub
- And more...

Works seamlessly on Linux/Ubuntu/Fedora/etc.

Usage:
    python3 publish_all.py --config config.json --platforms pypi,github,devto
    
    Or make it executable:
    chmod +x publish_all.py
    ./publish_all.py --config config.json
"""

import os
import sys
import json
import subprocess
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Optional
import time
from datetime import datetime
import platform

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LinuxChecker:
    """Check Linux environment and requirements"""
    
    @staticmethod
    def check_system():
        """Verify we're on Linux"""
        if platform.system() != "Linux":
            logger.warning(f"This script is optimized for Linux. Detected: {platform.system()}")
        logger.info(f"Operating System: {platform.system()} {platform.release()}")
    
    @staticmethod
    def check_python():
        """Verify Python version"""
        if sys.version_info < (3, 8):
            logger.error("Python 3.8+ required")
            sys.exit(1)
        logger.info(f"Python: {sys.version}")
    
    @staticmethod
    def check_git():
        """Check if git is installed"""
        try:
            subprocess.run(['git', '--version'], capture_output=True, check=True)
            logger.info("✓ Git is installed")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("⚠️  Git not found. Install with: sudo apt-get install git")
            return False
    
    @staticmethod
    def check_docker():
        """Check if docker is installed"""
        try:
            subprocess.run(['docker', '--version'], capture_output=True, check=True)
            logger.info("✓ Docker is installed")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("⚠️  Docker not found. For Docker publishing, install with: sudo apt-get install docker.io")
            return False
    
    @staticmethod
    def check_gh_cli():
        """Check if GitHub CLI is installed"""
        try:
            subprocess.run(['gh', '--version'], capture_output=True, check=True)
            logger.info("✓ GitHub CLI is installed")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("⚠️  GitHub CLI not found. Install with: sudo apt-get install gh")
            return False
    
    @staticmethod
    def check_dependencies():
        """Check all dependencies"""
        logger.info("\n" + "="*60)
        logger.info("CHECKING SYSTEM DEPENDENCIES")
        logger.info("="*60)
        
        LinuxChecker.check_system()
        LinuxChecker.check_python()
        git_ok = LinuxChecker.check_git()
        docker_ok = LinuxChecker.check_docker()
        gh_ok = LinuxChecker.check_gh_cli()
        
        logger.info("="*60)
        
        return git_ok, docker_ok, gh_ok
    
    @staticmethod
    def install_missing_tools():
        """Offer to install missing tools"""
        logger.info("\nMissing tools? Here's how to install on Linux:")
        logger.info("""
        # For Ubuntu/Debian:
        sudo apt-get update
        sudo apt-get install -y git docker.io gh
        
        # For Fedora:
        sudo dnf install -y git docker gh
        
        # For Arch:
        sudo pacman -S git docker github-cli
        """)


class PublishingConfig:
    """Configuration management for publishing"""
    
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found: {self.config_file}")
            sys.exit(1)
    
    def save_config(self, config: Dict):
        """Save configuration to JSON file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def validate(self) -> bool:
        """Validate configuration"""
        required_fields = ['project_name', 'version', 'description']
        for field in required_fields:
            if not self.get(field):
                logger.error(f"Missing required field: {field}")
                return False
        return True


class PyPIPublisher:
    """Publish to PyPI - Linux optimized"""
    
    def __init__(self, config: PublishingConfig):
        self.config = config
    
    def publish(self) -> bool:
        """Publish to PyPI"""
        logger.info("\n📦 Publishing to PyPI...")
        
        try:
            # Check if build tools are available
            try:
                subprocess.run(['python3', '-m', 'build', '--version'], 
                             capture_output=True, check=True)
            except:
                logger.error("Build tools not found. Install with:")
                logger.error("  pip install --upgrade build twine")
                return False
            
            # Build distribution
            logger.info("  Building distribution...")
            result = subprocess.run(
                ['python3', '-m', 'build'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            if result.returncode != 0:
                logger.error(f"  ✗ Build failed: {result.stderr}")
                return False
            
            logger.info("  ✓ Distribution built successfully")
            
            # Check if twine is available
            try:
                subprocess.run(['python3', '-m', 'twine', '--version'],
                             capture_output=True, check=True)
            except:
                logger.error("Twine not found. Install with:")
                logger.error("  pip install twine")
                return False
            
            # Upload to PyPI
            logger.info("  Uploading to PyPI...")
            result = subprocess.run(
                ['python3', '-m', 'twine', 'upload', 'dist/*'],
                capture_output=True,
                text=True,
                shell=False
            )
            if result.returncode != 0:
                logger.error(f"  ✗ Upload failed: {result.stderr}")
                return False
            
            logger.info("  ✓ Successfully published to PyPI")
            return True
        
        except Exception as e:
            logger.error(f"  ✗ PyPI publishing failed: {str(e)}")
            return False


class GitHubPublisher:
    """Publish to GitHub - Linux optimized"""
    
    def __init__(self, config: PublishingConfig):
        self.config = config
    
    def publish(self) -> bool:
        """Push to GitHub and create release"""
        logger.info("\n🐙 Publishing to GitHub...")
        
        try:
            # Check git status
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode != 0:
                logger.error("  ✗ Not a git repository. Initialize with: git init")
                return False
            
            # Add all files
            logger.info("  Adding files to git...")
            subprocess.run(['git', 'add', '.'], 
                         check=True, capture_output=True, cwd=os.getcwd())
            
            # Commit
            logger.info("  Committing changes...")
            commit_msg = f"Release v{self.config.get('version', '1.0.0')}"
            result = subprocess.run(
                ['git', 'commit', '-m', commit_msg],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode != 0 and "nothing to commit" not in result.stderr:
                logger.warning(f"  ⚠️  Commit issue: {result.stderr}")
            
            # Push
            logger.info("  Pushing to GitHub...")
            result = subprocess.run(
                ['git', 'push', '-u', 'origin', 'main'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode != 0:
                logger.warning(f"  ⚠️  Push issue: {result.stderr}")
            else:
                logger.info("  ✓ Successfully pushed to GitHub")
            
            # Try to create release with gh cli
            try:
                version = self.config.get('version', '1.0.0')
                logger.info(f"  Creating release v{version}...")
                
                result = subprocess.run(
                    ['gh', 'release', 'create', f'v{version}',
                     '--title', f"Jupyter AI Extension v{version}",
                     '--notes', self.config.get('release_notes', 'Release notes')],
                    capture_output=True,
                    text=True,
                    cwd=os.getcwd()
                )
                
                if result.returncode == 0:
                    logger.info(f"  ✓ Release v{version} created")
                else:
                    logger.warning(f"  ⚠️  Release creation: {result.stderr}")
            except FileNotFoundError:
                logger.warning("  ⚠️  gh CLI not found. Install with: sudo apt-get install gh")
            
            return True
        
        except subprocess.CalledProcessError as e:
            logger.error(f"  ✗ GitHub publishing failed: {str(e)}")
            return False


class DevToPublisher:
    """Publish to Dev.to - Linux optimized"""
    
    def __init__(self, config: PublishingConfig):
        self.config = config
        self.api_key = os.getenv('DEVTO_API_KEY')
        self.base_url = 'https://dev.to/api/articles'
    
    def publish(self) -> bool:
        """Publish article to Dev.to"""
        logger.info("\n📝 Publishing to Dev.to...")
        
        if not self.api_key:
            logger.warning("  ⚠️  DEVTO_API_KEY not set in environment")
            logger.warning("  Get key from: https://dev.to/settings/account")
            logger.warning("  Set with: export DEVTO_API_KEY='your_key'")
            return False
        
        try:
            import requests
            
            article_data = {
                'article': {
                    'title': self.config.get('devto_title', 'Jupyter AI Extension'),
                    'description': self.config.get('description'),
                    'body_markdown': self.load_article(),
                    'tags': self.config.get('devto_tags', ['jupyter', 'python', 'ai']),
                    'published': True
                }
            }
            
            headers = {
                'api-key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                self.base_url,
                json=article_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 201:
                data = response.json()
                logger.info(f"  ✓ Published to Dev.to: {data['url']}")
                return True
            else:
                logger.error(f"  ✗ Dev.to error: {response.text}")
                return False
        
        except ImportError:
            logger.warning("  ⚠️  requests library not installed")
            logger.warning("  Install with: pip install requests")
            return False
        except Exception as e:
            logger.error(f"  ✗ Dev.to publishing failed: {str(e)}")
            return False
    
    def load_article(self) -> str:
        """Load article markdown"""
        article_path = self.config.get('devto_article_path')
        if article_path and os.path.exists(article_path):
            with open(article_path, 'r') as f:
                return f.read()
        
        return self._default_article()
    
    @staticmethod
    def _default_article() -> str:
        """Default article template"""
        return """# Jupyter AI Extension

Multi-LLM support for Jupyter notebooks with OpenAI, Claude, and Google Gemini.

## Features
- Support for GPT-4, Claude Opus, and Gemini 2.0 Flash
- Simple one-line configuration
- Chat and completion modes
- Fully documented with examples

## Installation
```bash
pip install jupyter-ai-extension
```

## Quick Start
```python
from jupyter_ai_extension import JupyterAIExtension
ai = JupyterAIExtension()
ai.configure("openai")
response = ai.generate("Explain machine learning")
print(response)
```

## Documentation
- GitHub: https://github.com/yourusername/jupyter-ai-extension
- PyPI: https://pypi.org/project/jupyter-ai-extension/

Check out the repository for more examples and documentation!
"""


class TwitterPublisher:
    """Publish to Twitter/X - Linux optimized"""
    
    def __init__(self, config: PublishingConfig):
        self.config = config
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    
    def publish(self) -> bool:
        """Publish thread to Twitter"""
        logger.info("\n🐦 Publishing to Twitter/X...")
        
        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            logger.warning("  ⚠️  Twitter credentials not set in environment")
            logger.warning("  Get from: https://developer.twitter.com/")
            logger.warning("  Set with: export TWITTER_API_KEY='...'")
            return False
        
        try:
            import tweepy
            
            client = tweepy.Client(
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret
            )
            
            tweets = self.config.get('twitter_thread', [])
            if not tweets:
                logger.warning("  ⚠️  No tweets configured")
                return False
            
            previous_tweet_id = None
            for i, tweet_text in enumerate(tweets, 1):
                logger.info(f"  Posting tweet {i}/{len(tweets)}...")
                
                try:
                    response = client.create_tweet(text=tweet_text)
                    
                    if response and response.data:
                        previous_tweet_id = response.data['id']
                        logger.info(f"    ✓ Tweet {i} posted")
                        time.sleep(2)  # Rate limiting
                    else:
                        logger.error(f"    ✗ Failed to post tweet {i}")
                        return False
                except Exception as e:
                    logger.error(f"    ✗ Error posting tweet {i}: {str(e)}")
                    return False
            
            logger.info(f"  ✓ Published {len(tweets)}-tweet thread to Twitter")
            return True
        
        except ImportError:
            logger.warning("  ⚠️  tweepy library not installed")
            logger.warning("  Install with: pip install tweepy")
            return False
        except Exception as e:
            logger.error(f"  ✗ Twitter publishing failed: {str(e)}")
            return False


class LinkedInPublisher:
    """Publish to LinkedIn - Linux optimized"""
    
    def __init__(self, config: PublishingConfig):
        self.config = config
        self.access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    
    def publish(self) -> bool:
        """Publish to LinkedIn"""
        logger.info("\n💼 Publishing to LinkedIn...")
        
        if not self.access_token:
            logger.warning("  ⚠️  LINKEDIN_ACCESS_TOKEN not set in environment")
            logger.warning("  Get from: https://www.linkedin.com/developers/apps")
            logger.warning("  Set with: export LINKEDIN_ACCESS_TOKEN='...'")
            return False
        
        try:
            import requests
            
            post_content = self.config.get('linkedin_post', 'Check out my new project!')
            
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'lifecycleState': 'PUBLISHED',
                'specificContent': {
                    'com.linkedin.ugc.Share': {
                        'shareCommentary': {
                            'text': post_content
                        },
                        'shareMediaCategory': 'NONE'
                    }
                },
                'visibility': {
                    'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
                }
            }
            
            response = requests.post(
                'https://api.linkedin.com/v2/ugcPosts',
                json=data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code in [201, 200]:
                logger.info("  ✓ Published to LinkedIn")
                return True
            else:
                logger.error(f"  ✗ LinkedIn error: {response.text}")
                return False
        
        except ImportError:
            logger.warning("  ⚠️  requests library not installed")
            logger.warning("  Install with: pip install requests")
            return False
        except Exception as e:
            logger.error(f"  ✗ LinkedIn publishing failed: {str(e)}")
            return False


class DockerPublisher:
    """Publish to Docker Hub - Linux optimized"""
    
    def __init__(self, config: PublishingConfig):
        self.config = config
    
    def publish(self) -> bool:
        """Build and push Docker image"""
        logger.info("\n🐳 Publishing to Docker Hub...")
        
        try:
            docker_username = self.config.get('docker_username')
            image_name = self.config.get('docker_image_name', 'jupyter-ai-extension')
            version = self.config.get('version', '1.0.0')
            
            if not docker_username:
                logger.warning("  ⚠️  docker_username not configured")
                return False
            
            # Check if Dockerfile exists
            if not os.path.exists('Dockerfile'):
                logger.warning("  ⚠️  Dockerfile not found in current directory")
                return False
            
            # Check if docker is running
            try:
                subprocess.run(['docker', 'ps'], capture_output=True, check=True)
            except Exception:
                logger.error("  ✗ Docker daemon not running")
                logger.error("  Start with: sudo systemctl start docker")
                return False
            
            # Build image
            image_tag = f"{docker_username}/{image_name}:{version}"
            logger.info(f"  Building Docker image: {image_tag}...")
            
            result = subprocess.run(
                ['docker', 'build', '-t', image_tag, '.'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode != 0:
                logger.error(f"  ✗ Docker build failed: {result.stderr}")
                return False
            
            logger.info("  ✓ Docker image built")
            
            # Check if logged in to Docker Hub
            try:
                subprocess.run(['docker', 'info'], capture_output=True, check=True)
            except:
                logger.error("  ✗ Not logged in to Docker Hub")
                logger.error("  Login with: docker login")
                return False
            
            # Push image
            logger.info("  Pushing to Docker Hub...")
            result = subprocess.run(
                ['docker', 'push', image_tag],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode != 0:
                logger.error(f"  ✗ Docker push failed: {result.stderr}")
                return False
            
            logger.info(f"  ✓ Pushed to Docker Hub: {image_tag}")
            return True
        
        except Exception as e:
            logger.error(f"  ✗ Docker publishing failed: {str(e)}")
            return False


class ProductHuntPublisher:
    """Publish to Product Hunt"""
    
    def __init__(self, config: PublishingConfig):
        self.config = config
    
    def publish(self) -> bool:
        """Publish to Product Hunt (manual)"""
        logger.info("\n🚀 Product Hunt - Manual Setup Required")
        logger.info("""
        Product Hunt publishing requires manual setup:
        
        1. Go to https://www.producthunt.com/
        2. Sign in or create account
        3. Click "Ship" to create new product
        4. Fill in details:
           - Name: {}
           - Tagline: {}
           - Description: {}
           - Upload thumbnail image
           - Add 3-5 gallery images
        5. Set launch date for next Tuesday
        6. Review and launch
        
        For best results:
        - Post on Tuesday 12:01 AM PST
        - Write compelling description
        - Include working product link
        - Prepare launch comments
        """.format(
            self.config.get('project_name'),
            self.config.get('product_hunt_tagline', ''),
            self.config.get('description')
        ))
        return True


class MultiPlatformPublisher:
    """Orchestrate publishing to multiple platforms"""
    
    PUBLISHERS = {
        'pypi': PyPIPublisher,
        'github': GitHubPublisher,
        'devto': DevToPublisher,
        'twitter': TwitterPublisher,
        'linkedin': LinkedInPublisher,
        'docker': DockerPublisher,
        'producthunt': ProductHuntPublisher,
    }
    
    def __init__(self, config_file: str):
        self.config = PublishingConfig(config_file)
        self.results = {}
    
    def publish(self, platforms: Optional[List[str]] = None, check_deps: bool = True):
        """Publish to selected platforms"""
        
        # Check dependencies on Linux
        if check_deps:
            LinuxChecker.check_dependencies()
        
        if not self.config.validate():
            logger.error("Configuration validation failed")
            return False
        
        # Use all platforms if not specified
        if not platforms:
            platforms = list(self.PUBLISHERS.keys())
        
        logger.info(f"\n🚀 Publishing to platforms: {', '.join(platforms)}")
        logger.info(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        for platform_name in platforms:
            if platform_name not in self.PUBLISHERS:
                logger.warning(f"❓ Unknown platform: {platform_name}")
                continue
            
            try:
                publisher_class = self.PUBLISHERS[platform_name]
                publisher = publisher_class(self.config)
                success = publisher.publish()
                self.results[platform_name] = success
                
                time.sleep(2)  # Delay between platforms
            
            except Exception as e:
                logger.error(f"❌ Error publishing to {platform_name}: {str(e)}")
                self.results[platform_name] = False
        
        # Print summary
        self.print_summary()
        return all(self.results.values())
    
    def print_summary(self):
        """Print publishing summary"""
        print("=" * 70)
        logger.info("\n📊 PUBLISHING SUMMARY:")
        print("=" * 70)
        
        successful = sum(1 for v in self.results.values() if v)
        total = len(self.results)
        
        for platform, success in self.results.items():
            status = "✓ SUCCESS" if success else "✗ FAILED"
            logger.info(f"  {platform.upper():15} {status}")
        
        print("=" * 70)
        logger.info(f"\n📈 Results: {successful}/{total} platforms successful\n")
        
        if successful == total:
            logger.info("🎉 All platforms published successfully!")
        else:
            logger.warning(f"⚠️  {total - successful} platform(s) failed")


def create_example_config():
    """Create example configuration file"""
    example_config = {
        "project_name": "Jupyter AI Extension",
        "version": "1.0.0",
        "description": "Multi-LLM support for Jupyter Notebook (OpenAI, Claude, Gemini)",
        "github_repo": "yourusername/jupyter-ai-extension",
        "github_url": "https://github.com/yourusername/jupyter-ai-extension",
        
        "devto_title": "Jupyter AI Extension - Multi-LLM Support",
        "devto_tags": ["jupyter", "python", "ai", "llm"],
        "devto_article_path": "articles/announcement.md",
        
        "twitter_thread": [
            "🚀 Just launched Jupyter AI Extension! Use OpenAI, Claude & Gemini in your notebooks with a simple Python API.",
            "Features: ✓ Multi-LLM support ✓ One-line setup ✓ Chat mode ✓ Production-ready",
            "Get started: pip install jupyter-ai-extension",
            "Open source, fully documented. GitHub: https://github.com/yourusername/jupyter-ai-extension"
        ],
        
        "linkedin_post": "Excited to announce Jupyter AI Extension! Seamlessly use OpenAI, Claude, and Google Gemini in your Jupyter notebooks. Open source, fully documented.",
        
        "docker_username": "yourusername",
        "docker_image_name": "jupyter-ai-extension",
        
        "product_hunt_tagline": "Multi-LLM support for Jupyter notebooks",
        
        "release_notes": "Initial release with support for OpenAI, Claude, and Gemini. Fully documented with examples."
    }
    
    return example_config


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='🚀 Publish Jupyter AI Extension to multiple platforms (Linux-optimized)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 publish_all.py                                    # Publish to all platforms
  python3 publish_all.py --platforms pypi,github,devto     # Specific platforms
  python3 publish_all.py --dry-run                          # Test without publishing
  python3 publish_all.py --only github                      # Test single platform
  python3 publish_all.py --create-config                    # Create config template
  python3 publish_all.py --check-deps                       # Check dependencies
  
Or make it executable:
  chmod +x publish_all.py
  ./publish_all.py
        """
    )
    
    parser.add_argument(
        '--config',
        default='publish_config.json',
        help='Configuration file (default: publish_config.json)'
    )
    
    parser.add_argument(
        '--platforms',
        default=None,
        help='Comma-separated list of platforms (default: all)'
    )
    
    parser.add_argument(
        '--create-config',
        action='store_true',
        help='Create example configuration file'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Dry run (shows what would be published, no changes)'
    )
    
    parser.add_argument(
        '--only',
        default=None,
        help='Publish to only this platform (for testing)'
    )
    
    parser.add_argument(
        '--check-deps',
        action='store_true',
        help='Check system dependencies and exit'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Check dependencies
    if args.check_deps:
        LinuxChecker.check_dependencies()
        return 0
    
    # Create example config
    if args.create_config:
        config = create_example_config()
        with open('publish_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        logger.info("✓ Created publish_config.json")
        logger.info("Edit this file with your details:")
        logger.info("  nano publish_config.json")
        logger.info("\nThen run: python3 publish_all.py")
        return 0
    
    # Determine platforms
    platforms = None
    if args.only:
        platforms = [args.only]
    elif args.platforms:
        platforms = [p.strip() for p in args.platforms.split(',')]
    
    # Publish
    publisher = MultiPlatformPublisher(args.config)
    
    if args.dry_run:
        logger.info("🧪 DRY RUN MODE - No changes will be made")
        logger.info(f"   Would publish to: {platforms or 'all platforms'}")
        return 0
    
    success = publisher.publish(platforms=platforms)
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
