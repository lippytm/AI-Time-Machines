#!/usr/bin/env python3
"""Command line interface for AI Time Machines automation."""

import json
import sys
import argparse
from typing import Dict, Any

from workflow import process_automation_request
from pr_handler import extract_pr_number_from_url, extract_repo_from_url
from config import validate_github_auth


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="AI Time Machines - GitHub PR Automation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process specific PRs
  python main.py --repo-owner myorg --repo-name myrepo --pr-numbers 123 124

  # Process PR from URL
  python main.py --pr-url https://github.com/myorg/myrepo/pull/123

  # Auto-discover open PRs
  python main.py --repo-owner myorg --repo-name myrepo --auto-discover

  # Process with pattern filter
  python main.py --repo-owner myorg --repo-name myrepo --auto-discover --pattern "bug fix"

  # Process from JSON input
  echo '{"repository_owner":"myorg","repository_name":"myrepo","pull_request_numbers":[123]}' | python main.py --json
        """
    )
    
    # Repository information
    parser.add_argument('--repo-owner', help='Repository owner/organization')
    parser.add_argument('--repo-name', help='Repository name')
    parser.add_argument('--repo-url', help='Repository URL (alternative to owner/name)')
    
    # Pull request specification
    parser.add_argument('--pr-numbers', type=int, nargs='+', help='Pull request numbers to process')
    parser.add_argument('--pr-url', help='Pull request URL')
    parser.add_argument('--pr-urls', nargs='+', help='Multiple pull request URLs')
    
    # Auto-discovery options
    parser.add_argument('--auto-discover', action='store_true', 
                        help='Automatically discover open PRs')
    parser.add_argument('--pattern', help='Pattern to filter PRs during auto-discovery')
    
    # Input/output options
    parser.add_argument('--json', action='store_true', 
                        help='Read input from JSON stdin')
    parser.add_argument('--output-format', choices=['json', 'summary'], default='summary',
                        help='Output format')
    
    # Other options
    parser.add_argument('--validate', action='store_true',
                        help='Validate configuration and exit')
    
    return parser.parse_args()


def build_input_data(args) -> Dict[str, Any]:
    """Build input data dictionary from command line arguments."""
    input_data = {}
    
    # Repository information
    if args.repo_owner:
        input_data['repository_owner'] = args.repo_owner
    if args.repo_name:
        input_data['repository_name'] = args.repo_name
    if args.repo_url:
        input_data['repository_url'] = args.repo_url
    
    # Pull request numbers
    if args.pr_numbers:
        input_data['pull_request_numbers'] = args.pr_numbers
    
    # Pull request URLs
    pr_urls = []
    if args.pr_url:
        pr_urls.append(args.pr_url)
    if args.pr_urls:
        pr_urls.extend(args.pr_urls)
    if pr_urls:
        input_data['pull_request_urls'] = pr_urls
    
    # Auto-discovery
    if args.auto_discover:
        input_data['auto_discover'] = True
        if args.pattern:
            input_data['discovery_pattern'] = args.pattern
    
    return input_data


def format_output(result: Dict[str, Any], format_type: str) -> str:
    """Format output based on the specified format."""
    if format_type == 'json':
        return json.dumps(result, indent=2)
    
    # Summary format
    lines = []
    lines.append("=== AI Time Machines Workflow Results ===")
    lines.append(f"Success: {result['success']}")
    lines.append(f"Repository: {result['context']['repository_owner']}/{result['context']['repository_name']}")
    lines.append(f"Execution Time: {result['execution_time']:.2f}s")
    lines.append("")
    
    processed_prs = result['processed_prs']
    if processed_prs:
        lines.append("Processed Pull Requests:")
        for pr_number, pr_info in processed_prs.items():
            if pr_info:
                lines.append(f"  #{pr_number}: {pr_info['title']} ({pr_info['state']})")
            else:
                lines.append(f"  #{pr_number}: Failed to process")
        lines.append("")
    
    if result['errors']:
        lines.append("Errors:")
        for error in result['errors']:
            lines.append(f"  - {error}")
        lines.append("")
    
    return "\n".join(lines)


def main():
    """Main CLI entry point."""
    args = parse_arguments()
    
    # Validate configuration if requested
    if args.validate:
        if validate_github_auth():
            print("✓ GitHub authentication is configured correctly")
            return 0
        else:
            print("✗ GitHub authentication is not configured")
            print("Please set the GITHUB_TOKEN environment variable")
            return 1
    
    try:
        # Handle JSON input
        if args.json:
            input_data = json.loads(sys.stdin.read())
        else:
            input_data = build_input_data(args)
        
        # Validate we have enough information
        if not input_data:
            print("Error: No input data provided. Use --help for usage information.")
            return 1
        
        # Process the automation request
        result = process_automation_request(input_data)
        
        # Output results
        output = format_output(result, args.output_format)
        print(output)
        
        # Return appropriate exit code
        return 0 if result['success'] else 1
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())