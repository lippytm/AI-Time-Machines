"""Unit tests initialization."""

# This file makes the tests directory a Python package
import sys
from pathlib import Path

# Add the ai_time_machines package to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))