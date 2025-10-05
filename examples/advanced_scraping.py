"""
Advanced scraping example with dynamic content.

This example demonstrates how to scrape dynamic websites that require JavaScript.
Note: This requires a web browser (Chrome/Firefox) to be installed.
"""

from ai_time_machines import WebScraper
import json
import time


def main():
    """Demonstrate dynamic content scraping."""
    
    # Initialize scraper for dynamic content
    scraper = WebScraper(delay=2.0, timeout=60)
    
    print("🚀 Advanced Scraping Example - Dynamic Content")
    print("=" * 50)
    
    # Example 1: Basic dynamic scraping
    try:
        print("\n📱 Example 1: Basic Dynamic Scraping")
        print("-" * 30)
        
        # Initialize Selenium driver
        if scraper.init_selenium_driver(browser='chrome', headless=True):
            print("✅ WebDriver initialized successfully")
            
            # Scrape a site that loads content dynamically
            # Using httpbin.org which serves static content for testing
            url = "https://httpbin.org/html"
            
            data = scraper.scrape_dynamic_content(url)
            
            if 'error' not in data:
                print(f"✅ Successfully scraped dynamic content from: {url}")
                print(f"   Title: {data['title']}")
                print(f"   Current URL: {data['current_url']}")
                print(f"   Content loaded via JavaScript: {'script' in data['html_content'].lower()}")
            else:
                print(f"❌ Error scraping dynamic content: {data['error']}")
        else:
            print("❌ Failed to initialize WebDriver")
            print("   Make sure Chrome or Firefox is installed")
            return
            
    except Exception as e:
        print(f"❌ Error in dynamic scraping: {e}")
    
    # Example 2: Waiting for specific elements
    try:
        print("\n⏳ Example 2: Waiting for Specific Elements")
        print("-" * 40)
        
        # Scrape and wait for specific element to load
        data = scraper.scrape_dynamic_content(
            url="https://httpbin.org/delay/2",  # This endpoint has a 2-second delay
            wait_element="body",  # Wait for body element
            wait_time=10
        )
        
        if 'error' not in data:
            print("✅ Successfully waited for element and scraped content")
            print(f"   Page loaded after delay")
        else:
            print(f"❌ Error waiting for element: {data['error']}")
            
    except Exception as e:
        print(f"❌ Error in element waiting: {e}")
    
    # Example 3: Advanced data extraction
    try:
        print("\n🎯 Example 3: Advanced Data Extraction")
        print("-" * 35)
        
        # Define complex selectors for data extraction
        selectors = {
            "page_title": "title",
            "main_heading": "h1",
            "all_paragraphs": "p",
            "links": "a[href]",
            "meta_description": "meta[name='description']"
        }
        
        extracted_data = scraper.extract_data_by_selector(
            url="https://httpbin.org/html",
            selectors=selectors,
            use_selenium=True
        )
        
        if 'error' not in extracted_data:
            print("✅ Successfully extracted structured data")
            for key, value in extracted_data.items():
                if key not in ['url', 'timestamp']:
                    if isinstance(value, list) and value:
                        print(f"   {key}: {len(value)} items")
                        print(f"      Example: {value[0][:50]}{'...' if len(value[0]) > 50 else ''}")
                    elif value:
                        print(f"   {key}: {value[:50]}{'...' if len(str(value)) > 50 else ''}")
                    else:
                        print(f"   {key}: Not found")
            
            # Save extracted data
            scraper.save_scraped_data(extracted_data, "advanced_scraped_data.json")
            print("💾 Advanced data saved to advanced_scraped_data.json")
        else:
            print(f"❌ Error extracting data: {extracted_data['error']}")
            
    except Exception as e:
        print(f"❌ Error in advanced extraction: {e}")
    
    # Example 4: Multiple page scraping simulation
    try:
        print("\n📚 Example 4: Multiple Page Scraping Simulation")
        print("-" * 45)
        
        urls = [
            "https://httpbin.org/html",
            "https://httpbin.org/json",
            "https://httpbin.org/xml"
        ]
        
        all_data = []
        
        for url in urls:
            print(f"   Scraping: {url}")
            
            # Use static scraping for JSON/XML endpoints
            if '/json' in url or '/xml' in url:
                data = scraper.scrape_static_content(url)
            else:
                data = scraper.scrape_dynamic_content(url)
            
            if 'error' not in data:
                # Store minimal info to avoid huge output
                summary = {
                    'url': data['url'],
                    'title': data.get('title', 'N/A'),
                    'status': 'success',
                    'content_length': len(data.get('text_content', '')),
                    'links_count': len(data.get('links', [])),
                    'timestamp': data.get('timestamp')
                }
                all_data.append(summary)
                print(f"      ✅ Success - {summary['content_length']} chars, {summary['links_count']} links")
            else:
                print(f"      ❌ Error: {data['error']}")
            
            # Be respectful with delays
            time.sleep(1)
        
        # Save summary data
        with open("multiple_pages_summary.json", "w") as f:
            json.dump(all_data, f, indent=2, default=str)
        
        print(f"✅ Scraped {len(all_data)} pages successfully")
        print("💾 Summary saved to multiple_pages_summary.json")
        
    except Exception as e:
        print(f"❌ Error in multiple page scraping: {e}")
    
    finally:
        # Always clean up
        scraper.cleanup()
        print("\n🧹 Cleaned up all resources")


def custom_scraper_example():
    """Demonstrate creating a custom scraper class."""
    
    print("\n" + "="*50)
    print("Custom Scraper Class Example")
    print("="*50)
    
    class NewsArticleScraper(WebScraper):
        """Custom scraper for news articles."""
        
        def scrape_article(self, url):
            """Extract article-specific information."""
            selectors = {
                "headline": "h1, .headline, .title",
                "author": ".author, .byline, [data-author]",
                "publish_date": ".date, .publish-date, time",
                "content": ".content p, .article-body p, main p"
            }
            
            return self.extract_data_by_selector(url, selectors, use_selenium=True)
        
        def get_article_summary(self, url):
            """Get a summary of the article."""
            data = self.scrape_article(url)
            
            if 'error' in data:
                return data
            
            # Create summary
            summary = {
                'url': url,
                'headline': data.get('headline'),
                'author': data.get('author'),
                'date': data.get('publish_date'),
                'content_preview': None,
                'word_count': 0
            }
            
            # Process content
            if data.get('content') and isinstance(data['content'], list):
                full_content = ' '.join(data['content'])
                summary['content_preview'] = full_content[:200] + '...' if len(full_content) > 200 else full_content
                summary['word_count'] = len(full_content.split())
            
            return summary
    
    # Use the custom scraper
    try:
        news_scraper = NewsArticleScraper()
        
        # Since we don't have access to real news sites in this example,
        # we'll use httpbin.org to demonstrate the concept
        test_url = "https://httpbin.org/html"
        
        print(f"📰 Testing custom news scraper on: {test_url}")
        
        summary = news_scraper.get_article_summary(test_url)
        
        if 'error' not in summary:
            print("✅ Custom scraper worked successfully")
            print(f"   URL: {summary['url']}")
            print(f"   Headline: {summary.get('headline', 'Not found')}")
            print(f"   Author: {summary.get('author', 'Not found')}")
            print(f"   Date: {summary.get('publish_date', 'Not found')}")
            print(f"   Word count: {summary['word_count']}")
            if summary.get('content_preview'):
                print(f"   Content preview: {summary['content_preview']}")
        else:
            print(f"❌ Custom scraper error: {summary['error']}")
        
        news_scraper.cleanup()
        
    except Exception as e:
        print(f"❌ Error in custom scraper: {e}")


if __name__ == "__main__":
    main()
    custom_scraper_example()