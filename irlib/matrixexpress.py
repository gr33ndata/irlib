''' 
Informations Retrieval Library
==============================
MatrixExpress is a compact index for terms and classes.
Insdead of having row for each doc, we have one for each class. 
'''

# Author: Tarek Amr <@gr33ndata> 

import sys, math
from matrix import Matrix
from superlist import SuperList

class MatrixExpress(Matrix):

    def add_doc(self, doc_id = '', doc_class='', doc_terms=[], 
                frequency=False, do_padding=False, stopwords=[]):
        ''' Add new document to our matrix:
            doc_id: Identifier for the document, eg. file name, url, etc. 
            doc_class: You might need this in classification.
            doc_terms: List of terms you got after tokenizing the document.
                       Terms can be typles; string and frequencies
            frequency: If true, term occurences is incremented by one.
                        Else, occurences is only 0 or 1 (a la Bernoulli)
            do_padding: Boolean. Useless here
            stopwords: If not empty, ignore those stop words in doc_terms
        ''' 
        # Update list of terms if new term seen.
        # And document (row) with its associated data.
        my_doc_terms = SuperList()
        # Discard anything not in whitelist if it is not empty
        if self.whitelist:
            doc_terms = [t for t in doc_terms if t in self.whitelist]
        # Discard anything in stopwords if not empty
        if stopwords:
            doc_terms = [t for t in doc_terms if t not in stopwords]
        for term in doc_terms:
            if type(term) == tuple:
                term_idx = self.terms.unique_append(term[0])
                my_doc_terms.increment_after_padding(term_idx,term[1])
            else:
                term_idx = self.terms.unique_append(term)
                if frequency:
                    my_doc_terms.increment_after_padding(term_idx,1)
                else:
                    my_doc_terms.insert_after_padding(term_idx,1)
        #self.docs.append({  'id': doc_id, 
        #                    'class': doc_class, 
        #                    'terms': my_doc_terms})
        found = 0
        for doc in self.docs:
            if doc['class'] == doc_class:
                doc['terms'].add(my_doc_terms)
                found = 1
        if not found:        
            self.docs.append({'id': doc_id, 
                              'class': doc_class, 
                              'terms': my_doc_terms}) 
        if do_padding: 
            self.do_padding()  
                     
if __name__ == '__main__':

    mx = MatrixExpress()
    mx.add_doc(doc_id='1',
               doc_terms=['apple', 'mac', 'iphone', 'internet'],
               doc_class= 'apple',
               frequency=True, do_padding=True, stopwords=['internet'])
    mx.add_doc(doc_id='2',
               doc_terms=['windows', 'word', 'excel', 'internet'],
               doc_class= 'microsoft',
               frequency=True, do_padding=True, stopwords=['internet'])
    mx.add_doc(doc_id='3',
               doc_terms=['computer', 'mac', ('ipad', 10)],
               doc_class= 'apple',
               frequency=True, do_padding=True, stopwords=['internet'])
    mx.add_doc(doc_id='4',
               doc_terms=['excel', ('computer', 10), 'office'],
               doc_class= 'microsoft',
               frequency=True, do_padding=True, stopwords=['internet'])
    print mx
    print mx.terms
    for doc in mx.docs:
        print doc['class'], doc['terms'] 
        
    thresholds, freqs = mx.freq_levels(threshold=3) 
    print 'Threshold Map:', thresholds
    print mx.vocabulary(threshold_map=thresholds) 
    


