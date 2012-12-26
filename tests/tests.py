#!python

import sys
import unittest

sys.path.append('../')
from irlib.superlist import SuperList
 
class TestSuperList(unittest.TestCase):

    def setUp(self):
        self.x = SuperList([0,1,2,3])
        self.y = SuperList([0,1,2,3])

    def test_unique_append(self):
        new_item = 1
        i = self.x.unique_append(new_item)
        self.assertEqual(i, new_item)
        self.assertEqual(self.x, self.y)
        new_item = 4
        i = self.x.unique_append(new_item)
        self.assertEqual(i, new_item)
        self.assertNotEqual(self.x, self.y)

    def test_insert_after_padding(self):
        self.x.insert_after_padding(7,99)
        self.assertEqual( self.x[7],99)
        self.x.insert_after_padding(1,99)
        self.assertEqual( self.x[1],99)

    def test_increment_after_padding(self):
        self.x.increment_after_padding(7,99)
        self.assertEqual( self.x[7],99)
        self.x.increment_after_padding(1,99)
        self.assertEqual( self.x[1],100)

if __name__ == '__main__':
    unittest.main()
