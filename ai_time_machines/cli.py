"""
Command-line interface for AI Time Machines.

This module provides a CLI interface for the cloning and web scraping functionality.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from .cloning import RepositoryCloner
from .scraping import WebScraper


def clone_repository_command(args):
    """Handle repository cloning command."""
    cloner = RepositoryCloner(base_dir=args.base_dir)
    
    try:
        repo = cloner.clone_repository(
            repo_url=args.url,
            destination=args.destination,
            branch=args.branch,
            depth=args.depth,
            single_branch=args.single_branch
        )
        
        print(f"✅ Successfully cloned repository to: {repo.working_dir}")
        
        if args.info:
            info = cloner.get_repository_info(repo.working_dir)
            print(f"📊 Repository Information:")
            print(f"   Current branch: {info['current_branch']}")
            print(f"   Available branches: {', '.join(info['branches'])}")
            print(f"   Latest commit: {info['latest_commit']['message'][:50]}...")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        cloner.cleanup()


def list_repositories_command(args):
    """Handle list repositories command."""
    cloner = RepositoryCloner(base_dir=args.base_dir)
    
    try:
        repos = cloner.list_cloned_repositories()
        
        if not repos:
            print("No repositories found in the base directory.")
            return
        
        print(f"📁 Found {len(repos)} repositories:")
        for repo in repos:
            if 'error' in repo:
                print(f"   ❌ {repo.get('path', 'Unknown')}: {repo['error']}")
            else:
                print(f"   📂 {repo['path']}")
                print(f"      Branch: {repo['current_branch']}")
                print(f"      Latest: {repo['latest_commit']['message'][:50]}...")
                if repo['is_dirty']:
                    print("      ⚠️  Repository has uncommitted changes")
                print()
                
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def scrape_website_command(args):
    """Handle web scraping command."""
    scraper = WebScraper(delay=args.delay, timeout=args.timeout)
    
    try:
        if args.dynamic:
            data = scraper.scrape_dynamic_content(
                url=args.url,
                wait_element=args.wait_element,
                wait_time=args.wait_time
            )
        else:
            data = scraper.scrape_static_content(
                url=args.url,
                parser=args.parser
            )
        
        if 'error' in data:
            print(f"❌ Error scraping {args.url}: {data['error']}")
            sys.exit(1)
        
        print(f"✅ Successfully scraped: {args.url}")
        print(f"   Title: {data.get('title', 'N/A')}")
        print(f"   Links found: {len(data.get('links', []))}")
        print(f"   Images found: {len(data.get('images', []))}")
        
        if args.output:
            scraper.save_scraped_data(data, args.output, args.format)
            print(f"💾 Data saved to: {args.output}")
        
        if args.show_links and data.get('links'):
            print(f"\n🔗 Links found:")
            for i, link in enumerate(data['links'][:10], 1):  # Show first 10 links
                print(f"   {i}. {link['text'][:50]}... -> {link['absolute_url']}")
            if len(data['links']) > 10:
                print(f"   ... and {len(data['links']) - 10} more links")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        scraper.cleanup()


def extract_data_command(args):
    """Handle data extraction command."""
    scraper = WebScraper(delay=args.delay, timeout=args.timeout)
    
    try:
        # Parse selectors from JSON
        selectors = json.loads(args.selectors)
        
        data = scraper.extract_data_by_selector(
            url=args.url,
            selectors=selectors,
            use_selenium=args.dynamic
        )
        
        if 'error' in data:
            print(f"❌ Error extracting data from {args.url}: {data['error']}")
            sys.exit(1)
        
        print(f"✅ Successfully extracted data from: {args.url}")
        for key, value in data.items():
            if key not in ['url', 'timestamp']:
                print(f"   {key}: {value}")
        
        if args.output:
            scraper.save_scraped_data(data, args.output, args.format)
            print(f"💾 Data saved to: {args.output}")
            
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON format for selectors")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        scraper.cleanup()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI Time Machines - Git cloning and web scraping utilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Clone a repository
  ai-time-machines clone https://github.com/user/repo.git

  # Clone a specific branch
  ai-time-machines clone https://github.com/user/repo.git --branch main

  # List cloned repositories
  ai-time-machines list

  # Scrape a website
  ai-time-machines scrape https://example.com

  # Scrape with dynamic content
  ai-time-machines scrape https://example.com --dynamic

  # Extract specific data using CSS selectors
  ai-time-machines extract https://example.com '{"title": "h1", "links": "a"}'
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Clone command
    clone_parser = subparsers.add_parser('clone', help='Clone a git repository')
    clone_parser.add_argument('url', help='Repository URL to clone')
    clone_parser.add_argument('--destination', '-d', help='Local destination path')
    clone_parser.add_argument('--branch', '-b', help='Specific branch to clone')
    clone_parser.add_argument('--depth', type=int, help='Depth of clone (shallow clone)')
    clone_parser.add_argument('--single-branch', action='store_true', help='Clone only single branch')
    clone_parser.add_argument('--base-dir', default='./repositories', help='Base directory for repositories')
    clone_parser.add_argument('--info', action='store_true', help='Show repository information after cloning')
    clone_parser.set_defaults(func=clone_repository_command)
    
    # List command
    list_parser = subparsers.add_parser('list', help='List cloned repositories')
    list_parser.add_argument('--base-dir', default='./repositories', help='Base directory for repositories')
    list_parser.set_defaults(func=list_repositories_command)
    
    # Scrape command
    scrape_parser = subparsers.add_parser('scrape', help='Scrape a website')
    scrape_parser.add_argument('url', help='URL to scrape')
    scrape_parser.add_argument('--dynamic', action='store_true', help='Use Selenium for dynamic content')
    scrape_parser.add_argument('--parser', default='html.parser', choices=['html.parser', 'lxml', 'xml'], help='HTML parser to use')
    scrape_parser.add_argument('--wait-element', help='CSS selector to wait for (dynamic scraping)')
    scrape_parser.add_argument('--wait-time', type=int, default=10, help='Time to wait for element (seconds)')
    scrape_parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests (seconds)')
    scrape_parser.add_argument('--timeout', type=int, default=30, help='Request timeout (seconds)')
    scrape_parser.add_argument('--output', '-o', help='Output file path')
    scrape_parser.add_argument('--format', choices=['json', 'txt'], default='json', help='Output format')
    scrape_parser.add_argument('--show-links', action='store_true', help='Display found links')
    scrape_parser.set_defaults(func=scrape_website_command)
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract specific data using CSS selectors')
    extract_parser.add_argument('url', help='URL to scrape')
    extract_parser.add_argument('selectors', help='JSON string mapping field names to CSS selectors')
    extract_parser.add_argument('--dynamic', action='store_true', help='Use Selenium for dynamic content')
    extract_parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests (seconds)')
    extract_parser.add_argument('--timeout', type=int, default=30, help='Request timeout (seconds)')
    extract_parser.add_argument('--output', '-o', help='Output file path')
    extract_parser.add_argument('--format', choices=['json', 'txt'], default='json', help='Output format')
    extract_parser.set_defaults(func=extract_data_command)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()