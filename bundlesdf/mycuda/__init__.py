import os
import sys
import torch

# Add the libs directory to the library path at import time
package_dir = os.path.dirname(__file__)
torch_lib_dir = os.path.join(os.path.dirname(torch.__file__), 'lib')

if os.path.exists(torch_lib_dir):
    # Add to LD_LIBRARY_PATH for Linux
    if 'LD_LIBRARY_PATH' in os.environ:
        os.environ['LD_LIBRARY_PATH'] = f"{torch_lib_dir}:{os.environ['LD_LIBRARY_PATH']}"
    else:
        os.environ['LD_LIBRARY_PATH'] = torch_lib_dir
    
    # For macOS, also set DYLD_LIBRARY_PATH
    if sys.platform == 'darwin':
        if 'DYLD_LIBRARY_PATH' in os.environ:
            os.environ['DYLD_LIBRARY_PATH'] = f"{torch_lib_dir}:{os.environ['DYLD_LIBRARY_PATH']}"
        else:
            os.environ['DYLD_LIBRARY_PATH'] = torch_lib_dir

# Now import the actual modules
from .common import *
from .gridencoder import *
