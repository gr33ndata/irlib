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

    def test_stemmer_lower(self):
        p = Preprocessor(lower=True, stem=True)
        stemmed = p.stemmer('Running')
        if my_nltk:
            self.assertEqual(stemmed,'run')  
        else: 
            self.assertTrue(False,'NLTK is not installed') 
                    
    def test_tokenizer_lower(self):
        p = Preprocessor(lower=True, stem=False)
        tokens = p.tokenizer('This is IRLib')
        self.assertEqual(tokens,['this','is','irlib'])

    def test_2gram_tokenizer(self):
        p = Preprocessor(lower=False, stem=False, ngram=2)
        returned_tokens = p.ngram_tokenizer('how do you do?')
        expected_tokens = ['how do', 'do you', 'you do']
        self.assertEqual(returned_tokens, expected_tokens)

    def test_3gram_tokenizer(self):
        p = Preprocessor(lower=False, stem=False, ngram=3)
        returned_tokens = p.ngram_tokenizer('how do you do?')
        expected_tokens = ['how do you', 'do you do']
        self.assertEqual(returned_tokens, expected_tokens)

    def test_is_mention(self):
        is_it = Preprocessor.is_mention('@twitter')
        self.assertEqual(is_it, True)
        is_it = Preprocessor.is_mention('#twitter')
        self.assertEqual(is_it, False)

    def test_is_hashtag(self):
        is_it = Preprocessor.is_hashtag('@twitter')
        self.assertEqual(is_it, False)
        is_it = Preprocessor.is_hashtag('#twitter')
        self.assertEqual(is_it, True)

    def test_is_link(self):
        is_it = Preprocessor.is_link('hello world')
        self.assertEqual(is_it, False)
        is_it = Preprocessor.is_link('http://www.yahoo.com')
        self.assertEqual(is_it, True)
        is_it = Preprocessor.is_link('https://www.yahoo.com')
        self.assertEqual(is_it, True)
        is_it = Preprocessor.is_link('www.yahoo.com')
        self.assertEqual(is_it, True)
