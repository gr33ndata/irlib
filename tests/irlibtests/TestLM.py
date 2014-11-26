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

    def helper_test_ngrams(self, n, sent, expected_ngrams):
        lm = LM(n=n)
        ngrams_returned = lm.to_ngrams(sent.split())
        self.assertEqual(ngrams_returned, expected_ngrams)

    def test_ngram1(self):
        self.helper_test_ngrams(
            n=1, 
            sent='i like apples and oranges',
            expected_ngrams=[
                ['i'], ['like'], ['apples'], ['and'], ['oranges']
            ]
        )

    def test_ngram2(self):
        self.helper_test_ngrams(
            n=2, 
            sent='i like apples and oranges',
            expected_ngrams=[
                ['i', 'like'], 
                ['like', 'apples'], 
                ['apples', 'and'], 
                ['and', 'oranges']
            ]
        )

    def test_ngram3(self):
        self.helper_test_ngrams(
            n=3, 
            sent='i like apples and oranges',
            expected_ngrams=[
                ['i', 'like', 'apples'],
                ['like', 'apples', 'and'],
                ['apples', 'and', 'oranges']
            ]
        )
    