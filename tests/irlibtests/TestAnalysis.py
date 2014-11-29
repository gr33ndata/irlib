from unittest import TestCase

from irlib.analysis import Freq

class TestAnalysis(TestCase):

    def setUp(self):
        pass

    def test_freq_existing_term(self):
        f = Freq()
        f.add(['green', 'apple', 'juice'])
        f.add(['orange', 'orange', 'juice'])
        f.add(['sweet', 'apple', 'pie'])
        apple_freq = f['apple']
        self.assertEqual(apple_freq, 2)

    def test_freq_non_existing_term(self):
        f = Freq()
        f.add(['apple', 'juice'])
        f.add(['apple', 'pie'])
        orange_freq = f['orange']
        self.assertEqual(orange_freq, -1) 

    def test_freq_compare(self):
        f = Freq()
        cmp_val_gt = f.freq_cmp(
            {'token': 'orange', 'freq': 3},
            {'token': 'apple',  'freq': 2}
        )
        self.assertEqual(cmp_val_gt, 1) 
        cmp_val_lt = f.freq_cmp(
            {'token': 'orange', 'freq': 2},
            {'token': 'apple',  'freq': 3}
        )
        self.assertEqual(cmp_val_lt, -1) 

    def test_to_array(self):
        f = Freq()
        f.add(['apple', 'juice'])
        f.add(['apple', 'pie'])
        returned_array = f.to_array()
        expected_array = [
            {'token': 'apple', 'freq': 2},
            {'token': 'juice', 'freq': 1}, 
            {'token': 'pie', 'freq': 1}
        ]
        self.assertItemsEqual(returned_array, expected_array)

    def test_topn_value(self):
        f = Freq()
        f.add(['apple', 'not', 'orange', 'juice'])
        f.add(['apple', 'and', 'cinnamon', 'pie'])
        returned_array = f.topn(1)
        expected_array = [
            {'token': 'apple', 'freq': 2}
        ]
        self.assertEqual(returned_array, expected_array)

    def test_topn_len(self):
        f = Freq()
        f.add(['apple', 'not', 'orange', 'juice'])
        f.add(['apple', 'and', 'cinnamon', 'pie'])
        returned_array = f.topn(5)
        self.assertEqual(len(returned_array), 5)

    def test_len(self):
        f = Freq()
        f.add(['apple', 'not', 'orange', 'juice'])
        f.add(['apple', 'and', 'cinnamon', 'pie'])
        self.assertEqual(len(f), 7)
