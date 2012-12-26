#!python

import sys
import unittest

sys.path.append('../')
from irlib.superlist import SuperList
 
class TestSuperList(unittest.TestCase):

    def test_unique_append(self):
        x = SuperList([1,2,3])
        len1 = len(x)
        x.unique_append(1)
        len2 = len(x)
        self.assertEqual(len1, len2)

if __name__ == '__main__':
    unittest.main()
