"""
Repository cloning functionality for AI Time Machines.

This module provides comprehensive git repository cloning and management capabilities.
"""

import os
import shutil
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from git import Repo, GitCommandError


class RepositoryCloner:
    """
    A comprehensive repository cloning utility that supports various git operations.
    
    This class provides functionality to clone repositories, manage branches,
    and perform various git operations with error handling and logging.
    """
    
    def __init__(self, base_dir: Optional[str] = None, log_level: int = logging.INFO):
        """
        Initialize the RepositoryCloner.
        
        Args:
            base_dir: Base directory for cloning repositories. Defaults to ./repositories
            log_level: Logging level for operations
        """
        self.base_dir = Path(base_dir) if base_dir else Path.cwd() / "repositories"
        self.base_dir.mkdir(exist_ok=True)
        
        # Setup logging
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger(__name__)
        
        self.cloned_repos: Dict[str, Repo] = {}
    
    def clone_repository(self, 
                        repo_url: str, 
                        destination: Optional[str] = None,
                        branch: Optional[str] = None,
                        depth: Optional[int] = None,
                        single_branch: bool = False) -> Repo:
        """
        Clone a git repository with various options.
        
        Args:
            repo_url: URL of the repository to clone
            destination: Local destination path. If None, derives from repo name
            branch: Specific branch to clone
            depth: Depth of clone (for shallow clones)
            single_branch: Whether to clone only a single branch
            
        Returns:
            Git Repo object
            
        Raises:
            GitCommandError: If cloning fails
            ValueError: If invalid parameters provided
        """
        if not repo_url:
            raise ValueError("Repository URL cannot be empty")
        
        # Determine destination path
        if not destination:
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            destination = self.base_dir / repo_name
        else:
            destination = Path(destination)
        
        # Remove existing directory if it exists
        if destination.exists():
            self.logger.warning(f"Destination {destination} exists. Removing...")
            shutil.rmtree(destination)
        
        try:
            self.logger.info(f"Cloning {repo_url} to {destination}")
            
            # Prepare clone arguments
            clone_kwargs = {}
            if branch:
                clone_kwargs['branch'] = branch
            if depth:
                clone_kwargs['depth'] = depth
            if single_branch:
                clone_kwargs['single_branch'] = True
            
            # Clone the repository
            repo = Repo.clone_from(repo_url, destination, **clone_kwargs)
            
            # Store the cloned repo
            self.cloned_repos[str(destination)] = repo
            
            self.logger.info(f"Successfully cloned {repo_url}")
            return repo
            
        except GitCommandError as e:
            self.logger.error(f"Failed to clone {repo_url}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error cloning {repo_url}: {e}")
            raise
    
    def get_repository_info(self, repo_path: str) -> Dict[str, Any]:
        """
        Get comprehensive information about a cloned repository.
        
        Args:
            repo_path: Path to the repository
            
        Returns:
            Dictionary containing repository information
        """
        try:
            repo = Repo(repo_path)
            
            # Get current branch
            current_branch = repo.active_branch.name if not repo.head.is_detached else "HEAD"
            
            # Get all branches
            branches = [branch.name for branch in repo.branches]
            
            # Get remote information
            remotes = {}
            for remote in repo.remotes:
                remotes[remote.name] = list(remote.urls)
            
            # Get latest commit info
            latest_commit = repo.head.commit
            
            info = {
                "path": repo_path,
                "current_branch": current_branch,
                "branches": branches,
                "remotes": remotes,
                "latest_commit": {
                    "sha": latest_commit.hexsha,
                    "message": latest_commit.message.strip(),
                    "author": str(latest_commit.author),
                    "date": latest_commit.committed_datetime.isoformat()
                },
                "is_dirty": repo.is_dirty(),
                "untracked_files": repo.untracked_files
            }
            
            return info
            
        except Exception as e:
            self.logger.error(f"Failed to get repository info for {repo_path}: {e}")
            return {"error": str(e)}
    
    def list_cloned_repositories(self) -> List[Dict[str, Any]]:
        """
        List all repositories in the base directory.
        
        Returns:
            List of repository information dictionaries
        """
        repositories = []
        
        for item in self.base_dir.iterdir():
            if item.is_dir() and (item / ".git").exists():
                repo_info = self.get_repository_info(str(item))
                repositories.append(repo_info)
        
        return repositories
    
    def update_repository(self, repo_path: str, branch: Optional[str] = None) -> bool:
        """
        Update a repository by pulling latest changes.
        
        Args:
            repo_path: Path to the repository
            branch: Branch to checkout and update (optional)
            
        Returns:
            True if update successful, False otherwise
        """
        try:
            repo = Repo(repo_path)
            
            # Checkout specific branch if provided
            if branch and branch in [b.name for b in repo.branches]:
                repo.git.checkout(branch)
                self.logger.info(f"Checked out branch {branch}")
            
            # Pull latest changes
            origin = repo.remotes.origin
            origin.pull()
            
            self.logger.info(f"Successfully updated repository at {repo_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update repository at {repo_path}: {e}")
            return False
    
    def cleanup(self):
        """Clean up resources and close repository connections."""
        for repo in self.cloned_repos.values():
            repo.close()
        self.cloned_repos.clear()
        self.logger.info("Cleaned up repository connections")