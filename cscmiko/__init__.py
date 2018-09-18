name = "cscmiko"
import sys
from .devices import *



# Verify Python Version
try:
    if not sys.version_info.major == 3:
        raise RuntimeError('cscmiko requires Python3')
except AttributeError:
    raise RuntimeError('cscmiko requires Python3')
