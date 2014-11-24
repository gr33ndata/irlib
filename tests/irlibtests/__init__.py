import os
import sys

def is_test_file(myfile, mypath):
    if not os.path.isfile(os.path.join(mypath,myfile)):
        return False
    return (myfile.startswith('Test') and myfile.endswith('.py'))

def get_irlibtests_path():
    return os.path.dirname(os.path.realpath(__file__))

def get_irlib_path():
    return os.path.join(get_irlibtests_path(), '..', '..')

def get_irlibtests_tests():
    mypath = get_irlibtests_path()
    return [f.rsplit('.',1)[0] for f in os.listdir(mypath) if is_test_file(f,mypath)]

sys.path.append(get_irlib_path())

import irlib

from irlibtests.TestSuperList import TestSuperList
from irlibtests.TestMatrix import TestMatrix
from irlibtests.TestMetrics import TestMetrics
from irlibtests.TestProgress import TestProgress