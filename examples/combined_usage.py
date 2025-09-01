"""
Combined example showcasing both cloning and scraping capabilities.

This example demonstrates how to clone repositories and then scrape
documentation or project websites for additional information.
"""

from ai_time_machines import RepositoryCloner, WebScraper
import json
import os
from pathlib import Path


def main():
    """Demonstrate combined cloning and scraping workflow."""
    
    print("🔄 Combined Example: Repository Cloning + Web Scraping")
    print("=" * 60)
    
    # Initialize both tools
    cloner = RepositoryCloner(base_dir="./combined_example")
    scraper = WebScraper(delay=1.5, timeout=45)
    
    # Repository information with associated websites
    projects = [
        {
            "name": "Hello-World",
            "repo_url": "https://github.com/octocat/Hello-World.git",
            "website": "https://github.com/octocat/Hello-World",
            "description": "GitHub's Hello World repository"
        }
    ]
    
    results = []
    
    for project in projects:
        print(f"\n📦 Processing project: {project['name']}")
        print("-" * 40)
        
        project_result = {
            "name": project['name'],
            "repo_info": None,
            "website_data": None,
            "status": "pending"
        }
        
        try:
            # Step 1: Clone the repository
            print(f"🔄 Cloning repository: {project['repo_url']}")
            
            repo = cloner.clone_repository(
                project['repo_url'],
                single_branch=True,  # Only clone main branch for speed
                depth=1  # Shallow clone
            )
            
            print(f"✅ Repository cloned to: {repo.working_dir}")
            
            # Get repository information
            repo_info = cloner.get_repository_info(repo.working_dir)
            project_result["repo_info"] = {
                "path": repo_info["path"],
                "current_branch": repo_info["current_branch"],
                "latest_commit": repo_info["latest_commit"]["message"][:100],
                "commit_author": repo_info["latest_commit"]["author"],
                "is_dirty": repo_info["is_dirty"]
            }
            
            # Check for README file
            readme_path = Path(repo.working_dir) / "README.md"
            if readme_path.exists():
                with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                    readme_content = f.read()[:500]  # First 500 characters
                project_result["repo_info"]["readme_preview"] = readme_content
                print(f"   📄 README.md found ({len(readme_content)} characters)")
            
            # Step 2: Scrape the project website
            if project.get('website'):
                print(f"🕷️ Scraping project website: {project['website']}")
                
                website_data = scraper.scrape_static_content(project['website'])
                
                if 'error' not in website_data:
                    print(f"✅ Website scraped successfully")
                    
                    # Extract relevant information
                    project_result["website_data"] = {
                        "title": website_data.get("title"),
                        "meta_description": website_data.get("meta_description"),
                        "links_count": len(website_data.get("links", [])),
                        "images_count": len(website_data.get("images", [])),
                        "text_preview": website_data.get("text_content", "")[:200]
                    }
                    
                    # Look for specific GitHub information
                    if "github.com" in project['website']:
                        # Extract GitHub-specific data using selectors
                        github_selectors = {
                            "stars": "[data-hotkey='g b'] .Counter",
                            "forks": "a[href*='/forks'] .Counter",
                            "description": "[data-pjax='#repo-content-pjax-container'] p",
                            "language": ".Language",
                            "topics": ".topic-tag"
                        }
                        
                        github_data = scraper.extract_data_by_selector(
                            project['website'],
                            github_selectors
                        )
                        
                        if 'error' not in github_data:
                            project_result["website_data"]["github_info"] = {
                                key: value for key, value in github_data.items()
                                if key not in ['url', 'timestamp'] and value
                            }
                else:
                    print(f"❌ Error scraping website: {website_data['error']}")
                    project_result["website_data"] = {"error": website_data['error']}
            
            project_result["status"] = "success"
            print(f"✅ Project {project['name']} processed successfully")
            
        except Exception as e:
            print(f"❌ Error processing project {project['name']}: {e}")
            project_result["status"] = "error"
            project_result["error"] = str(e)
        
        results.append(project_result)
    
    # Generate combined report
    print(f"\n📊 Combined Analysis Report")
    print("=" * 30)
    
    for result in results:
        print(f"\n📦 Project: {result['name']}")
        print(f"   Status: {result['status']}")
        
        if result['status'] == 'success':
            # Repository information
            if result.get('repo_info'):
                repo = result['repo_info']
                print(f"   📁 Repository:")
                print(f"      Branch: {repo['current_branch']}")
                print(f"      Latest commit: {repo['latest_commit']}")
                print(f"      Author: {repo['commit_author']}")
                
                if repo.get('readme_preview'):
                    print(f"      README preview: {repo['readme_preview'][:100]}...")
            
            # Website information
            if result.get('website_data') and 'error' not in result['website_data']:
                website = result['website_data']
                print(f"   🌐 Website:")
                print(f"      Title: {website.get('title', 'N/A')}")
                print(f"      Links: {website.get('links_count', 0)}")
                print(f"      Images: {website.get('images_count', 0)}")
                
                if website.get('github_info'):
                    gh_info = website['github_info']
                    print(f"      GitHub info:")
                    for key, value in gh_info.items():
                        if value:
                            print(f"         {key}: {value}")
        else:
            print(f"   ❌ Error: {result.get('error', 'Unknown error')}")
    
    # Save combined results
    output_file = "combined_analysis_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Combined analysis saved to: {output_file}")
    
    # Cleanup
    try:
        cloner.cleanup()
        scraper.cleanup()
        print("\n🧹 Cleaned up all resources")
    except Exception as e:
        print(f"⚠️ Warning during cleanup: {e}")


def research_workflow_example():
    """Demonstrate a research workflow combining both tools."""
    
    print("\n" + "="*60)
    print("Research Workflow Example")
    print("="*60)
    
    # Simulate a research project where we want to:
    # 1. Clone related repositories
    # 2. Scrape documentation websites
    # 3. Combine information for analysis
    
    cloner = RepositoryCloner(base_dir="./research_repos")
    scraper = WebScraper(delay=2.0)
    
    research_topics = {
        "machine_learning": {
            "repos": ["https://github.com/octocat/Hello-World.git"],  # Using simple repo for demo
            "websites": ["https://httpbin.org/html"]  # Using test site for demo
        }
    }
    
    try:
        for topic, sources in research_topics.items():
            print(f"\n🔬 Researching topic: {topic}")
            print("-" * 30)
            
            # Clone repositories
            repo_data = []
            for repo_url in sources["repos"]:
                try:
                    print(f"   Cloning: {repo_url}")
                    repo = cloner.clone_repository(repo_url, depth=1)
                    info = cloner.get_repository_info(repo.working_dir)
                    
                    repo_summary = {
                        "url": repo_url,
                        "path": info["path"],
                        "branch": info["current_branch"],
                        "latest_commit": info["latest_commit"]["message"][:50]
                    }
                    repo_data.append(repo_summary)
                    print(f"      ✅ Success")
                    
                except Exception as e:
                    print(f"      ❌ Error: {e}")
            
            # Scrape documentation websites
            website_data = []
            for website_url in sources["websites"]:
                try:
                    print(f"   Scraping: {website_url}")
                    data = scraper.scrape_static_content(website_url)
                    
                    if 'error' not in data:
                        website_summary = {
                            "url": website_url,
                            "title": data.get("title"),
                            "content_length": len(data.get("text_content", "")),
                            "links_count": len(data.get("links", []))
                        }
                        website_data.append(website_summary)
                        print(f"      ✅ Success")
                    else:
                        print(f"      ❌ Error: {data['error']}")
                        
                except Exception as e:
                    print(f"      ❌ Error: {e}")
            
            # Combine research data
            research_result = {
                "topic": topic,
                "repositories": repo_data,
                "websites": website_data,
                "summary": {
                    "total_repos": len(repo_data),
                    "total_websites": len(website_data),
                    "total_sources": len(repo_data) + len(website_data)
                }
            }
            
            # Save research results
            filename = f"research_{topic}.json"
            with open(filename, 'w') as f:
                json.dump(research_result, f, indent=2, default=str)
            
            print(f"   💾 Research data saved to: {filename}")
            print(f"   📊 Summary: {research_result['summary']['total_repos']} repos, "
                  f"{research_result['summary']['total_websites']} websites")
    
    except Exception as e:
        print(f"❌ Research workflow error: {e}")
    
    finally:
        cloner.cleanup()
        scraper.cleanup()
        print("\n🧹 Research workflow completed")


if __name__ == "__main__":
    main()
    research_workflow_example()