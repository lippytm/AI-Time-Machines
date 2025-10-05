"""Pull request handling and automation module."""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from github import Github
from github.PullRequest import PullRequest
from github.Repository import Repository

from auth import ensure_authorized
from config import get_repo_info


@dataclass
class PRInfo:
    """Data class for pull request information."""
    number: int
    title: str
    state: str
    author: str
    repository: str
    url: str
    created_at: str
    updated_at: str
    mergeable: Optional[bool] = None
    
    @classmethod
    def from_github_pr(cls, pr: PullRequest, repo_name: str) -> "PRInfo":
        """Create PRInfo from GitHub PullRequest object."""
        return cls(
            number=pr.number,
            title=pr.title,
            state=pr.state,
            author=pr.user.login,
            repository=repo_name,
            url=pr.html_url,
            created_at=pr.created_at.isoformat(),
            updated_at=pr.updated_at.isoformat(),
            mergeable=pr.mergeable
        )


class PRProcessor:
    """Handles pull request processing and automation."""
    
    def __init__(self, repo_owner: Optional[str] = None, repo_name: Optional[str] = None):
        """Initialize PR processor with repository information."""
        self.repo_owner, self.repo_name = get_repo_info(repo_owner, repo_name)
        self.github_client = ensure_authorized()
        self._repository = None
    
    @property
    def repository(self) -> Repository:
        """Get the GitHub repository object."""
        if not self._repository:
            self._repository = self.github_client.get_repo(f"{self.repo_owner}/{self.repo_name}")
        return self._repository
    
    def get_pull_request(self, pr_number: int) -> PRInfo:
        """Get information about a specific pull request."""
        try:
            pr = self.repository.get_pull(pr_number)
            return PRInfo.from_github_pr(pr, f"{self.repo_owner}/{self.repo_name}")
        except Exception as e:
            raise ValueError(f"Failed to get pull request {pr_number}: {e}")
    
    def list_pull_requests(self, state: str = "open", limit: Optional[int] = None) -> List[PRInfo]:
        """List pull requests for the repository."""
        try:
            prs = self.repository.get_pulls(state=state)
            pr_list = []
            
            for i, pr in enumerate(prs):
                if limit and i >= limit:
                    break
                pr_list.append(PRInfo.from_github_pr(pr, f"{self.repo_owner}/{self.repo_name}"))
            
            return pr_list
        except Exception as e:
            raise ValueError(f"Failed to list pull requests: {e}")
    
    def get_pr_files(self, pr_number: int) -> List[Dict[str, Any]]:
        """Get list of files changed in a pull request."""
        try:
            pr = self.repository.get_pull(pr_number)
            files = pr.get_files()
            
            return [
                {
                    "filename": file.filename,
                    "status": file.status,
                    "additions": file.additions,
                    "deletions": file.deletions,
                    "changes": file.changes,
                    "patch": file.patch
                }
                for file in files
            ]
        except Exception as e:
            raise ValueError(f"Failed to get files for PR {pr_number}: {e}")
    
    def process_pr_batch(self, pr_numbers: List[int]) -> Dict[int, PRInfo]:
        """Process a batch of pull requests and return their information."""
        results = {}
        for pr_number in pr_numbers:
            try:
                results[pr_number] = self.get_pull_request(pr_number)
            except Exception as e:
                print(f"Error processing PR {pr_number}: {e}")
                results[pr_number] = None
        
        return results
    
    def auto_discover_prs(self, pattern: Optional[str] = None) -> List[PRInfo]:
        """Automatically discover pull requests based on patterns or criteria."""
        prs = self.list_pull_requests(state="open")
        
        if pattern:
            # Filter PRs based on title pattern
            filtered_prs = [pr for pr in prs if pattern.lower() in pr.title.lower()]
            return filtered_prs
        
        return prs


def extract_pr_number_from_url(url: str) -> Optional[int]:
    """Extract pull request number from GitHub URL."""
    try:
        # Handle URLs like: https://github.com/owner/repo/pull/123
        if "/pull/" in url:
            return int(url.split("/pull/")[-1].split("/")[0])
        return None
    except (ValueError, IndexError):
        return None


def extract_repo_from_url(url: str) -> Optional[tuple[str, str]]:
    """Extract repository owner and name from GitHub URL."""
    try:
        # Handle URLs like: https://github.com/owner/repo/...
        if "github.com/" in url:
            parts = url.split("github.com/")[1].split("/")
            if len(parts) >= 2:
                return parts[0], parts[1]
        return None
    except (ValueError, IndexError):
        return None