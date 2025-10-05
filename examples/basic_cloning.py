"""
Basic repository cloning example.

This example demonstrates how to clone repositories and extract basic information.
"""

from ai_time_machines import RepositoryCloner
import json


def main():
    """Clone a sample repository and display information."""
    
    # Initialize the cloner
    cloner = RepositoryCloner(base_dir="./example_repositories")
    
    # Repository to clone (using a small, public repository)
    repo_url = "https://github.com/octocat/Hello-World.git"
    
    try:
        print(f"🔄 Cloning repository: {repo_url}")
        
        # Clone the repository
        repo = cloner.clone_repository(repo_url)
        
        print(f"✅ Successfully cloned to: {repo.working_dir}")
        
        # Get repository information
        info = cloner.get_repository_info(repo.working_dir)
        
        # Display information
        print("\n📊 Repository Information:")
        print(f"   Path: {info['path']}")
        print(f"   Current branch: {info['current_branch']}")
        print(f"   Available branches: {', '.join(info['branches'])}")
        print(f"   Remote URLs: {info['remotes']}")
        print(f"   Latest commit: {info['latest_commit']['message'].strip()}")
        print(f"   Author: {info['latest_commit']['author']}")
        print(f"   Date: {info['latest_commit']['date']}")
        print(f"   Is dirty: {info['is_dirty']}")
        
        if info['untracked_files']:
            print(f"   Untracked files: {info['untracked_files']}")
        
        # Save repository information to JSON
        with open("repository_info.json", "w") as f:
            json.dump(info, f, indent=2, default=str)
        
        print(f"\n💾 Repository information saved to repository_info.json")
        
        # List all cloned repositories
        print("\n📁 All cloned repositories:")
        repos = cloner.list_cloned_repositories()
        for repo_info in repos:
            if 'error' not in repo_info:
                print(f"   - {repo_info['path']} (branch: {repo_info['current_branch']})")
            else:
                print(f"   - Error: {repo_info['error']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Clean up resources
        cloner.cleanup()
        print("\n🧹 Cleaned up resources")


if __name__ == "__main__":
    main()