import os
import sys

def get_irlibtests_path():
    return os.path.dirname(os.path.realpath(__file__))

def get_irlib_path():
    return os.path.join(get_irlibtests_path(), '..', '..')

sys.path.append(get_irlib_path())

import irlib

from irlibtests.TestSuperList import TestSuperList
from irlibtests.TestMatrix import TestMatrix
from irlibtests.TestMetrics import TestMetrics
from irlibtests.TestProgress import TestProgress