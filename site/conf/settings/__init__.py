from .common import *

try:
    from local import *
except ImportError:
    print("Please, provide your local configuration for this project.\n"
          "You need to create conf/settings/local.py with your local settings.")
    import sys
    sys.exit(1)
