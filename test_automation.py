"""Tests for AI Time Machines automation functionality."""

import unittest
from unittest.mock import Mock, patch, MagicMock
import os
import tempfile

from config import Settings, get_repo_info, validate_github_auth
from pr_handler import extract_pr_number_from_url, extract_repo_from_url, PRInfo, PRProcessor
from workflow import WorkflowEngine, WorkflowContext


class TestConfig(unittest.TestCase):
    """Test configuration management."""
    
    def test_get_repo_info_with_parameters(self):
        """Test getting repo info with explicit parameters."""
        owner, name = get_repo_info("testowner", "testrepo")
        self.assertEqual(owner, "testowner")
        self.assertEqual(name, "testrepo")
    
    def test_get_repo_info_missing_params(self):
        """Test error when required parameters are missing."""
        with self.assertRaises(ValueError):
            get_repo_info()
    
    def test_validate_github_auth_without_token(self):
        """Test auth validation without token."""
        with patch('config.settings') as mock_settings:
            mock_settings.github_token = None
            self.assertFalse(validate_github_auth())


class TestPRHandler(unittest.TestCase):
    """Test pull request handling functionality."""
    
    def test_extract_pr_number_from_url(self):
        """Test extracting PR number from URL."""
        url = "https://github.com/owner/repo/pull/123"
        pr_number = extract_pr_number_from_url(url)
        self.assertEqual(pr_number, 123)
    
    def test_extract_pr_number_invalid_url(self):
        """Test handling invalid URLs."""
        invalid_url = "https://github.com/owner/repo"
        pr_number = extract_pr_number_from_url(invalid_url)
        self.assertIsNone(pr_number)
    
    def test_extract_repo_from_url(self):
        """Test extracting repository info from URL."""
        url = "https://github.com/testowner/testrepo/pull/123"
        repo_info = extract_repo_from_url(url)
        self.assertEqual(repo_info, ("testowner", "testrepo"))
    
    def test_extract_repo_invalid_url(self):
        """Test handling invalid repository URLs."""
        invalid_url = "https://example.com/invalid"
        repo_info = extract_repo_from_url(invalid_url)
        self.assertIsNone(repo_info)
    
    def test_pr_info_creation(self):
        """Test PRInfo data class creation."""
        # Mock GitHub PR object
        mock_pr = Mock()
        mock_pr.number = 123
        mock_pr.title = "Test PR"
        mock_pr.state = "open"
        mock_pr.user.login = "testuser"
        mock_pr.html_url = "https://github.com/owner/repo/pull/123"
        mock_pr.created_at.isoformat.return_value = "2023-01-01T00:00:00"
        mock_pr.updated_at.isoformat.return_value = "2023-01-01T00:00:00"
        mock_pr.mergeable = True
        
        pr_info = PRInfo.from_github_pr(mock_pr, "owner/repo")
        
        self.assertEqual(pr_info.number, 123)
        self.assertEqual(pr_info.title, "Test PR")
        self.assertEqual(pr_info.state, "open")
        self.assertEqual(pr_info.author, "testuser")
        self.assertEqual(pr_info.repository, "owner/repo")


class TestWorkflow(unittest.TestCase):
    """Test workflow engine functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = WorkflowEngine()
    
    def test_create_context_from_input_basic(self):
        """Test creating workflow context from basic input."""
        input_data = {
            "repository_owner": "testowner",
            "repository_name": "testrepo",
            "pull_request_numbers": [123, 124]
        }
        
        context = self.engine.create_context_from_input(input_data)
        
        self.assertEqual(context.repository_owner, "testowner")
        self.assertEqual(context.repository_name, "testrepo")
        self.assertEqual(context.pull_request_numbers, [123, 124])
    
    def test_create_context_from_url(self):
        """Test creating context from PR URL."""
        input_data = {
            "repository_owner": "testowner",
            "repository_name": "testrepo",
            "pull_request_urls": ["https://github.com/testowner/testrepo/pull/123"]
        }
        
        context = self.engine.create_context_from_input(input_data)
        
        self.assertEqual(context.pull_request_numbers, [123])
    
    def test_create_context_repo_from_url(self):
        """Test extracting repository info from URL."""
        input_data = {
            "repository_url": "https://github.com/testowner/testrepo",
            "pull_request_numbers": [123]
        }
        
        context = self.engine.create_context_from_input(input_data)
        
        self.assertEqual(context.repository_owner, "testowner")
        self.assertEqual(context.repository_name, "testrepo")
    
    def test_workflow_context_to_dict(self):
        """Test converting workflow context to dictionary."""
        context = WorkflowContext(
            repository_owner="testowner",
            repository_name="testrepo",
            pull_request_numbers=[123],
            timestamp="2023-01-01T00:00:00",
            metadata={"test": "value"}
        )
        
        context_dict = context.to_dict()
        
        self.assertEqual(context_dict["repository_owner"], "testowner")
        self.assertEqual(context_dict["pull_request_numbers"], [123])
        self.assertEqual(context_dict["metadata"]["test"], "value")


class TestIntegration(unittest.TestCase):
    """Integration tests without requiring real GitHub access."""
    
    @patch('pr_handler.ensure_authorized')
    def test_pr_processor_initialization(self, mock_ensure_authorized):
        """Test PR processor initialization."""
        mock_github_client = Mock()
        mock_ensure_authorized.return_value = mock_github_client
        
        processor = PRProcessor("testowner", "testrepo")
        
        self.assertIsNotNone(processor)
        self.assertEqual(processor.repo_owner, "testowner")
        self.assertEqual(processor.repo_name, "testrepo")
        mock_ensure_authorized.assert_called_once()
    
    @patch('workflow.process_automation_request')
    def test_automation_request_processing(self, mock_process):
        """Test processing automation request."""
        mock_process.return_value = {
            "success": True,
            "context": {"repository_owner": "test", "repository_name": "repo"},
            "processed_prs": {},
            "errors": [],
            "execution_time": 1.0
        }
        
        from workflow import process_automation_request
        
        input_data = {
            "repository_owner": "test",
            "repository_name": "repo",
            "pull_request_numbers": [123]
        }
        
        result = process_automation_request(input_data)
        
        self.assertTrue(result["success"])
        mock_process.assert_called_once_with(input_data)


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)