name = "cscmiko"
import sys
import os
from .devices import *

__version__ = '0.0.9'
# Verify Python Version
try:
    if not sys.version_info.major == 3:
        raise RuntimeError('cscmiko requires Python3')
except AttributeError:
    raise RuntimeError('cscmiko requires Python3')

# set fetch-template env variable
dir_path = os.path.dirname(os.path.realpath(__file__))
os.environ["NET_TEXTFSM"] = dir_path + "/fetch-templates/templates"

