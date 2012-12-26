''' 
Informations Retrieval Library
==============================
Matrix is an index for documents, terms, and their classes. 
'''

# Author: Tarek Amr <@gr33ndata> 

from superlist import SuperList

class Matrix:

    def __init__(self):
        self.terms = SuperList()
        self.docs = []

	def do_padding(self):
        ''' Align the length of all rows in matrix
            Each time we see a new term, list of terms is expanded,
            and the matrix row for such document is of same length too.
            But what about rows added earlier for previous documents?
            So, this method alighn all previously added rows, 
            to match the current length of the terms list.
        '''
		for doc in self.docs:
			doc['terms'].expand(new_len=len(self.terms))

    def add_doc(self, doc_id = '', doc_class='', doc_terms=[], 
                frequency=False, do_padding=False):
        ''' Add new document to our matrix:
            doc_id: Identifier for the document, eg. file name, url, etc. 
            doc_class: You might need this in classification.
            doc_terms: List of terms you got after tokenizing the document.
            frequency: If true, term occurences is incremented by one.
                        Else, occurences is only 0 or 1 (a la Bernoulli)
            do_padding: Boolean. Check do_padding() for more info.
        '''
		my_doc_terms = SuperList()
		for term in doc_terms:
			term_idx = self.terms.unique_append(term)
			#my_doc_terms.insert_after_padding(self.terms.index(term))
            if frequency:
                my_doc_terms.increment_after_padding(term_idx,1)
            else:
                my_doc_terms.insert_after_padding(term_idx,1)
                
		self.docs.append({  'id': doc_id, 
                            'class': doc_class, 
                            'terms': my_doc_terms})
		if do_padding: self.do_padding()


if __name__ == '__main__':

    pass
