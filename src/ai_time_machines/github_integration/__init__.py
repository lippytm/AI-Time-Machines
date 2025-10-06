"""GitHub API integration for repository interactions, issues, and pull requests."""

from typing import List, Optional, Dict, Any
from github import Github, Repository, Issue, PullRequest
from loguru import logger

from ..config import config


class GitHubIntegration:
    """GitHub API integration class."""

    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub integration."""
        self.token = token or config.github.token
        if not self.token:
            raise ValueError("GitHub token is required")
        
        self.github = Github(self.token)
        self.repo_owner = config.github.repository_owner
        self.repo_name = config.github.repository_name
        self._repository = None

    @property
    def repository(self) -> Repository.Repository:
        """Get the repository object."""
        if self._repository is None:
            self._repository = self.github.get_repo(f"{self.repo_owner}/{self.repo_name}")
        return self._repository

    def get_repository_info(self) -> Dict[str, Any]:
        """Get basic repository information."""
        try:
            repo = self.repository
            return {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "url": repo.html_url,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "open_issues": repo.open_issues_count,
                "default_branch": repo.default_branch,
                "created_at": repo.created_at.isoformat(),
                "updated_at": repo.updated_at.isoformat(),
            }
        except Exception as e:
            logger.error(f"Failed to get repository info: {e}")
            raise

    def create_issue(self, title: str, body: str, labels: Optional[List[str]] = None) -> Issue.Issue:
        """Create a new issue in the repository."""
        try:
            repo = self.repository
            issue = repo.create_issue(
                title=title,
                body=body,
                labels=labels or []
            )
            logger.info(f"Created issue #{issue.number}: {title}")
            return issue
        except Exception as e:
            logger.error(f"Failed to create issue: {e}")
            raise

    def get_issues(self, state: str = "open", labels: Optional[List[str]] = None) -> List[Issue.Issue]:
        """Get issues from the repository."""
        try:
            repo = self.repository
            issues = repo.get_issues(state=state, labels=labels or [])
            return list(issues)
        except Exception as e:
            logger.error(f"Failed to get issues: {e}")
            raise

    def update_issue(self, issue_number: int, title: Optional[str] = None, 
                    body: Optional[str] = None, state: Optional[str] = None) -> Issue.Issue:
        """Update an existing issue."""
        try:
            repo = self.repository
            issue = repo.get_issue(issue_number)
            
            if title is not None:
                issue.edit(title=title)
            if body is not None:
                issue.edit(body=body)
            if state is not None:
                issue.edit(state=state)
                
            logger.info(f"Updated issue #{issue_number}")
            return issue
        except Exception as e:
            logger.error(f"Failed to update issue #{issue_number}: {e}")
            raise

    def add_issue_comment(self, issue_number: int, comment: str) -> None:
        """Add a comment to an issue."""
        try:
            repo = self.repository
            issue = repo.get_issue(issue_number)
            issue.create_comment(comment)
            logger.info(f"Added comment to issue #{issue_number}")
        except Exception as e:
            logger.error(f"Failed to add comment to issue #{issue_number}: {e}")
            raise

    def get_pull_requests(self, state: str = "open") -> List[PullRequest.PullRequest]:
        """Get pull requests from the repository."""
        try:
            repo = self.repository
            pulls = repo.get_pulls(state=state)
            return list(pulls)
        except Exception as e:
            logger.error(f"Failed to get pull requests: {e}")
            raise

    def create_pull_request(self, title: str, head: str, base: str, 
                           body: Optional[str] = None) -> PullRequest.PullRequest:
        """Create a new pull request."""
        try:
            repo = self.repository
            pr = repo.create_pull(
                title=title,
                head=head,
                base=base,
                body=body or ""
            )
            logger.info(f"Created pull request #{pr.number}: {title}")
            return pr
        except Exception as e:
            logger.error(f"Failed to create pull request: {e}")
            raise

    def add_pr_comment(self, pr_number: int, comment: str) -> None:
        """Add a comment to a pull request."""
        try:
            repo = self.repository
            pr = repo.get_pull(pr_number)
            pr.create_issue_comment(comment)
            logger.info(f"Added comment to PR #{pr_number}")
        except Exception as e:
            logger.error(f"Failed to add comment to PR #{pr_number}: {e}")
            raise

    def get_commits(self, sha: Optional[str] = None, path: Optional[str] = None) -> List[Any]:
        """Get commits from the repository."""
        try:
            repo = self.repository
            commits = repo.get_commits(sha=sha, path=path)
            return list(commits)
        except Exception as e:
            logger.error(f"Failed to get commits: {e}")
            raise

    def get_file_contents(self, path: str, ref: Optional[str] = None) -> str:
        """Get contents of a file from the repository."""
        try:
            repo = self.repository
            file_content = repo.get_contents(path, ref=ref)
            return file_content.decoded_content.decode('utf-8')
        except Exception as e:
            logger.error(f"Failed to get file contents for {path}: {e}")
            raise

    def create_or_update_file(self, path: str, message: str, content: str, 
                             branch: Optional[str] = None, sha: Optional[str] = None) -> None:
        """Create or update a file in the repository."""
        try:
            repo = self.repository
            
            # Try to get existing file
            try:
                existing_file = repo.get_contents(path, ref=branch)
                # Update existing file
                repo.update_file(
                    path=path,
                    message=message,
                    content=content,
                    sha=existing_file.sha,
                    branch=branch
                )
                logger.info(f"Updated file: {path}")
            except:
                # Create new file
                repo.create_file(
                    path=path,
                    message=message,
                    content=content,
                    branch=branch
                )
                logger.info(f"Created file: {path}")
                
        except Exception as e:
            logger.error(f"Failed to create/update file {path}: {e}")
            raise