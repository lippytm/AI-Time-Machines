# Software Architecture Guide

## Overview

AI Time Machines is designed with a modular, extensible architecture that separates concerns between git repository management and web scraping functionality. This document explains how the software is created and structured.

## Architecture Principles

### 1. Separation of Concerns
- **Repository Management**: Handled by `RepositoryCloner` class
- **Web Scraping**: Handled by `WebScraper` class  
- **CLI Interface**: Handled by `cli.py` module
- **Package Management**: Standard Python packaging with `setup.py`

### 2. Error Handling and Logging
- Comprehensive error handling with meaningful error messages
- Configurable logging levels for debugging and monitoring
- Graceful degradation when network or system resources are unavailable

### 3. Resource Management
- Proper cleanup of git repositories and web drivers
- Context managers and cleanup methods to prevent resource leaks
- Temporary file handling with automatic cleanup

### 4. Extensibility
- Class-based design allows for easy inheritance and customization
- Plugin-style architecture for adding new scrapers or cloners
- Configuration-driven behavior for different use cases

## Core Components

### RepositoryCloner Class

```python
class RepositoryCloner:
    def __init__(self, base_dir=None, log_level=logging.INFO)
    def clone_repository(self, repo_url, destination=None, branch=None, depth=None, single_branch=False)
    def get_repository_info(self, repo_path)
    def list_cloned_repositories(self)
    def update_repository(self, repo_path, branch=None)
    def cleanup(self)
```

**Responsibilities:**
- Git repository cloning with various options
- Repository metadata extraction
- Branch and commit management
- Bulk repository operations

**Dependencies:**
- `gitpython` for Git operations
- `pathlib` for path management
- `logging` for operation tracking

### WebScraper Class

```python
class WebScraper:
    def __init__(self, user_agent=None, delay=1.0, timeout=30, log_level=logging.INFO)
    def scrape_static_content(self, url, parser='html.parser', custom_headers=None)
    def scrape_dynamic_content(self, url, wait_element=None, wait_time=10)
    def init_selenium_driver(self, browser='chrome', headless=True)
    def extract_data_by_selector(self, url, selectors, use_selenium=False)
    def save_scraped_data(self, data, filename, format='json')
    def cleanup(self)
```

**Responsibilities:**
- Static web content scraping
- Dynamic content scraping with JavaScript support
- Data extraction using CSS selectors
- Data persistence in various formats

**Dependencies:**
- `requests` for HTTP operations
- `beautifulsoup4` for HTML parsing
- `selenium` for dynamic content
- `lxml` for XML processing

## Design Patterns Used

### 1. Factory Pattern
The WebScraper can create different types of browser drivers:

```python
def init_selenium_driver(self, browser='chrome', headless=True):
    if browser.lower() == 'chrome':
        options = ChromeOptions()
        # Configure Chrome options
        self.driver = webdriver.Chrome(options=options)
    elif browser.lower() == 'firefox':
        options = FirefoxOptions()
        # Configure Firefox options
        self.driver = webdriver.Firefox(options=options)
```

### 2. Template Method Pattern
Both cloner and scraper follow a common pattern:
1. Initialize resources
2. Perform operations
3. Handle errors gracefully
4. Clean up resources

### 3. Strategy Pattern
Different parsing strategies for web content:
- Static parsing with BeautifulSoup
- Dynamic parsing with Selenium
- Custom selector-based extraction

### 4. Builder Pattern
Repository cloning options are built progressively:

```python
clone_kwargs = {}
if branch:
    clone_kwargs['branch'] = branch
if depth:
    clone_kwargs['depth'] = depth
if single_branch:
    clone_kwargs['single_branch'] = True

repo = Repo.clone_from(repo_url, destination, **clone_kwargs)
```

## Data Flow

### Repository Cloning Flow
```
URL Input → Validation → Git Clone → Metadata Extraction → Storage → Cleanup
```

### Web Scraping Flow
```
URL Input → Request/Load → Parse → Extract → Transform → Save → Cleanup
```

### Combined Workflow Flow
```
Repository URLs → Clone → Extract Info → Website URLs → Scrape → Combine Data → Report
```

## Error Handling Strategy

### 1. Layered Error Handling
- **Input Validation**: Check parameters before processing
- **Network Errors**: Handle connection timeouts and failures
- **System Errors**: Handle file system and permission issues
- **Resource Errors**: Handle browser and git failures

### 2. Error Response Format
```python
{
    "error": "Human-readable error message",
    "url": "Original request URL",
    "timestamp": 1234567890.123,
    "details": "Additional technical details"
}
```

### 3. Graceful Degradation
- Continue processing other items if one fails
- Provide partial results when possible
- Log errors for debugging while continuing operation

## Configuration Management

### Environment Variables
```python
AI_TM_BASE_DIR      # Default repository directory
AI_TM_USER_AGENT    # Default user agent string
AI_TM_DEFAULT_DELAY # Default delay between requests
AI_TM_LOG_LEVEL     # Logging verbosity
```

### Runtime Configuration
```python
# Repository cloner configuration
cloner = RepositoryCloner(
    base_dir="/custom/path",
    log_level=logging.DEBUG
)

# Web scraper configuration
scraper = WebScraper(
    user_agent="Custom Bot 1.0",
    delay=2.0,
    timeout=60
)
```

## Performance Considerations

### 1. Memory Management
- Streaming for large files
- Cleanup of temporary resources
- Lazy loading of repository data

### 2. Network Efficiency
- Connection pooling with requests.Session
- Configurable delays to respect server limits
- Timeout handling to prevent hanging

### 3. Scalability
- Batch operations for multiple repositories
- Parallel processing capability (future enhancement)
- Efficient data structures for large datasets

## Security Considerations

### 1. Input Validation
- URL validation and sanitization
- Path traversal prevention
- Injection attack prevention

### 2. Network Security
- HTTPS by default
- Certificate validation
- Safe header handling

### 3. File System Security
- Safe temporary file creation
- Permission checking
- Directory traversal prevention

## Testing Strategy

### 1. Unit Tests
- Individual method testing
- Mock external dependencies
- Error condition testing

### 2. Integration Tests
- End-to-end workflow testing
- Real network operations (where possible)
- Resource cleanup verification

### 3. Example-based Testing
- Runnable examples serve as integration tests
- Documentation examples are verified
- Common use cases are covered

## Future Enhancements

### 1. Planned Features
- Parallel processing for batch operations
- Advanced filtering and search capabilities
- Database integration for metadata storage
- REST API interface

### 2. Performance Improvements
- Caching for repeated operations
- Connection pooling optimization
- Memory usage optimization

### 3. Additional Integrations
- More version control systems (SVN, Mercurial)
- Additional browser engines
- Cloud storage integration

## Contributing Guidelines

### 1. Code Standards
- Follow PEP 8 style guidelines
- Include comprehensive docstrings
- Add type hints where appropriate
- Maintain test coverage above 80%

### 2. Architecture Compliance
- Maintain separation of concerns
- Follow established patterns
- Add proper error handling
- Include cleanup methods

### 3. Documentation Requirements
- Update API documentation
- Add usage examples
- Update architecture documentation
- Include migration guides for breaking changes

This architecture provides a solid foundation for the AI Time Machines toolkit while remaining flexible enough to accommodate future enhancements and use cases.