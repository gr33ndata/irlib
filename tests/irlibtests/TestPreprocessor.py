from unittest import TestCase

from irlib.preprocessor import Preprocessor, my_nltk

class TestPreprocessor(TestCase):

    def setUp(self):
        pass        

    def test_term2ch(self):
        p = Preprocessor()
        charlist = p.term2ch('help')
        self.assertEqual(charlist, ['h', 'e', 'l', 'p']) 

    def test_stemmer(self):
        p = Preprocessor(stem=True)
        stemmed = p.stemmer('running')
        if my_nltk:
            self.assertEqual(stemmed,'run')  
        else: 
            self.assertTrue(False,'NLTK is not installed') 
