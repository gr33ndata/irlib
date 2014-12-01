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

    def test_tokenizer_lower(self):
        p = Preprocessor(lower=True, stem=False)
        tokens = p.tokenizer('This is IRLib')
        self.assertEqual(tokens,['this','is','irlib'])

    def test_ngram_tokenizer(self):
        p = Preprocessor(lower=False, stem=False, ngram=2)
        returned_tokens = p.ngram_tokenizer('how do you do?')
        expected_tokens = ['how do', 'do you', 'you do']
        self.assertEqual(returned_tokens, expected_tokens)
