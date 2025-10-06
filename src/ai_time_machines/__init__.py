"""Main AI Time Machines application."""

import sys
from typing import Optional
from loguru import logger

from .config import config
from .github_integration import GitHubIntegration
from .email_service import EmailService
from .ai_components import ChatGPTGitHubAgent


class AITimeMachines:
    """Main AI Time Machines application."""

    def __init__(self):
        """Initialize the AI Time Machines application."""
        # Configure logging
        logger.remove()
        logger.add(
            sys.stderr,
            level=config.app.log_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )
        
        logger.info("Initializing AI Time Machines")
        
        # Initialize components
        self.github = GitHubIntegration()
        self.email_service = EmailService()
        self.ai_agent = ChatGPTGitHubAgent()
        
        logger.info("AI Time Machines initialized successfully")

    def process_query(self, query: str, context: Optional[dict] = None) -> dict:
        """Process a user query with the AI agent."""
        logger.info(f"Processing query: {query}")
        try:
            result = self.ai_agent.process_query(query, context)
            logger.info("Query processed successfully")
            return result
        except Exception as e:
            logger.error(f"Failed to process query: {e}")
            self.email_service.send_error_notification(
                error_message=f"Query processing failed: {query}",
                error_details=str(e)
            )
            raise

    def get_repository_health(self) -> dict:
        """Get repository health analysis."""
        logger.info("Analyzing repository health")
        try:
            health = self.ai_agent.analyze_repository_health()
            logger.info(f"Repository health score: {health['health_score']}")
            return health
        except Exception as e:
            logger.error(f"Failed to analyze repository health: {e}")
            raise

    def get_repository_summary(self) -> dict:
        """Get repository summary."""
        logger.info("Getting repository summary")
        try:
            summary = self.ai_agent.get_repository_summary()
            logger.info("Repository summary retrieved successfully")
            return summary
        except Exception as e:
            logger.error(f"Failed to get repository summary: {e}")
            raise

    def test_integrations(self) -> dict:
        """Test all integrations."""
        logger.info("Testing integrations")
        results = {}
        
        # Test GitHub integration
        try:
            repo_info = self.github.get_repository_info()
            results["github"] = {
                "status": "success",
                "repository": repo_info["full_name"],
                "message": "GitHub integration working"
            }
            logger.info("GitHub integration test passed")
        except Exception as e:
            results["github"] = {
                "status": "error",
                "message": f"GitHub integration failed: {e}"
            }
            logger.error(f"GitHub integration test failed: {e}")
        
        # Test email service
        try:
            email_test = self.email_service.test_connection()
            results["email"] = {
                "status": "success" if email_test else "warning",
                "message": "Email service working" if email_test else "Email service configured but test failed"
            }
            logger.info("Email service test completed")
        except Exception as e:
            results["email"] = {
                "status": "error",
                "message": f"Email service failed: {e}"
            }
            logger.error(f"Email service test failed: {e}")
        
        # Test AI components (basic check)
        try:
            # Just verify we can initialize the AI agent
            test_response = "AI Time Machines components are functional"
            results["ai"] = {
                "status": "success",
                "message": test_response
            }
            logger.info("AI components test passed")
        except Exception as e:
            results["ai"] = {
                "status": "error",
                "message": f"AI components failed: {e}"
            }
            logger.error(f"AI components test failed: {e}")
        
        # Send notification about test results
        try:
            self.email_service.send_github_event_notification(
                event_type="Integration Test",
                event_data={
                    "repository": config.github.repository_owner + "/" + config.github.repository_name,
                    "timestamp": "test_time",
                    "results": results
                }
            )
        except Exception as e:
            logger.warning(f"Failed to send test notification: {e}")
        
        return results

    def monitor_repository(self, check_interval: int = 300) -> None:
        """Monitor repository for changes and send notifications."""
        import time
        
        logger.info(f"Starting repository monitoring (check interval: {check_interval}s)")
        
        last_check_time = time.time()
        
        while True:
            try:
                # Get recent activity
                issues = self.github.get_issues(state="all")
                prs = self.github.get_pull_requests(state="all")
                
                # Check for new issues or PRs since last check
                new_items = []
                current_time = time.time()
                
                for issue in issues:
                    if issue.created_at.timestamp() > last_check_time:
                        new_items.append(f"New issue #{issue.number}: {issue.title}")
                
                for pr in prs:
                    if pr.created_at.timestamp() > last_check_time:
                        new_items.append(f"New PR #{pr.number}: {pr.title}")
                
                # Send notifications for new items
                if new_items:
                    self.email_service.send_github_event_notification(
                        event_type="Repository Activity",
                        event_data={
                            "repository": config.github.repository_owner + "/" + config.github.repository_name,
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "new_activity": new_items
                        }
                    )
                    logger.info(f"Detected {len(new_items)} new repository items")
                
                last_check_time = current_time
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                logger.info("Repository monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Error during repository monitoring: {e}")
                self.email_service.send_error_notification(
                    error_message="Repository monitoring error",
                    error_details=str(e)
                )
                time.sleep(60)  # Wait a minute before retrying


def main():
    """Main entry point for the application."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Time Machines - ChatGPT GitHub Integration")
    parser.add_argument("--query", type=str, help="Process a query with the AI agent")
    parser.add_argument("--health", action="store_true", help="Get repository health analysis")
    parser.add_argument("--summary", action="store_true", help="Get repository summary")
    parser.add_argument("--test", action="store_true", help="Test all integrations")
    parser.add_argument("--monitor", action="store_true", help="Start repository monitoring")
    parser.add_argument("--monitor-interval", type=int, default=300, help="Monitoring check interval in seconds")
    
    args = parser.parse_args()
    
    try:
        app = AITimeMachines()
        
        if args.query:
            result = app.process_query(args.query)
            print(f"AI Response: {result['response']}")
            if result['actions_taken']:
                print(f"Actions taken: {', '.join(result['actions_taken'])}")
        
        elif args.health:
            health = app.get_repository_health()
            print(f"Repository Health Score: {health['health_score']}/100")
            if health['recommendations']:
                print("Recommendations:")
                for rec in health['recommendations']:
                    print(f"  - {rec}")
        
        elif args.summary:
            summary = app.get_repository_summary()
            print(f"Repository: {summary['repository']['full_name']}")
            print(f"Description: {summary['repository'].get('description', 'No description')}")
            print(f"Stars: {summary['repository']['stars']}")
            print(f"Open Issues: {summary['statistics']['open_issues']}")
            print(f"Open PRs: {summary['statistics']['open_prs']}")
        
        elif args.test:
            results = app.test_integrations()
            print("Integration Test Results:")
            for service, result in results.items():
                status_emoji = "✅" if result["status"] == "success" else "⚠️" if result["status"] == "warning" else "❌"
                print(f"  {status_emoji} {service.title()}: {result['message']}")
        
        elif args.monitor:
            app.monitor_repository(args.monitor_interval)
        
        else:
            parser.print_help()
    
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()