"""
Pytest Configuration

This module configures the Python path for test discovery and provides
shared fixtures for all tests.
"""

import sys
from pathlib import Path

# Add the project root to Python path so 'src' can be imported
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
