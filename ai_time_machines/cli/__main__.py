"""CLI entry point for AI Time Machines."""

import sys
from pathlib import Path

# Add the parent directory to Python path for CLI execution
current_dir = Path(__file__).parent
parent_dir = current_dir.parent.parent
sys.path.insert(0, str(parent_dir))

from ai_time_machines.cli import main

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())