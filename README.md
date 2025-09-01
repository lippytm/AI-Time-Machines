# AI-Time-Machines

Adding AI Agents to everything with Time Machines - A comprehensive toolkit for repository cloning and web scraping capabilities.

## 🌟 Features

- **🔄 Repository Cloning**: Advanced git repository cloning and management
- **🕷️ Web Scraping**: Comprehensive web scraping for both static and dynamic content
- **📚 Educational Resources**: Complete tutorials and learning materials
- **🛠️ CLI Interface**: Easy-to-use command-line tools
- **📖 Comprehensive Documentation**: Detailed guides and examples

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/lippytm/AI-Time-Machines.git
cd AI-Time-Machines

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Basic Usage

#### Repository Cloning

```python
from ai_time_machines import RepositoryCloner

# Initialize cloner
cloner = RepositoryCloner()

# Clone a repository
repo = cloner.clone_repository("https://github.com/user/repo.git")

# Get repository information
info = cloner.get_repository_info(repo.working_dir)
print(f"Current branch: {info['current_branch']}")
```

#### Web Scraping

```python
from ai_time_machines import WebScraper

# Initialize scraper
scraper = WebScraper()

# Scrape static content
data = scraper.scrape_static_content("https://example.com")
print(f"Title: {data['title']}")
print(f"Found {len(data['links'])} links")

# Scrape dynamic content (requires Selenium)
dynamic_data = scraper.scrape_dynamic_content("https://spa-example.com")

# Extract specific data using CSS selectors
extracted = scraper.extract_data_by_selector(
    "https://example.com",
    {"title": "h1", "paragraphs": "p"}
)
```

### Command Line Interface

```bash
# Clone a repository
ai-time-machines clone https://github.com/user/repo.git

# Clone specific branch
ai-time-machines clone https://github.com/user/repo.git --branch main

# List cloned repositories
ai-time-machines list

# Scrape a website
ai-time-machines scrape https://example.com --output data.json

# Scrape dynamic content
ai-time-machines scrape https://spa-example.com --dynamic

# Extract specific data
ai-time-machines extract https://example.com '{"title": "h1", "links": "a"}'
```

## 📋 Requirements

- Python 3.7+
- Git
- Chrome or Firefox (for dynamic web scraping)

### Dependencies

- `requests` - HTTP library for web scraping
- `beautifulsoup4` - HTML/XML parsing
- `gitpython` - Git repository management
- `selenium` - Web browser automation
- `lxml` - XML and HTML parser

## 🎓 Educational Materials

### How the Software is Created

This software is built using modern Python development practices and follows these principles:

#### Architecture Overview

```
ai_time_machines/
├── __init__.py          # Package initialization
├── cloning.py           # Git repository cloning functionality
├── scraping.py          # Web scraping capabilities
└── cli.py              # Command-line interface
```

#### Design Patterns Used

1. **Class-based Architecture**: Each major functionality is encapsulated in its own class
2. **Error Handling**: Comprehensive error handling with logging
3. **Separation of Concerns**: Clear separation between cloning, scraping, and CLI functionality
4. **Configuration Management**: Flexible configuration options for different use cases

#### Development Process

1. **Requirements Analysis**: Understanding the need for cloning and scraping capabilities
2. **Design Phase**: Planning the class structure and interfaces
3. **Implementation**: Writing clean, documented code with error handling
4. **Testing**: Ensuring reliability and robustness
5. **Documentation**: Creating comprehensive guides and examples

### Key Technologies Explained

#### Git Operations with GitPython

GitPython provides a Python interface to Git repositories:

```python
from git import Repo

# Clone a repository
repo = Repo.clone_from(url, destination)

# Get repository information
current_branch = repo.active_branch.name
commits = list(repo.iter_commits(max_count=10))
```

#### Web Scraping with Requests and BeautifulSoup

For static content scraping:

```python
import requests
from bs4 import BeautifulSoup

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract data
title = soup.find('title').text
links = soup.find_all('a')
```

#### Dynamic Content with Selenium

For JavaScript-heavy websites:

```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get(url)

# Wait for dynamic content to load
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "dynamic-content")))

# Extract data
html = driver.page_source
```

## 📚 Tutorials

### Tutorial 1: Setting Up Your Environment

1. **Install Python**: Ensure Python 3.7+ is installed
2. **Clone the repository**: `git clone https://github.com/lippytm/AI-Time-Machines.git`
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Install the package**: `pip install -e .`
5. **Verify installation**: `ai-time-machines --help`

### Tutorial 2: Basic Repository Cloning

```python
from ai_time_machines import RepositoryCloner

# Create a cloner instance
cloner = RepositoryCloner(base_dir="./my_repos")

# Clone a repository
repo = cloner.clone_repository(
    "https://github.com/octocat/Hello-World.git",
    branch="main"
)

# Explore the repository
info = cloner.get_repository_info(repo.working_dir)
print(f"Repository: {info['path']}")
print(f"Current branch: {info['current_branch']}")
print(f"Branches: {info['branches']}")
print(f"Latest commit: {info['latest_commit']['message']}")

# Clean up
cloner.cleanup()
```

### Tutorial 3: Web Scraping Basics

```python
from ai_time_machines import WebScraper

# Create a scraper instance
scraper = WebScraper(delay=1.0)

# Scrape a simple website
data = scraper.scrape_static_content("https://httpbin.org/html")

# Examine the results
print(f"Page title: {data['title']}")
print(f"Number of links: {len(data['links'])}")
print(f"Text content preview: {data['text_content'][:100]}...")

# Save the data
scraper.save_scraped_data(data, "scraped_data.json")

# Clean up
scraper.cleanup()
```

### Tutorial 4: Advanced Web Scraping

```python
from ai_time_machines import WebScraper

scraper = WebScraper()

# Scrape a site with custom CSS selectors
selectors = {
    "title": "h1",
    "description": ".description",
    "price": ".price",
    "features": ".feature-list li"
}

data = scraper.extract_data_by_selector(
    "https://example-store.com/product/123",
    selectors,
    use_selenium=True  # For dynamic content
)

print(f"Product: {data['title']}")
print(f"Price: {data['price']}")
print(f"Features: {data['features']}")

scraper.cleanup()
```

### Tutorial 5: Building Your Own Extensions

You can extend the functionality by creating custom classes:

```python
from ai_time_machines import WebScraper
import json

class NewsScaper(WebScraper):
    """Specialized scraper for news websites."""
    
    def scrape_article(self, url):
        """Extract article-specific information."""
        selectors = {
            "headline": "h1",
            "author": ".author",
            "date": ".publish-date",
            "content": ".article-content p"
        }
        
        return self.extract_data_by_selector(url, selectors)
    
    def scrape_news_site(self, base_url):
        """Scrape multiple articles from a news site."""
        # Get article links
        data = self.scrape_static_content(base_url)
        article_links = [
            link['absolute_url'] for link in data['links']
            if '/article/' in link['absolute_url']
        ]
        
        # Scrape each article
        articles = []
        for link in article_links[:5]:  # Limit to 5 articles
            article = self.scrape_article(link)
            articles.append(article)
        
        return articles

# Usage
news_scraper = NewsScaper()
articles = news_scraper.scrape_news_site("https://example-news.com")
```

## 🔧 Configuration

### Environment Variables

You can configure the tools using environment variables:

```bash
export AI_TM_BASE_DIR="/path/to/repositories"
export AI_TM_USER_AGENT="My Custom Bot"
export AI_TM_DEFAULT_DELAY="2.0"
export AI_TM_LOG_LEVEL="DEBUG"
```

### Configuration File

Create a `config.json` file for advanced configuration:

```json
{
  "cloning": {
    "base_dir": "./repositories",
    "default_branch": "main",
    "max_depth": null
  },
  "scraping": {
    "user_agent": "AI-Time-Machines/1.0",
    "default_delay": 1.0,
    "timeout": 30,
    "browser": "chrome",
    "headless": true
  }
}
```

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check this README and inline code documentation
- **Issues**: Report bugs and request features on GitHub Issues
- **Discussions**: Join community discussions on GitHub Discussions

## 🚨 Ethical Usage

Please use these tools responsibly:

- **Respect robots.txt**: Always check and respect website crawling policies
- **Rate limiting**: Use appropriate delays between requests
- **Terms of service**: Respect website terms of service
- **Copyright**: Respect intellectual property rights
- **Privacy**: Handle personal data responsibly

## 🔄 Changelog

### v0.1.0 (Initial Release)

- ✅ Basic repository cloning functionality
- ✅ Static web scraping capabilities
- ✅ Dynamic content scraping with Selenium
- ✅ Command-line interface
- ✅ Comprehensive documentation
- ✅ Educational tutorials 
