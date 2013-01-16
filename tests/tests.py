#!/usr/bin/env python

import sys
import unittest

sys.path.append('../')
from irlib.superlist import SuperList
from irlib.matrix import Matrix, Stats
from irlib.metrics import Metrics
 
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
        self.assertEqual(self.x[7],99)
        self.x.insert_after_padding(1,99)
        self.assertEqual(self.x[1],99)

    def test_increment_after_padding(self):
        self.x.increment_after_padding(7,99)
        self.assertEqual(self.x[7],99)
        self.x.increment_after_padding(1,99)
        self.assertEqual(self.x[1],100)

class TestMetrics(unittest.TestCase):

    def setUp(self):
        self.m = Metrics()

    def test_metrics(self):
        e = self.m.euclid_vectors([1,1],[4,5])
        self.assertEqual(e,5)
        c = self.m.cos_vectors([1,1,1],[1,1,1])
        self.assertEqual(round(c,5),float(1))
        c = self.m.cos_vectors([1,0,1],[0,1,0])
        self.assertEqual(round(c,5),float(0))

class TestMatrix(unittest.TestCase):

    def setUp(self):
        self.m = Matrix()

    def test_add_doc(self):
        # Try without frequency
        self.assertEqual(len(self.m),0)
        doc1_terms = ['buy', 'now', 'or', 'buy', 'later']
        self.m.add_doc( doc_id = 'file_spam.txt', 
                        doc_class='Spam', 
                        doc_terms= doc1_terms,
                        frequency=False)
        self.assertEqual(self.m.terms, ['buy', 'now', 'or', 'later'])
        self.assertEqual(self.m.docs[0]['terms'], [1,1,1,1])
        # Now try with frequency
        doc2_terms = ['buy', 'today', 'or', 'buy', 'later']
        self.m.add_doc( doc_id = 'file_spam.txt', 
                        doc_class='Spam', 
                        doc_terms= doc2_terms,
                        frequency=True)
        self.assertEqual(self.m.terms, ['buy', 'now', 'or', 'later', 'today'])
        self.assertEqual(self.m.docs[1]['terms'], [2,0,1,1,1])
        # Now let's see if padding is working
        doc2_terms = ['buy', 'now']
        self.m.add_doc( doc_id = 'file_spam.txt', 
                        doc_class='Ham', 
                        doc_terms= doc2_terms,
                        frequency=True,
                        do_padding=True)
        self.assertEqual(len(self.m.terms), len(self.m.docs[0]['terms']))     
        self.assertEqual(len(self.m),3)
        self.assertEqual('buy' in self.m, True)
        self.assertEqual('shpping' in self.m, False)
        self.assertEqual(self.m.classes.keys().sort(), ['Spam', 'Ham'].sort())
        
        self.s = Stats(self.m)
        self.assertEqual(self.s.getN(), 11)
        self.assertEqual(self.s.pr_term('buy'), float(4)/self.s.getN())
        self.s.mi()
        
if __name__ == '__main__':
    unittest.main()
