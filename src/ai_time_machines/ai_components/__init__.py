"""AI components for ChatGPT integration and GitHub interactions."""

from typing import Optional, Dict, Any, List
import openai
from loguru import logger
from datetime import datetime

from ..config import config
from ..github_integration import GitHubIntegration
from ..email_service import EmailService


class ChatGPTGitHubAgent:
    """ChatGPT agent for GitHub repository interactions."""

    def __init__(self):
        """Initialize the ChatGPT GitHub agent."""
        self.openai_client = openai.OpenAI(api_key=config.openai.api_key)
        self.github = GitHubIntegration()
        self.email_service = EmailService()

    def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a query and potentially take GitHub actions."""
        try:
            logger.info(f"Processing query: {query}")
            
            # Get repository context
            repo_info = self.github.get_repository_info()
            recent_issues = self.github.get_issues(state="open")[:5]  # Last 5 open issues
            recent_prs = self.github.get_pull_requests(state="open")[:5]  # Last 5 open PRs
            
            # Prepare context for ChatGPT
            system_prompt = self._build_system_prompt(repo_info, recent_issues, recent_prs)
            
            # Get AI response
            response = self._get_chatgpt_response(query, system_prompt, context)
            
            # Parse response for potential actions
            actions_taken = self._execute_github_actions(response, query)
            
            result = {
                "query": query,
                "response": response,
                "actions_taken": actions_taken,
                "timestamp": datetime.now().isoformat(),
                "repository": repo_info["full_name"]
            }
            
            # Send notification if configured
            if actions_taken:
                self.email_service.send_ai_response_notification(
                    query=query,
                    response=response,
                    github_action=", ".join(actions_taken)
                )
            
            logger.info("Query processed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Failed to process query: {e}")
            self.email_service.send_error_notification(
                error_message=f"Failed to process query: {query}",
                error_details=str(e)
            )
            raise

    def _build_system_prompt(self, repo_info: Dict, recent_issues: List, recent_prs: List) -> str:
        """Build system prompt with repository context."""
        issues_summary = "\n".join([
            f"- Issue #{issue.number}: {issue.title} (State: {issue.state})"
            for issue in recent_issues
        ]) if recent_issues else "No recent issues"
        
        prs_summary = "\n".join([
            f"- PR #{pr.number}: {pr.title} (State: {pr.state})"
            for pr in recent_prs
        ]) if recent_prs else "No recent pull requests"
        
        return f"""You are an AI assistant for the "{repo_info['name']}" GitHub repository.

Repository Information:
- Name: {repo_info['name']}
- Description: {repo_info.get('description', 'No description')}
- Stars: {repo_info['stars']}
- Open Issues: {repo_info['open_issues']}
- Default Branch: {repo_info['default_branch']}

Recent Open Issues:
{issues_summary}

Recent Open Pull Requests:
{prs_summary}

You can help with:
1. Answering questions about the repository
2. Creating issues (respond with "CREATE_ISSUE: title | body | labels")
3. Commenting on issues (respond with "COMMENT_ISSUE: issue_number | comment")
4. General repository management and development advice

Always be helpful and provide actionable insights. If you suggest creating an issue or commenting, format your response with the appropriate action prefix."""

    def _get_chatgpt_response(self, query: str, system_prompt: str, 
                             context: Optional[Dict[str, Any]] = None) -> str:
        """Get response from ChatGPT."""
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
            
            # Add context if provided
            if context:
                context_str = f"Additional context: {context}"
                messages.append({"role": "system", "content": context_str})
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Failed to get ChatGPT response: {e}")
            return f"Sorry, I encountered an error while processing your request: {str(e)}"

    def _execute_github_actions(self, response: str, original_query: str) -> List[str]:
        """Execute GitHub actions based on AI response."""
        actions_taken = []
        
        try:
            lines = response.split('\n')
            
            for line in lines:
                line = line.strip()
                
                # Create issue action
                if line.startswith("CREATE_ISSUE:"):
                    parts = line[13:].split(" | ")
                    if len(parts) >= 2:
                        title = parts[0].strip()
                        body = parts[1].strip()
                        labels = parts[2].strip().split(",") if len(parts) > 2 else []
                        
                        # Add context about the original query
                        body += f"\n\n---\nThis issue was created by AI Time Machines in response to: {original_query}"
                        
                        issue = self.github.create_issue(title, body, labels)
                        actions_taken.append(f"Created issue #{issue.number}: {title}")
                
                # Comment on issue action
                elif line.startswith("COMMENT_ISSUE:"):
                    parts = line[14:].split(" | ")
                    if len(parts) >= 2:
                        try:
                            issue_number = int(parts[0].strip())
                            comment = parts[1].strip()
                            
                            # Add context about the AI response
                            comment += f"\n\n---\n*Comment generated by AI Time Machines*"
                            
                            self.github.add_issue_comment(issue_number, comment)
                            actions_taken.append(f"Added comment to issue #{issue_number}")
                        except ValueError:
                            logger.warning(f"Invalid issue number in action: {parts[0]}")
            
        except Exception as e:
            logger.error(f"Failed to execute GitHub actions: {e}")
            
        return actions_taken

    def get_repository_summary(self) -> Dict[str, Any]:
        """Get a comprehensive repository summary."""
        try:
            repo_info = self.github.get_repository_info()
            issues = self.github.get_issues(state="all")
            prs = self.github.get_pull_requests(state="all")
            
            open_issues = [i for i in issues if i.state == "open"]
            closed_issues = [i for i in issues if i.state == "closed"]
            open_prs = [p for p in prs if p.state == "open"]
            closed_prs = [p for p in prs if p.state == "closed"]
            
            summary = {
                "repository": repo_info,
                "statistics": {
                    "total_issues": len(issues),
                    "open_issues": len(open_issues),
                    "closed_issues": len(closed_issues),
                    "total_prs": len(prs),
                    "open_prs": len(open_prs),
                    "closed_prs": len(closed_prs),
                },
                "recent_activity": {
                    "recent_issues": [
                        {"number": i.number, "title": i.title, "state": i.state}
                        for i in issues[:10]
                    ],
                    "recent_prs": [
                        {"number": p.number, "title": p.title, "state": p.state}
                        for p in prs[:10]
                    ]
                }
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to get repository summary: {e}")
            raise

    def analyze_repository_health(self) -> Dict[str, Any]:
        """Analyze repository health and provide insights."""
        try:
            summary = self.get_repository_summary()
            
            # Simple health metrics
            total_issues = summary["statistics"]["total_issues"]
            open_issues = summary["statistics"]["open_issues"]
            open_prs = summary["statistics"]["open_prs"]
            
            health_score = 100
            recommendations = []
            
            # Check issue ratio
            if total_issues > 0:
                open_issue_ratio = open_issues / total_issues
                if open_issue_ratio > 0.7:
                    health_score -= 20
                    recommendations.append("High ratio of open issues - consider addressing some")
            
            # Check PR accumulation
            if open_prs > 10:
                health_score -= 15
                recommendations.append("Many open pull requests - consider reviewing and merging")
            
            # Check repository activity
            if total_issues == 0 and len(summary["recent_activity"]["recent_prs"]) == 0:
                recommendations.append("Low activity - consider adding documentation or examples")
            
            analysis = {
                "health_score": max(0, health_score),
                "statistics": summary["statistics"],
                "recommendations": recommendations,
                "timestamp": datetime.now().isoformat()
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze repository health: {e}")
            raise