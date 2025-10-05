"""
Basic web scraping example.

This example demonstrates how to scrape websites and extract information.
"""

from ai_time_machines import WebScraper
import json


def main():
    """Scrape a sample website and display results."""
    
    # Initialize the scraper
    scraper = WebScraper(delay=1.0, timeout=30)
    
    # URL to scrape (using a test site)
    url = "https://httpbin.org/html"
    
    try:
        print(f"🕷️ Scraping website: {url}")
        
        # Scrape static content
        data = scraper.scrape_static_content(url)
        
        if 'error' in data:
            print(f"❌ Error: {data['error']}")
            return
        
        print(f"✅ Successfully scraped website")
        
        # Display basic information
        print("\n📊 Scraped Information:")
        print(f"   Title: {data['title']}")
        print(f"   Status code: {data['status_code']}")
        print(f"   Meta description: {data.get('meta_description', 'N/A')}")
        print(f"   Number of links: {len(data['links'])}")
        print(f"   Number of images: {len(data['images'])}")
        
        # Display headings
        if data['headings']:
            print("\n📑 Headings found:")
            for level, headings in data['headings'].items():
                for heading in headings:
                    print(f"   {level.upper()}: {heading}")
        
        # Display first few links
        if data['links']:
            print("\n🔗 Links found (first 5):")
            for i, link in enumerate(data['links'][:5], 1):
                print(f"   {i}. {link['text'][:50]}{'...' if len(link['text']) > 50 else ''}")
                print(f"      URL: {link['absolute_url']}")
        
        # Display text content preview
        if data['text_content']:
            text_preview = data['text_content'][:200].replace('\n', ' ')
            print(f"\n📝 Text content preview:")
            print(f"   {text_preview}{'...' if len(data['text_content']) > 200 else ''}")
        
        # Save scraped data
        scraper.save_scraped_data(data, "scraped_data.json")
        print(f"\n💾 Scraped data saved to scraped_data.json")
        
        # Example of extracting specific data using CSS selectors
        print(f"\n🎯 Extracting specific data with CSS selectors...")
        
        selectors = {
            "title": "title",
            "headings": "h1, h2, h3",
            "paragraphs": "p"
        }
        
        extracted_data = scraper.extract_data_by_selector(url, selectors)
        
        if 'error' not in extracted_data:
            print("   Extracted data:")
            for key, value in extracted_data.items():
                if key not in ['url', 'timestamp']:
                    if isinstance(value, list):
                        print(f"   {key}: {len(value)} items found")
                        if value:
                            print(f"      First item: {value[0][:50]}{'...' if len(value[0]) > 50 else ''}")
                    else:
                        print(f"   {key}: {value}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Clean up resources
        scraper.cleanup()
        print("\n🧹 Cleaned up resources")


def advanced_example():
    """Demonstrate advanced scraping features."""
    
    print("\n" + "="*50)
    print("Advanced Scraping Example")
    print("="*50)
    
    scraper = WebScraper(delay=2.0)
    
    # Example with custom headers
    custom_headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache'
    }
    
    try:
        # Scrape with custom headers
        data = scraper.scrape_static_content(
            "https://httpbin.org/headers",
            custom_headers=custom_headers
        )
        
        if 'error' not in data:
            print("✅ Successfully scraped with custom headers")
            print(f"   Title: {data.get('title', 'N/A')}")
            
            # The httpbin.org/headers endpoint returns JSON showing the headers
            # Let's look for specific content in the text
            if 'Accept-Language' in data['text_content']:
                print("   ✅ Custom headers were sent successfully")
            else:
                print("   ⚠️ Custom headers might not have been applied")
    
    except Exception as e:
        print(f"❌ Advanced example error: {e}")
    
    finally:
        scraper.cleanup()


if __name__ == "__main__":
    main()
    advanced_example()