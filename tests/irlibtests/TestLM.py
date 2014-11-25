from unittest import TestCase

from irlib.lm import LM

class TestLM(TestCase):

    def setUp(self):
        pass

    def test_vocabulary(self):
        lm = LM()
        lm.add_doc(doc_id='doc1', doc_terms='apple tree'.split())
        lm.add_doc(doc_id='doc2', doc_terms='orange juice'.split())
        vocab_returned = lm.get_vocabulary()
        vocab_expected = set(['apple','tree','orange','juice'])
        self.assertEqual(vocab_returned, vocab_expected)

    def test_ngram1(self):
        lm = LM(n=1)
        ngrams_returned = lm.to_ngrams('i like apples and oranges'.split())
        ngrams_expected = [
            ['i'], ['like'], ['apples'], ['and'], ['oranges']
        ]
        self.assertEqual(ngrams_returned, ngrams_expected)

    def test_ngram2(self):
        lm = LM(n=2)
        ngrams_returned = lm.to_ngrams('i like apples and oranges'.split())
        ngrams_expected = [
            ['i', 'like'], 
            ['like', 'apples'], 
            ['apples', 'and'], 
            ['and', 'oranges']
        ]
        self.assertEqual(ngrams_returned, ngrams_expected)

    def test_ngram3(self):
        lm = LM(n=3)
        ngrams_returned = lm.to_ngrams('i like apples and oranges'.split())
        ngrams_expected = [
            ['i', 'like', 'apples'],
            ['like', 'apples', 'and'],
            ['apples', 'and', 'oranges']
        ]
        self.assertEqual(ngrams_returned, ngrams_expected)
    