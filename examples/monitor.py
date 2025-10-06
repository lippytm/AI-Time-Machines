#!/usr/bin/env python3
"""Example script for automated repository monitoring."""

import sys
import os
import time
import signal

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_time_machines import AITimeMachines


class RepositoryMonitor:
    """Enhanced repository monitoring with AI analysis."""
    
    def __init__(self, check_interval: int = 300):
        """Initialize the monitor."""
        self.app = AITimeMachines()
        self.check_interval = check_interval
        self.running = True
        
        # Handle Ctrl+C gracefully
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle interrupt signal."""
        print("\n🛑 Stopping monitor...")
        self.running = False
    
    def run(self):
        """Run the monitoring loop."""
        print("🔍 Starting AI-powered repository monitoring")
        print(f"Check interval: {self.check_interval} seconds")
        print("Press Ctrl+C to stop\n")
        
        last_health_score = None
        check_count = 0
        
        while self.running:
            try:
                check_count += 1
                print(f"🔄 Check #{check_count} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Get repository health
                health = self.app.get_repository_health()
                current_score = health['health_score']
                
                print(f"   Health Score: {current_score}/100")
                
                # Check for health changes
                if last_health_score is not None and current_score != last_health_score:
                    change = current_score - last_health_score
                    trend = "📈" if change > 0 else "📉"
                    print(f"   {trend} Health changed by {change} points")
                    
                    # Send notification for significant changes
                    if abs(change) >= 10:
                        self.app.email_service.send_github_event_notification(
                            event_type="Health Change Alert",
                            event_data={
                                "repository": self.app.github.repo_owner + "/" + self.app.github.repo_name,
                                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                                "previous_score": last_health_score,
                                "current_score": current_score,
                                "change": change,
                                "recommendations": health['recommendations']
                            }
                        )
                
                last_health_score = current_score
                
                # Show recent activity
                summary = self.app.get_repository_summary()
                recent_issues = summary['recent_activity']['recent_issues'][:3]
                recent_prs = summary['recent_activity']['recent_prs'][:3]
                
                if recent_issues:
                    print("   Recent Issues:")
                    for issue in recent_issues:
                        print(f"     - #{issue['number']}: {issue['title']} ({issue['state']})")
                
                if recent_prs:
                    print("   Recent PRs:")
                    for pr in recent_prs:
                        print(f"     - #{pr['number']}: {pr['title']} ({pr['state']})")
                
                # AI analysis every 10 checks
                if check_count % 10 == 0:
                    print("   🤖 Running AI analysis...")
                    analysis_query = f"""
                    Analyze the current repository state. Health score is {current_score}/100.
                    Recent issues: {len(recent_issues)}. Recent PRs: {len(recent_prs)}.
                    What insights or recommendations do you have?
                    """
                    
                    try:
                        result = self.app.process_query(analysis_query)
                        print(f"   AI Insight: {result['response'][:150]}...")
                        
                        if result['actions_taken']:
                            print(f"   AI Actions: {', '.join(result['actions_taken'])}")
                    except Exception as e:
                        print(f"   AI Analysis failed: {e}")
                
                print()
                
                # Wait for next check
                if self.running:
                    time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Monitor error: {e}")
                print("   Continuing monitoring...\n")
                time.sleep(60)  # Wait a minute before retrying
        
        print("✅ Repository monitoring stopped")


def main():
    """Main monitoring function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI-powered repository monitoring")
    parser.add_argument("--interval", type=int, default=300, help="Check interval in seconds")
    
    args = parser.parse_args()
    
    try:
        monitor = RepositoryMonitor(args.interval)
        monitor.run()
    except Exception as e:
        print(f"❌ Monitoring failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()