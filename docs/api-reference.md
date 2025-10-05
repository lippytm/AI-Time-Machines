# AI Time Machines API Reference

## RepositoryCloner Class

### Constructor

```python
RepositoryCloner(base_dir=None, log_level=logging.INFO)
```

**Parameters:**
- `base_dir` (str, optional): Base directory for cloning repositories. Defaults to `./repositories`
- `log_level` (int): Logging level for operations

### Methods

#### clone_repository()

```python
clone_repository(repo_url, destination=None, branch=None, depth=None, single_branch=False)
```

Clone a git repository with various options.

**Parameters:**
- `repo_url` (str): URL of the repository to clone
- `destination` (str, optional): Local destination path
- `branch` (str, optional): Specific branch to clone
- `depth` (int, optional): Depth of clone (for shallow clones)
- `single_branch` (bool): Whether to clone only a single branch

**Returns:** `git.Repo` object

**Raises:**
- `GitCommandError`: If cloning fails
- `ValueError`: If invalid parameters provided

#### get_repository_info()

```python
get_repository_info(repo_path)
```

Get comprehensive information about a cloned repository.

**Parameters:**
- `repo_path` (str): Path to the repository

**Returns:** Dictionary containing:
- `path`: Repository path
- `current_branch`: Current branch name
- `branches`: List of all branches
- `remotes`: Dictionary of remotes
- `latest_commit`: Latest commit information
- `is_dirty`: Whether repository has uncommitted changes
- `untracked_files`: List of untracked files

#### list_cloned_repositories()

```python
list_cloned_repositories()
```

List all repositories in the base directory.

**Returns:** List of repository information dictionaries

#### update_repository()

```python
update_repository(repo_path, branch=None)
```

Update a repository by pulling latest changes.

**Parameters:**
- `repo_path` (str): Path to the repository
- `branch` (str, optional): Branch to checkout and update

**Returns:** `bool` - True if update successful

#### cleanup()

```python
cleanup()
```

Clean up resources and close repository connections.

## WebScraper Class

### Constructor

```python
WebScraper(user_agent=None, delay=1.0, timeout=30, log_level=logging.INFO)
```

**Parameters:**
- `user_agent` (str, optional): Custom user agent string
- `delay` (float): Delay between requests in seconds
- `timeout` (int): Request timeout in seconds
- `log_level` (int): Logging level for operations

### Methods

#### scrape_static_content()

```python
scrape_static_content(url, parser='html.parser', custom_headers=None)
```

Scrape static web content using requests and BeautifulSoup.

**Parameters:**
- `url` (str): URL to scrape
- `parser` (str): BeautifulSoup parser ('html.parser', 'lxml', 'xml')
- `custom_headers` (dict, optional): Additional headers for the request

**Returns:** Dictionary containing:
- `url`: Original URL
- `status_code`: HTTP status code
- `title`: Page title
- `meta_description`: Meta description
- `headings`: Dictionary of headings by level
- `links`: List of found links
- `images`: List of found images
- `text_content`: Plain text content
- `html_content`: Raw HTML content
- `timestamp`: Scraping timestamp

#### scrape_dynamic_content()

```python
scrape_dynamic_content(url, wait_element=None, wait_time=10)
```

Scrape dynamic web content using Selenium WebDriver.

**Parameters:**
- `url` (str): URL to scrape
- `wait_element` (str, optional): CSS selector to wait for before scraping
- `wait_time` (int): Maximum time to wait for element

**Returns:** Dictionary with similar structure to `scrape_static_content()`

#### init_selenium_driver()

```python
init_selenium_driver(browser='chrome', headless=True)
```

Initialize Selenium WebDriver for dynamic content scraping.

**Parameters:**
- `browser` (str): Browser type ('chrome' or 'firefox')
- `headless` (bool): Run browser in headless mode

**Returns:** `bool` - True if driver initialized successfully

#### extract_data_by_selector()

```python
extract_data_by_selector(url, selectors, use_selenium=False)
```

Extract specific data using CSS selectors.

**Parameters:**
- `url` (str): URL to scrape
- `selectors` (dict): Dictionary mapping field names to CSS selectors
- `use_selenium` (bool): Whether to use Selenium for dynamic content

**Returns:** Dictionary containing extracted data

#### save_scraped_data()

```python
save_scraped_data(data, filename, format='json')
```

Save scraped data to file.

**Parameters:**
- `data` (dict): Data to save
- `filename` (str): Output filename
- `format` (str): Output format ('json', 'txt')

#### cleanup()

```python
cleanup()
```

Clean up resources and close browser driver.

## Command Line Interface

### Commands

#### clone

```bash
ai-time-machines clone <url> [options]
```

Clone a git repository.

**Options:**
- `--destination, -d`: Local destination path
- `--branch, -b`: Specific branch to clone
- `--depth`: Depth of clone (shallow clone)
- `--single-branch`: Clone only single branch
- `--base-dir`: Base directory for repositories
- `--info`: Show repository information after cloning

#### list

```bash
ai-time-machines list [options]
```

List cloned repositories.

**Options:**
- `--base-dir`: Base directory for repositories

#### scrape

```bash
ai-time-machines scrape <url> [options]
```

Scrape a website.

**Options:**
- `--dynamic`: Use Selenium for dynamic content
- `--parser`: HTML parser to use (html.parser, lxml, xml)
- `--wait-element`: CSS selector to wait for (dynamic scraping)
- `--wait-time`: Time to wait for element (seconds)
- `--delay`: Delay between requests (seconds)
- `--timeout`: Request timeout (seconds)
- `--output, -o`: Output file path
- `--format`: Output format (json, txt)
- `--show-links`: Display found links

#### extract

```bash
ai-time-machines extract <url> <selectors> [options]
```

Extract specific data using CSS selectors.

**Parameters:**
- `url`: URL to scrape
- `selectors`: JSON string mapping field names to CSS selectors

**Options:**
- `--dynamic`: Use Selenium for dynamic content
- `--delay`: Delay between requests (seconds)
- `--timeout`: Request timeout (seconds)
- `--output, -o`: Output file path
- `--format`: Output format (json, txt)

## Error Handling

### Exceptions

- `GitCommandError`: Git operation failed
- `requests.RequestException`: HTTP request failed
- `selenium.common.exceptions.WebDriverException`: WebDriver error
- `ValueError`: Invalid parameter provided

### Error Response Format

```python
{
    "error": "Error description",
    "url": "Original URL",
    "timestamp": 1234567890.123
}
```

## Configuration

### Environment Variables

- `AI_TM_BASE_DIR`: Default base directory for repositories
- `AI_TM_USER_AGENT`: Default user agent for web scraping
- `AI_TM_DEFAULT_DELAY`: Default delay between requests
- `AI_TM_LOG_LEVEL`: Default logging level

### Logging Levels

- `DEBUG`: Detailed debugging information
- `INFO`: General information messages
- `WARNING`: Warning messages
- `ERROR`: Error messages
- `CRITICAL`: Critical error messages