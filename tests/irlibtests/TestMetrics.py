from unittest import TestCase

from irlib.metrics import Metrics

class TestMetrics(TestCase):

    def setUp(self):
        self.m = Metrics()

    def test_euclid_distance(self):
        e = self.m.euclid_vectors([1,1],[4,5])
        self.assertEqual(e,5)

    def test_cos_distance_0(self):
        c = self.m.cos_vectors([1,0,1],[0,1,0])
        self.assertEqual(round(c,5),float(0))

    def test_cos_distance_1(self):
        c = self.m.cos_vectors([1,1,1],[1,1,1])
        self.assertEqual(round(c,5),float(1)) 
