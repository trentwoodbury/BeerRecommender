import os
import sys

PROJECT_ROOT = os.path.dirname(__file__)
ABS_PATH = os.path.join(PROJECT_ROOT, os.pardir)
sys.path.insert(0, ABS_PATH)

import recommender_package
