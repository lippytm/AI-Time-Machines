#!/usr/bin/env python3
"""Example script demonstrating AI Time Machines usage."""

import sys
import os

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_time_machines import AITimeMachines


def main():
    """Demonstrate various AI Time Machines features."""
    print("🤖 AI Time Machines Demo")
    print("=" * 40)
    
    try:
        # Initialize the application
        print("Initializing AI Time Machines...")
        app = AITimeMachines()
        print("✅ Initialization complete\n")
        
        # Test integrations
        print("1. Testing integrations...")
        results = app.test_integrations()
        for service, result in results.items():
            status = "✅" if result["status"] == "success" else "⚠️" if result["status"] == "warning" else "❌"
            print(f"   {status} {service.title()}: {result['message']}")
        print()
        
        # Get repository summary
        print("2. Repository Summary:")
        summary = app.get_repository_summary()
        repo = summary['repository']
        stats = summary['statistics']
        
        print(f"   Repository: {repo['full_name']}")
        print(f"   Description: {repo.get('description', 'No description')}")
        print(f"   Stars: {repo['stars']}")
        print(f"   Total Issues: {stats['total_issues']}")
        print(f"   Open Issues: {stats['open_issues']}")
        print(f"   Open PRs: {stats['open_prs']}")
        print()
        
        # Repository health analysis
        print("3. Repository Health Analysis:")
        health = app.get_repository_health()
        print(f"   Health Score: {health['health_score']}/100")
        
        if health['recommendations']:
            print("   Recommendations:")
            for rec in health['recommendations']:
                print(f"     - {rec}")
        else:
            print("   No recommendations - repository looks healthy!")
        print()
        
        # AI Query Examples
        print("4. AI Query Examples:")
        
        queries = [
            "What is the current status of this repository?",
            "How many open issues do we have?",
            "Can you analyze the recent activity?",
        ]
        
        for i, query in enumerate(queries, 1):
            print(f"   Query {i}: {query}")
            try:
                result = app.process_query(query)
                print(f"   AI Response: {result['response'][:200]}...")
                if result['actions_taken']:
                    print(f"   Actions: {', '.join(result['actions_taken'])}")
                print()
            except Exception as e:
                print(f"   Error: {e}")
                print()
        
        print("🎉 Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()