import os
import sys

# fixes troubles with import at the tests runtime
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)
