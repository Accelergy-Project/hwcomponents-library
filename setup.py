"""Setup.py to ensure hwcomponents._version_scheme is importable during build."""

import sys
from pathlib import Path

# Add paths to ensure hwcomponents can be imported
current_dir = Path(__file__).parent.absolute()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Try to find hwcomponents in parent directories (for submodule case)
parent_dir = current_dir.parent.parent
hwcomponents_dir = parent_dir / "hwcomponents"
if hwcomponents_dir.exists() and str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from setuptools import setup

setup()
