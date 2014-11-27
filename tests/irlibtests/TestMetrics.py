from unittest import TestCase

from irlib.metrics import Metrics

class TestMetrics(TestCase):

    def setUp(self):
        self.m = Metrics()

    def test_jaccard_same_len(self):
        with self.assertRaises(ValueError):
            self.m.jaccard_vectors(
                [0, 1],
                [0, 1, 2, 3]
            )

    def test_jaccard_empty(self):
        e = self.m.jaccard_vectors([],[])
        self.assertEqual(e,1)

    def test_jaccard_int(self):
        e = self.m.jaccard_vectors(
            [0, 2, 1, 3],
            [0, 1, 2, 3]
        )
        self.assertEqual(e,0.75)
    
    def test_jaccard_bool(self):
        e = self.m.jaccard_vectors(
            [False, False, True, True, True ],
            [False, True , True, True, False]
        )
        self.assertEqual(e,0.4)

    def test_euclid_same_len(self):
        with self.assertRaises(ValueError):
            self.m.euclid_vectors(
                [0, 1, 2, 3],
                [0, 1]
            )

    def test_euclid(self):
        e = self.m.euclid_vectors([1,1],[4,5])
        self.assertEqual(e,5)

    def test_cos_same_len(self):
        with self.assertRaises(ValueError):
            self.m.cos_vectors(
                [0, 1, 2],
                [1, 1]
            )

    def test_cos_0(self):
        c = self.m.cos_vectors([1,0,1],[0,1,0])
        self.assertEqual(round(c,5),float(0))

    def test_cos_1(self):
        c = self.m.cos_vectors([1,1,1],[1,1,1])
        self.assertEqual(round(c,5),float(1)) 

