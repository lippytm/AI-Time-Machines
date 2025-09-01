#!/usr/bin/env python3
"""Demo script showing AI Time Machines automation functionality."""

import json
from workflow import process_automation_request
from pr_handler import extract_pr_number_from_url, extract_repo_from_url

def demo_url_extraction():
    """Demonstrate URL parsing functionality."""
    print("=== URL Extraction Demo ===")
    
    test_urls = [
        "https://github.com/lippytm/AI-Time-Machines/pull/123",
        "https://github.com/microsoft/vscode/pull/456", 
        "https://github.com/python/cpython/pull/789"
    ]
    
    for url in test_urls:
        pr_number = extract_pr_number_from_url(url)
        repo_info = extract_repo_from_url(url)
        print(f"URL: {url}")
        print(f"  PR Number: {pr_number}")
        print(f"  Repository: {repo_info}")
        print()

def demo_workflow_context():
    """Demonstrate workflow context creation without requiring authentication."""
    print("=== Workflow Context Demo ===")
    
    # Test various input formats
    test_inputs = [
        {
            "name": "Direct PR Numbers",
            "data": {
                "repository_owner": "microsoft",
                "repository_name": "vscode",
                "pull_request_numbers": [123, 124, 125]
            }
        },
        {
            "name": "URL-based Input",
            "data": {
                "pull_request_urls": [
                    "https://github.com/python/cpython/pull/100",
                    "https://github.com/python/cpython/pull/101"
                ]
            }
        },
        {
            "name": "Mixed Input with Metadata", 
            "data": {
                "repository_owner": "tensorflow",
                "repository_name": "tensorflow",
                "pull_request_number": 42,
                "metadata": {
                    "source": "demo",
                    "priority": "high"
                }
            }
        }
    ]
    
    # Import workflow engine for context creation only
    from workflow import WorkflowEngine
    engine = WorkflowEngine()
    
    for test in test_inputs:
        print(f"Test: {test['name']}")
        try:
            context = engine.create_context_from_input(test['data'])
            print(f"  Repository: {context.repository_owner}/{context.repository_name}")
            print(f"  PR Numbers: {context.pull_request_numbers}")
            print(f"  Metadata: {context.metadata}")
        except Exception as e:
            print(f"  Error: {e}")
        print()

def demo_json_format():
    """Demonstrate JSON input/output format."""
    print("=== JSON Format Demo ===")
    
    sample_input = {
        "repository_owner": "facebook", 
        "repository_name": "react",
        "pull_request_numbers": [200, 201],
        "auto_discover": False,
        "metadata": {
            "workflow": "ci_check",
            "requester": "automation_bot"
        }
    }
    
    print("Sample JSON Input:")
    print(json.dumps(sample_input, indent=2))
    print()
    
    # Show what the output structure would look like
    sample_output = {
        "success": True,
        "context": {
            "repository_owner": "facebook",
            "repository_name": "react", 
            "pull_request_numbers": [200, 201],
            "timestamp": "2023-01-01T12:00:00",
            "metadata": sample_input["metadata"]
        },
        "processed_prs": {
            "200": {
                "number": 200,
                "title": "Sample PR Title",
                "state": "open",
                "author": "developer1",
                "repository": "facebook/react",
                "url": "https://github.com/facebook/react/pull/200"
            },
            "201": None  # Failed to process
        },
        "errors": ["Failed to process PRs: [201]"],
        "execution_time": 2.5
    }
    
    print("Sample JSON Output:")
    print(json.dumps(sample_output, indent=2))

def main():
    """Run all demos."""
    print("AI Time Machines - Automation Demo")
    print("=" * 50)
    print()
    
    demo_url_extraction()
    print()
    
    demo_workflow_context() 
    print()
    
    demo_json_format()
    print()
    
    print("Demo completed! The system is ready for GitHub automation.")
    print("To use with real GitHub data, set GITHUB_TOKEN environment variable.")

if __name__ == "__main__":
    main()