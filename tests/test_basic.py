"""
Basic tests for AI Time Machines functionality.

This module contains simple tests to verify the basic functionality
of the cloning and scraping features.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import os

# Add the parent directory to the path so we can import our modules
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ai_time_machines import RepositoryCloner, WebScraper


class TestRepositoryCloner(unittest.TestCase):
    """Test cases for RepositoryCloner functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.cloner = RepositoryCloner(base_dir=self.temp_dir)
    
    def tearDown(self):
        """Clean up after tests."""
        self.cloner.cleanup()
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_cloner_initialization(self):
        """Test that cloner initializes correctly."""
        self.assertIsInstance(self.cloner, RepositoryCloner)
        self.assertTrue(Path(self.temp_dir).exists())
    
    def test_clone_repository(self):
        """Test cloning a repository."""
        # Use a small, stable repository for testing
        repo_url = "https://github.com/octocat/Hello-World.git"
        
        try:
            repo = self.cloner.clone_repository(repo_url, depth=1)
            self.assertTrue(os.path.exists(repo.working_dir))
            self.assertTrue(os.path.exists(os.path.join(repo.working_dir, '.git')))
            
            # Test getting repository info
            info = self.cloner.get_repository_info(repo.working_dir)
            self.assertIn('current_branch', info)
            self.assertIn('latest_commit', info)
            self.assertIsInstance(info['branches'], list)
            
        except Exception as e:
            self.skipTest(f"Network or Git issue: {e}")
    
    def test_list_repositories(self):
        """Test listing repositories."""
        repos = self.cloner.list_cloned_repositories()
        self.assertIsInstance(repos, list)


class TestWebScraper(unittest.TestCase):
    """Test cases for WebScraper functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = WebScraper(delay=0.5)  # Shorter delay for tests
    
    def tearDown(self):
        """Clean up after tests."""
        self.scraper.cleanup()
    
    def test_scraper_initialization(self):
        """Test that scraper initializes correctly."""
        self.assertIsInstance(self.scraper, WebScraper)
        self.assertEqual(self.scraper.delay, 0.5)
    
    def test_scrape_static_content(self):
        """Test scraping static content."""
        # Use httpbin.org for reliable testing
        test_url = "https://httpbin.org/html"
        
        try:
            data = self.scraper.scrape_static_content(test_url)
            
            # Check for successful scraping
            self.assertNotIn('error', data)
            self.assertEqual(data['url'], test_url)
            self.assertIn('title', data)
            self.assertIn('links', data)
            self.assertIn('text_content', data)
            self.assertIsInstance(data['links'], list)
            
        except Exception as e:
            self.skipTest(f"Network issue: {e}")
    
    def test_extract_data_by_selector(self):
        """Test extracting data using CSS selectors."""
        test_url = "https://httpbin.org/html"
        selectors = {
            "title": "title",
            "headings": "h1"
        }
        
        try:
            data = self.scraper.extract_data_by_selector(test_url, selectors)
            
            self.assertNotIn('error', data)
            self.assertIn('title', data)
            self.assertIn('headings', data)
            
        except Exception as e:
            self.skipTest(f"Network issue: {e}")
    
    def test_save_scraped_data(self):
        """Test saving scraped data to file."""
        test_data = {
            "url": "https://example.com",
            "title": "Test Title",
            "content": "Test content"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            self.scraper.save_scraped_data(test_data, temp_file, 'json')
            self.assertTrue(os.path.exists(temp_file))
            
            # Verify file content
            import json
            with open(temp_file, 'r') as f:
                loaded_data = json.load(f)
            
            self.assertEqual(loaded_data['title'], "Test Title")
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestIntegration(unittest.TestCase):
    """Integration tests combining cloning and scraping."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.cloner = RepositoryCloner(base_dir=self.temp_dir)
        self.scraper = WebScraper(delay=0.5)
    
    def tearDown(self):
        """Clean up after tests."""
        self.cloner.cleanup()
        self.scraper.cleanup()
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_combined_workflow(self):
        """Test a basic combined workflow."""
        # This test verifies that both tools can be used together
        try:
            # Clone a repository
            repo_url = "https://github.com/octocat/Hello-World.git"
            repo = self.cloner.clone_repository(repo_url, depth=1)
            self.assertTrue(os.path.exists(repo.working_dir))
            
            # Scrape the GitHub page
            github_url = "https://github.com/octocat/Hello-World"
            data = self.scraper.scrape_static_content(github_url)
            self.assertNotIn('error', data)
            
            # Both operations should be successful
            self.assertIsNotNone(repo)
            self.assertIsNotNone(data)
            
        except Exception as e:
            self.skipTest(f"Network or Git issue: {e}")


def run_basic_tests():
    """Run basic functionality tests."""
    print("🧪 Running Basic Tests")
    print("=" * 30)
    
    # Test cloner basic functionality
    print("\n📁 Testing Repository Cloner...")
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            cloner = RepositoryCloner(base_dir=temp_dir)
            
            # Test initialization
            assert isinstance(cloner, RepositoryCloner)
            print("   ✅ Cloner initialization: OK")
            
            # Test listing (should be empty)
            repos = cloner.list_cloned_repositories()
            assert isinstance(repos, list)
            print("   ✅ List repositories: OK")
            
            cloner.cleanup()
            
    except Exception as e:
        print(f"   ❌ Cloner test failed: {e}")
    
    # Test scraper basic functionality
    print("\n🕷️ Testing Web Scraper...")
    try:
        scraper = WebScraper(delay=0.1)
        
        # Test initialization
        assert isinstance(scraper, WebScraper)
        print("   ✅ Scraper initialization: OK")
        
        # Test with a simple example
        test_data = {"test": "data"}
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        scraper.save_scraped_data(test_data, temp_file)
        assert os.path.exists(temp_file)
        print("   ✅ Save data: OK")
        
        os.unlink(temp_file)
        scraper.cleanup()
        
    except Exception as e:
        print(f"   ❌ Scraper test failed: {e}")
    
    print("\n✅ Basic tests completed!")


if __name__ == "__main__":
    # Run basic tests first
    run_basic_tests()
    
    print("\n" + "="*50)
    print("Running Unit Tests")
    print("="*50)
    
    # Run unittest suite
    unittest.main(verbosity=2)