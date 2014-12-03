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

    def test_add_doc_empty(self):
        doc1_terms = []
        with self.assertRaises(ValueError):
            self.m.add_doc( doc_id = 'doc1', 
                            doc_class='Spam', 
                            doc_terms= doc1_terms)

    def test_query_alignment(self):
        doc1_terms = ['buy', 'now', 'or', 'buy', 'later']
        self.m.add_doc( doc_id = 'file_spam.txt', 
                        doc_class='Spam', 
                        doc_terms= doc1_terms,
                        frequency=False)
        q_vector = self.m.query_to_vector(['best', 'buy'], frequency=False)
        self.assertEqual(q_vector, [1,0,0,0]) 

    def test_tf_idf(self):
        doc1_terms = ['new', 'york', 'times']
        self.m.add_doc( doc_id = 'doc1', 
                        doc_class='Spam', 
                        doc_terms= doc1_terms,
                        do_padding=True,
                        frequency=True)
        doc2_terms = ['new', 'york', 'post']
        self.m.add_doc( doc_id = 'doc2', 
                        doc_class='Spam', 
                        doc_terms= doc2_terms,
                        do_padding=True,
                        frequency=True)
        doc3_terms = ['los', 'angeles', 'times']
        self.m.add_doc( doc_id = 'doc3', 
                        doc_class='Spam', 
                        doc_terms= doc3_terms,
                        do_padding=True,
                        frequency=True)
        self.m.tf_idf(log_base=2)
        doc1_tfidf_retval = self.m.docs[0]['terms']
        doc1_tfidf_retval = [round(item, 3) for item in doc1_tfidf_retval]
        doc1_tfidf_expval = [0.585, 0.585, 0.585, 0, 0, 0]
        self.assertEqual(doc1_tfidf_retval, doc1_tfidf_expval)