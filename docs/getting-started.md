# Getting Started with AI Time Machines

## Overview

AI Time Machines is a comprehensive toolkit that combines git repository management with advanced web scraping capabilities. This guide will help you get started with the core functionality.

## Installation Guide

### Prerequisites

Before installing AI Time Machines, ensure you have:

- Python 3.7 or higher
- Git installed on your system
- Chrome or Firefox browser (for dynamic web scraping)

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/lippytm/AI-Time-Machines.git
   cd AI-Time-Machines
   ```

2. **Create a Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the Package**
   ```bash
   pip install -e .
   ```

5. **Verify Installation**
   ```bash
   ai-time-machines --help
   ```

## Quick Start Examples

### Repository Cloning

```python
from ai_time_machines import RepositoryCloner

# Basic usage
cloner = RepositoryCloner()
repo = cloner.clone_repository("https://github.com/octocat/Hello-World.git")
print(f"Cloned to: {repo.working_dir}")
```

### Web Scraping

```python
from ai_time_machines import WebScraper

# Basic web scraping
scraper = WebScraper()
data = scraper.scrape_static_content("https://httpbin.org/html")
print(f"Found {len(data['links'])} links")
```

## Core Concepts

### Repository Management

The `RepositoryCloner` class provides:
- Cloning repositories with various options
- Branch management
- Repository information extraction
- Bulk operations on multiple repositories

### Web Scraping

The `WebScraper` class supports:
- Static content scraping with requests/BeautifulSoup
- Dynamic content scraping with Selenium
- Data extraction using CSS selectors
- Configurable delays and timeouts

## Configuration

### Basic Configuration

```python
# Custom base directory for repositories
cloner = RepositoryCloner(base_dir="/path/to/repos")

# Custom scraper settings
scraper = WebScraper(
    delay=2.0,          # 2 second delay between requests
    timeout=60,         # 60 second timeout
    user_agent="My Bot" # Custom user agent
)
```

### Advanced Configuration

Create a `config.py` file:

```python
import os

# Repository settings
REPO_BASE_DIR = os.getenv('AI_TM_BASE_DIR', './repositories')
DEFAULT_BRANCH = os.getenv('AI_TM_DEFAULT_BRANCH', 'main')

# Scraping settings
SCRAPER_DELAY = float(os.getenv('AI_TM_DELAY', '1.0'))
SCRAPER_TIMEOUT = int(os.getenv('AI_TM_TIMEOUT', '30'))
USER_AGENT = os.getenv('AI_TM_USER_AGENT', 'AI-Time-Machines/1.0')
```

## Best Practices

### Repository Cloning

1. **Use descriptive destination paths**
2. **Handle errors gracefully**
3. **Clean up resources after use**
4. **Check repository status before operations**

### Web Scraping

1. **Respect robots.txt**
2. **Use appropriate delays**
3. **Handle errors and timeouts**
4. **Save data regularly**
5. **Use the least intrusive method (static vs dynamic)**

## Common Use Cases

### Academic Research

```python
# Clone multiple research repositories
repos = [
    "https://github.com/tensorflow/tensorflow.git",
    "https://github.com/pytorch/pytorch.git",
    "https://github.com/scikit-learn/scikit-learn.git"
]

cloner = RepositoryCloner(base_dir="./research_repos")
for repo_url in repos:
    try:
        repo = cloner.clone_repository(repo_url, depth=1)  # Shallow clone
        print(f"✅ Cloned {repo_url}")
    except Exception as e:
        print(f"❌ Failed to clone {repo_url}: {e}")
```

### Data Collection

```python
# Scrape news websites for articles
scraper = WebScraper(delay=2.0)  # Be respectful

news_sites = [
    "https://news.ycombinator.com",
    "https://www.reddit.com/r/technology.rss"
]

for site in news_sites:
    try:
        data = scraper.scrape_static_content(site)
        scraper.save_scraped_data(data, f"data_{site.split('//')[1].split('.')[0]}.json")
    except Exception as e:
        print(f"Error scraping {site}: {e}")
```

## Troubleshooting

### Common Issues

1. **Git not found**: Ensure Git is installed and in PATH
2. **Browser driver issues**: Install ChromeDriver or GeckoDriver
3. **Permission errors**: Check file permissions and ownership
4. **Network timeouts**: Increase timeout values or check connectivity

### Debugging

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your code here
```

## Next Steps

1. Read the [API Reference](api-reference.md)
2. Check out [Examples](../examples/)
3. Learn about [Advanced Usage](advanced-usage.md)
4. Explore [Integration Patterns](integration-patterns.md)