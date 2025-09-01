"""Automation workflow engine for AI Time Machines."""

import json
import logging
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, asdict
from datetime import datetime

from pr_handler import PRProcessor, PRInfo, extract_pr_number_from_url, extract_repo_from_url
from config import settings


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class WorkflowContext:
    """Context information for workflow execution."""
    repository_owner: str
    repository_name: str
    pull_request_numbers: List[int]
    timestamp: str
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class WorkflowResult:
    """Result of workflow execution."""
    success: bool
    context: WorkflowContext
    processed_prs: Dict[int, PRInfo]
    errors: List[str]
    execution_time: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        # Convert PRInfo objects to dicts
        result['processed_prs'] = {
            k: asdict(v) if v else None 
            for k, v in self.processed_prs.items()
        }
        return result


class WorkflowEngine:
    """Main automation workflow engine."""
    
    def __init__(self):
        """Initialize workflow engine."""
        self.processors: Dict[str, PRProcessor] = {}
        self.hooks: Dict[str, List[Callable]] = {
            'pre_process': [],
            'post_process': [],
            'on_error': []
        }
    
    def get_processor(self, repo_owner: str, repo_name: str) -> PRProcessor:
        """Get or create PR processor for repository."""
        key = f"{repo_owner}/{repo_name}"
        if key not in self.processors:
            self.processors[key] = PRProcessor(repo_owner, repo_name)
        return self.processors[key]
    
    def add_hook(self, hook_type: str, callback: Callable):
        """Add a callback hook to the workflow."""
        if hook_type in self.hooks:
            self.hooks[hook_type].append(callback)
    
    def _execute_hooks(self, hook_type: str, context: WorkflowContext, **kwargs):
        """Execute all hooks of a given type."""
        for hook in self.hooks.get(hook_type, []):
            try:
                hook(context, **kwargs)
            except Exception as e:
                logger.error(f"Hook execution failed: {e}")
    
    def create_context_from_input(self, 
                                  input_data: Dict[str, Any]) -> WorkflowContext:
        """Create workflow context from various input formats."""
        # Extract repository information
        repo_owner = input_data.get('repository_owner')
        repo_name = input_data.get('repository_name')
        
        # Try to extract from URL if not provided directly
        if not repo_owner or not repo_name:
            repo_url = input_data.get('repository_url')
            if repo_url:
                repo_info = extract_repo_from_url(repo_url)
                if repo_info:
                    repo_owner, repo_name = repo_info
        
        # Use defaults if still not found
        if not repo_owner or not repo_name:
            from config import get_repo_info
            repo_owner, repo_name = get_repo_info(repo_owner, repo_name)
        
        # Extract PR numbers from various sources
        pr_numbers = []
        
        # Direct PR numbers
        if 'pull_request_numbers' in input_data:
            pr_numbers.extend(input_data['pull_request_numbers'])
        
        # Single PR number
        if 'pull_request_number' in input_data:
            pr_numbers.append(input_data['pull_request_number'])
        
        # PR URLs
        pr_urls = input_data.get('pull_request_urls', [])
        if isinstance(pr_urls, str):
            pr_urls = [pr_urls]
        
        for url in pr_urls:
            pr_number = extract_pr_number_from_url(url)
            if pr_number:
                pr_numbers.append(pr_number)
        
        # Auto-discover PRs if none specified
        if not pr_numbers and input_data.get('auto_discover', False):
            processor = self.get_processor(repo_owner, repo_name)
            discovered_prs = processor.auto_discover_prs(
                pattern=input_data.get('discovery_pattern')
            )
            pr_numbers = [pr.number for pr in discovered_prs]
        
        return WorkflowContext(
            repository_owner=repo_owner,
            repository_name=repo_name,
            pull_request_numbers=list(set(pr_numbers)),  # Remove duplicates
            timestamp=datetime.now().isoformat(),
            metadata=input_data.get('metadata', {})
        )
    
    def execute_workflow(self, input_data: Dict[str, Any]) -> WorkflowResult:
        """Execute the main automation workflow."""
        start_time = datetime.now()
        errors = []
        processed_prs = {}
        
        try:
            # Create workflow context
            context = self.create_context_from_input(input_data)
            logger.info(f"Starting workflow for {context.repository_owner}/{context.repository_name}")
            logger.info(f"Processing PRs: {context.pull_request_numbers}")
            
            # Execute pre-process hooks
            self._execute_hooks('pre_process', context)
            
            # Get processor for this repository
            processor = self.get_processor(context.repository_owner, context.repository_name)
            
            # Process pull requests
            if context.pull_request_numbers:
                # Respect batch size limits
                batch_size = min(len(context.pull_request_numbers), settings.max_pr_batch_size)
                pr_batch = context.pull_request_numbers[:batch_size]
                
                logger.info(f"Processing batch of {len(pr_batch)} PRs")
                processed_prs = processor.process_pr_batch(pr_batch)
                
                # Log results
                successful_prs = [k for k, v in processed_prs.items() if v is not None]
                failed_prs = [k for k, v in processed_prs.items() if v is None]
                
                logger.info(f"Successfully processed: {successful_prs}")
                if failed_prs:
                    logger.warning(f"Failed to process: {failed_prs}")
                    errors.append(f"Failed to process PRs: {failed_prs}")
            
            # Execute post-process hooks
            self._execute_hooks('post_process', context, processed_prs=processed_prs)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return WorkflowResult(
                success=len(errors) == 0,
                context=context,
                processed_prs=processed_prs,
                errors=errors,
                execution_time=execution_time
            )
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            errors.append(str(e))
            
            # Execute error hooks
            context = WorkflowContext(
                repository_owner="unknown",
                repository_name="unknown",
                pull_request_numbers=[],
                timestamp=datetime.now().isoformat(),
                metadata={}
            )
            self._execute_hooks('on_error', context, error=e)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return WorkflowResult(
                success=False,
                context=context,
                processed_prs=processed_prs,
                errors=errors,
                execution_time=execution_time
            )


# Global workflow engine instance
workflow_engine = WorkflowEngine()


def process_automation_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Main entry point for processing automation requests."""
    result = workflow_engine.execute_workflow(input_data)
    return result.to_dict()