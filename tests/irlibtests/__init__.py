import os
import sys

# Append IRLib to System Path
cwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(cwd, '..', '..'))

import irlib
