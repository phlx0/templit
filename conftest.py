# conftest.py
# Ensures the package root is on sys.path so pytest can import `templit`
# without requiring `pip install -e .` first.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
