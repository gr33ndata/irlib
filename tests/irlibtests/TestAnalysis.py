from unittest import TestCase

from irlib.analysis import Freq

class TestAnalysis(TestCase):

    def setUp(self):
        pass

    def test_check_freq_existing_term(self):
        f = Freq()
        f.add(['apple', 'juice'])
        f.add(['apple', 'pie'])
        apple_freq = f['apple']
        self.assertEqual(apple_freq, 2)

    def test_check_freq_non_existing_term(self):
        f = Freq()
        f.add(['apple', 'juice'])
        f.add(['apple', 'pie'])
        orange_freq = f['orange']
        self.assertEqual(orange_freq, -1)   