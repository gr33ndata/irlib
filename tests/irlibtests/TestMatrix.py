from unittest import TestCase

from irlib.matrix import Matrix

class TestMatrix(TestCase):

    def setUp(self):
        self.m = Matrix()

    def test_add_doc(self):
        # Try without frequency
        self.assertEqual(len(self.m),0)
        doc1_terms = ['buy', 'now', 'or', 'buy', 'later']
        self.m.add_doc( doc_id = 'file_spam.txt', 
                        doc_class='Spam', 
                        doc_terms= doc1_terms,
                        frequency=False)
        self.assertEqual(self.m.terms, ['buy', 'now', 'or', 'later'])
        self.assertEqual(self.m.docs[0]['terms'], [1,1,1,1])
        # Now try with frequency
        doc2_terms = ['buy', 'today', 'or', 'buy', 'later']
        self.m.add_doc( doc_id = 'file_spam.txt', 
                        doc_class='Spam', 
                        doc_terms= doc2_terms,
                        frequency=True)
        self.assertEqual(self.m.terms, ['buy', 'now', 'or', 'later', 'today'])
        self.assertEqual(self.m.docs[1]['terms'], [2,0,1,1,1])
        # Now let's see if padding is working
        doc2_terms = ['buy', 'now']
        self.m.add_doc( doc_id = 'file_spam.txt', 
                        doc_class='Ham', 
                        doc_terms= doc2_terms,
                        frequency=True,
                        do_padding=True)
        #print self.m.terms, self.m.docs[0]['terms']
        self.assertEqual(len(self.m.terms), len(self.m.docs[0]['terms'])) 
        self.assertEqual(len(self.m),3)
        self.assertEqual('buy' in self.m, True)
        self.assertEqual('shopping' in self.m, False)
        
        # The statistical class is removed for now.
        #self.assertEqual(self.m.classes.keys().sort(), ['Spam', 'Ham'].sort())
        #self.s = Stats(self.m)
        #self.assertEqual(self.s.getN(), 11)
        #self.assertEqual(self.s.pr_term('buy'), float(4)/self.s.getN())
        #self.s.mi()
