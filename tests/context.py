'''Provides context for importing modules for testing.
   Code adapted from
   [Python Guide](http://docs.python-guide.org/en/latest/writing/structure/)
   Usage example:
   from .context import interface'''

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import interface
import rotation
