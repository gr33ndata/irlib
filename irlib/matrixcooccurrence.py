''' 
Informations Retrieval Library
==============================
MatrixCooccurrence: You give it a Matrix,
and it creates new co-occurrence matrix of its features
'''

# Author: Tarek Amr <@gr33ndata> 

import sys, math
from matrix import Matrix
from superlist import SuperList

from itertools import permutations

class MatrixCooccurrence(Matrix):

    def __init__(self, mx=None):
    
        self.orig_mx = mx
        self.terms = self.orig_mx.vocabulary()
        
        N = len(self.terms)
        square = [[0 for _ in range(0,N)] for _ in range(0,N)]
        for doc in self.orig_mx.docs:
            terms_indeces = self._nonzeros(doc['terms']) 
            for c in permutations(terms_indeces,2):
                square[c[0]][c[1]] += 1
            for cc in terms_indeces:
                square[cc][cc] += 1
        
        self.docs = []
        for i in range(len(self.terms)):
            self.docs.append({  'id': self.terms[i], 
                                'class': '', 
                                'terms': square[i]})
                
    def _nonzeros(self, x):
        nz = []
        for i in range(0,len(x)):
            if x[i] != 0:
                nz.append(i)
        return nz     
        
    def normalize(self):
        for i in range(len(self.docs)):
            terms = self.docs[i]['terms']
            idf = terms[i]
            for j in range(len(terms)):
                terms[j] = float(terms[j]) / idf
            self.docs[i]['terms'] = terms
        
if __name__ == '__main__':

    mx = Matrix()
    mx.add_doc(doc_id=1,
        doc_terms=['apple', 'juice', 'fruit'],
        doc_class= '0',
        frequency=True, do_padding=True) 
    mx.add_doc(doc_id=2,
        doc_terms=['orange', 'juice', 'fruit'],
        doc_class= '0',
        frequency=True, do_padding=True)
    mx.add_doc(doc_id=3,
        doc_terms=['tomato', 'juice', 'food'],
        doc_class= '0',
        frequency=True, do_padding=True)   
    
    print 'Matrix'   
    print mx.vocabulary()
    for doc in mx.docs:
        print doc['terms']  
    #print mx 
        
    mxcc = MatrixCooccurrence(mx)
    print 'MatrixCooccurrence'   
    print mxcc.vocabulary()
    for doc in mxcc.docs:
        print doc['id'], doc['terms']
    #print mxcc   
        
    print 'MatrixCooccurrence (Normalized)' 
    #mxcc.normalize()
    mxcc.tf_idf(do_idf=True)  
    print mxcc.vocabulary()
    for doc in mxcc.docs:
        print doc['id'], doc['terms']    
