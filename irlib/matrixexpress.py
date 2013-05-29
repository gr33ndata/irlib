''' 
Informations Retrieval Library
==============================
MatrixExpress is a compact index for terms and classes. 
'''

# Author: Tarek Amr <@gr33ndata> 

import sys, math
from matrix import Matrix
from superlist import SuperList

class MatrixExpress(Matrix)

    def add_doc(self, doc_id = '', doc_class='', doc_terms=[], 
                frequency=False, do_padding=False):
        ''' Add new document to our matrix:
            doc_id: Identifier for the document, eg. file name, url, etc. 
            doc_class: You might need this in classification.
            doc_terms: List of terms you got after tokenizing the document.
                       Terms can be typles; string and frequencies
            frequency: If true, term occurences is incremented by one.
                        Else, occurences is only 0 or 1 (a la Bernoulli)
            do_padding: Boolean. Check do_padding() for more info.
        ''' 
        # Update list of terms if new term seen.
        # And document (row) with its associated data.
        my_doc_terms = SuperList()
        # Discard anything not in whitelist if it is not empty
        if self.whitelist:
            doc_terms = [t for t in doc_terms if t in self.whitelist]
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
        self.docs.append({  'id': doc_id, 
                            'class': doc_class, 
                            'terms': my_doc_terms})
        # Update list of document classes if new class seen.
        #self.classes.unique_append(doc_class)
        #if self.classes.has_key(doc_class):
        #else:
        #    self.classes[doc_class].add(my_doc_terms)
        #    self.classes[doc_class] = my_doc_terms
        if do_padding: 
            self.do_padding()
