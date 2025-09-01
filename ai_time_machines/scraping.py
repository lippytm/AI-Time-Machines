"""
Web scraping functionality for AI Time Machines.

This module provides comprehensive web scraping capabilities with support for
various parsing methods and data extraction techniques.
"""

import requests
import logging
import time
import json
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class WebScraper:
    """
    A comprehensive web scraping utility with support for both static and dynamic content.
    
    This class provides functionality to scrape websites using requests/BeautifulSoup
    for static content and Selenium for dynamic content that requires JavaScript execution.
    """
    
    def __init__(self, 
                 user_agent: Optional[str] = None,
                 delay: float = 1.0,
                 timeout: int = 30,
                 log_level: int = logging.INFO):
        """
        Initialize the WebScraper.
        
        Args:
            user_agent: Custom user agent string
            delay: Delay between requests in seconds
            timeout: Request timeout in seconds
            log_level: Logging level for operations
        """
        self.delay = delay
        self.timeout = timeout
        
        # Setup logging
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger(__name__)
        
        # Setup session with headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent or 'AI-Time-Machines/1.0 (Educational Web Scraper)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        # Selenium driver (initialized when needed)
        self.driver = None
        self.driver_type = None
    
    def scrape_static_content(self, 
                            url: str, 
                            parser: str = 'html.parser',
                            custom_headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Scrape static web content using requests and BeautifulSoup.
        
        Args:
            url: URL to scrape
            parser: BeautifulSoup parser ('html.parser', 'lxml', 'xml')
            custom_headers: Additional headers for the request
            
        Returns:
            Dictionary containing scraped data and metadata
        """
        try:
            self.logger.info(f"Scraping static content from {url}")
            
            # Prepare headers
            headers = {}
            if custom_headers:
                headers.update(custom_headers)
            
            # Make request
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            
            # Parse content
            soup = BeautifulSoup(response.content, parser)
            
            # Extract basic information
            result = {
                'url': url,
                'status_code': response.status_code,
                'title': soup.title.string.strip() if soup.title else None,
                'meta_description': None,
                'headings': {},
                'links': [],
                'images': [],
                'text_content': soup.get_text().strip(),
                'html_content': str(soup),
                'timestamp': time.time()
            }
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                result['meta_description'] = meta_desc.get('content', '').strip()
            
            # Extract headings
            for level in range(1, 7):
                headings = soup.find_all(f'h{level}')
                if headings:
                    result['headings'][f'h{level}'] = [h.get_text().strip() for h in headings]
            
            # Extract links
            for link in soup.find_all('a', href=True):
                href = link['href']
                absolute_url = urljoin(url, href)
                result['links'].append({
                    'text': link.get_text().strip(),
                    'href': href,
                    'absolute_url': absolute_url
                })
            
            # Extract images
            for img in soup.find_all('img', src=True):
                src = img['src']
                absolute_url = urljoin(url, src)
                result['images'].append({
                    'alt': img.get('alt', ''),
                    'src': src,
                    'absolute_url': absolute_url
                })
            
            self.logger.info(f"Successfully scraped {len(result['links'])} links and {len(result['images'])} images")
            
            # Add delay
            time.sleep(self.delay)
            
            return result
            
        except requests.RequestException as e:
            self.logger.error(f"Request failed for {url}: {e}")
            return {'error': f'Request failed: {e}', 'url': url, 'timestamp': time.time()}
        except Exception as e:
            self.logger.error(f"Unexpected error scraping {url}: {e}")
            return {'error': f'Unexpected error: {e}', 'url': url, 'timestamp': time.time()}
    
    def init_selenium_driver(self, browser: str = 'chrome', headless: bool = True) -> bool:
        """
        Initialize Selenium WebDriver for dynamic content scraping.
        
        Args:
            browser: Browser type ('chrome' or 'firefox')
            headless: Run browser in headless mode
            
        Returns:
            True if driver initialized successfully, False otherwise
        """
        try:
            if browser.lower() == 'chrome':
                options = ChromeOptions()
                if headless:
                    options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                self.driver = webdriver.Chrome(options=options)
            elif browser.lower() == 'firefox':
                options = FirefoxOptions()
                if headless:
                    options.add_argument('--headless')
                self.driver = webdriver.Firefox(options=options)
            else:
                raise ValueError(f"Unsupported browser: {browser}")
            
            self.driver_type = browser.lower()
            self.driver.set_page_load_timeout(self.timeout)
            self.logger.info(f"Initialized {browser} WebDriver")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {e}")
            return False
    
    def scrape_dynamic_content(self, 
                             url: str,
                             wait_element: Optional[str] = None,
                             wait_time: int = 10) -> Dict[str, Any]:
        """
        Scrape dynamic web content using Selenium WebDriver.
        
        Args:
            url: URL to scrape
            wait_element: CSS selector to wait for before scraping
            wait_time: Maximum time to wait for element
            
        Returns:
            Dictionary containing scraped data and metadata
        """
        if not self.driver:
            if not self.init_selenium_driver():
                return {'error': 'Failed to initialize WebDriver', 'url': url, 'timestamp': time.time()}
        
        try:
            self.logger.info(f"Scraping dynamic content from {url}")
            
            # Load page
            self.driver.get(url)
            
            # Wait for specific element if provided
            if wait_element:
                wait = WebDriverWait(self.driver, wait_time)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, wait_element)))
            
            # Get page source and parse with BeautifulSoup
            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract information (similar to static scraping)
            result = {
                'url': url,
                'title': self.driver.title,
                'current_url': self.driver.current_url,
                'meta_description': None,
                'headings': {},
                'links': [],
                'images': [],
                'text_content': soup.get_text().strip(),
                'html_content': html_content,
                'timestamp': time.time()
            }
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                result['meta_description'] = meta_desc.get('content', '').strip()
            
            # Extract headings
            for level in range(1, 7):
                headings = soup.find_all(f'h{level}')
                if headings:
                    result['headings'][f'h{level}'] = [h.get_text().strip() for h in headings]
            
            # Extract links
            for link in soup.find_all('a', href=True):
                href = link['href']
                absolute_url = urljoin(url, href)
                result['links'].append({
                    'text': link.get_text().strip(),
                    'href': href,
                    'absolute_url': absolute_url
                })
            
            # Extract images
            for img in soup.find_all('img', src=True):
                src = img['src']
                absolute_url = urljoin(url, src)
                result['images'].append({
                    'alt': img.get('alt', ''),
                    'src': src,
                    'absolute_url': absolute_url
                })
            
            self.logger.info(f"Successfully scraped dynamic content with {len(result['links'])} links")
            
            # Add delay
            time.sleep(self.delay)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to scrape dynamic content from {url}: {e}")
            return {'error': f'Failed to scrape: {e}', 'url': url, 'timestamp': time.time()}
    
    def extract_data_by_selector(self, 
                               url: str, 
                               selectors: Dict[str, str],
                               use_selenium: bool = False) -> Dict[str, Any]:
        """
        Extract specific data using CSS selectors.
        
        Args:
            url: URL to scrape
            selectors: Dictionary mapping field names to CSS selectors
            use_selenium: Whether to use Selenium for dynamic content
            
        Returns:
            Dictionary containing extracted data
        """
        try:
            if use_selenium:
                data = self.scrape_dynamic_content(url)
                if 'error' in data:
                    return data
                soup = BeautifulSoup(data['html_content'], 'html.parser')
            else:
                data = self.scrape_static_content(url)
                if 'error' in data:
                    return data
                soup = BeautifulSoup(data['html_content'], 'html.parser')
            
            extracted_data = {'url': url, 'timestamp': time.time()}
            
            for field_name, selector in selectors.items():
                elements = soup.select(selector)
                if elements:
                    if len(elements) == 1:
                        extracted_data[field_name] = elements[0].get_text().strip()
                    else:
                        extracted_data[field_name] = [elem.get_text().strip() for elem in elements]
                else:
                    extracted_data[field_name] = None
            
            return extracted_data
            
        except Exception as e:
            self.logger.error(f"Failed to extract data from {url}: {e}")
            return {'error': f'Extraction failed: {e}', 'url': url, 'timestamp': time.time()}
    
    def save_scraped_data(self, data: Dict[str, Any], filename: str, format: str = 'json'):
        """
        Save scraped data to file.
        
        Args:
            data: Data to save
            filename: Output filename
            format: Output format ('json', 'txt')
        """
        try:
            output_path = Path(filename)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if format.lower() == 'json':
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            elif format.lower() == 'txt':
                with open(output_path, 'w', encoding='utf-8') as f:
                    if isinstance(data, dict):
                        for key, value in data.items():
                            f.write(f"{key}: {value}\n")
                    else:
                        f.write(str(data))
            
            self.logger.info(f"Saved scraped data to {output_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to save data to {filename}: {e}")
    
    def cleanup(self):
        """Clean up resources and close browser driver."""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.logger.info("Closed WebDriver")
        
        self.session.close()
        self.logger.info("Closed requests session")