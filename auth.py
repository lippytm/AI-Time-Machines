"""Authorization module for GitHub API access."""

import os
from typing import Optional
from github import Github, Auth
from config import settings, validate_github_auth


class GitHubAuthorizer:
    """Handles GitHub API authorization and authentication."""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize with GitHub token."""
        self.token = token or settings.github_token
        self._github_client = None
        
    def authenticate(self) -> Github:
        """Create and return authenticated GitHub client."""
        if not self.token:
            raise ValueError("GitHub token is required for authentication")
            
        if not self._github_client:
            auth = Auth.Token(self.token)
            self._github_client = Github(auth=auth)
            
        return self._github_client
    
    def validate_access(self, repo_owner: str, repo_name: str) -> bool:
        """Validate that the token has access to the specified repository."""
        try:
            client = self.authenticate()
            repo = client.get_repo(f"{repo_owner}/{repo_name}")
            # Try to access repository information
            _ = repo.name
            return True
        except Exception as e:
            print(f"Access validation failed: {e}")
            return False
    
    def get_user_info(self) -> dict:
        """Get information about the authenticated user."""
        try:
            client = self.authenticate()
            user = client.get_user()
            return {
                "login": user.login,
                "name": user.name,
                "email": user.email,
                "id": user.id
            }
        except Exception as e:
            raise ValueError(f"Failed to get user info: {e}")


# Global authorizer instance
authorizer = GitHubAuthorizer()


def ensure_authorized() -> Github:
    """Ensure GitHub authorization is valid and return client."""
    if not validate_github_auth():
        raise ValueError("GitHub token not configured. Please set GITHUB_TOKEN environment variable.")
    
    return authorizer.authenticate()