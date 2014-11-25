from unittest import TestCase

from irlib.preprocessor import Preprocessor

class TestPreprocessor(TestCase):

    def setUp(self):
        self.p = Preprocessor()

    def test_term2ch(self):
        chz = self.p.term2ch('help')
        self.assertEqual(chz,['h', 'e', 'l', 'p'])   
