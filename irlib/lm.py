''' 
Informations Retrieval Library
==============================
LM is an implementation of ngram Language Model 
'''

# Author: Tarek Amr <@gr33ndata> 

import sys, math

from superlist import SuperList
from progress import Progress
from preprocessor import Preprocessor


class LM:

    def __init__(self, n=3):
        '''
        Initializes our Language Model
        ngram = n-gram (default = 3)
        pr = {
            'orange': {
                'total': 3, 
                'terms': {'juice': 1, 'naranja': 1, 'jaffa': 1}
            }, 
            'apple': {
                'total': 6, 
                'terms': {'ipad': 2, 'ios': 3, 'apple': 1}
            }
        }   
        '''
        self.n = n
        self.term_count = {}
        self.vocabulary = set()
    
    def logpr(self, x, base=2):
        if x == 0:
            return -math.log(0.0000001,base)
        else:
            return -math.log(x,base)
    
    def term_pr(self, doc_id, term, smooting='Laplace', log=True, logbase=2):
        add_numer = 0
        add_demom = 0
        if smooting == 'Laplace':
            add_numer = 1
            add_demom = len(self.vocabulary)
        pr = float(self.term_count[doc_id]['terms'].get(term,0) + add_numer) \
             / float(self.term_count[doc_id]['total'] + add_demom)
        print term, pr
        if log:
            return -math.log(pr,logbase)
        else:
            return pr
                
    def ngrams(self, terms):
        ''' Converts terms to all possibe ngrams 
            terms: list of terms
        '''
        if self.n == 1:
            return terms
        n_grams = []
        for i in range(0,len(terms)-self.n+1):
            n_grams.append(" ".join(terms[i:i+self.n]))
        return n_grams
		    
    def add_doc(self, doc_id = '', doc_terms=[]):
        if not doc_id in self.term_count:
            self.term_count[doc_id] = {'terms': {}, 'total': 0}
        terms = self.ngrams(doc_terms)
        for term in terms:
            if term in self.term_count[doc_id]['terms']:
                self.term_count[doc_id]['terms'][term] += 1
            else:
                self.term_count[doc_id]['terms'][term] = 1
            self.term_count[doc_id]['total'] += 1
            self.vocabulary.add(term)

    def calculate(self, doc_terms=[]):
        print self.term_count
        terms = self.ngrams(doc_terms)
        for doc_id in self.term_count:
            print '\n', doc_id, ':'
            doc_pr = 0
            for term in terms:
                doc_pr += self.term_pr(doc_id, term, 
                        smooting='Laplace', log=True, logbase=2)
            print doc_id, doc_pr            
    
if __name__ == '__main__':

    p = Preprocessor()
    
    lm = LM(n=9)
    lm.add_doc(doc_id='apple', doc_terms=p.term2ch('i see glass of apple juice'))
    lm.add_doc(doc_id='apple', doc_terms=p.term2ch('the tree is full of apples'))
    #lm.add_doc(doc_id='orange', doc_terms=p.term2ch('i see the orange tree shaking'))
    lm.add_doc(doc_id='orange', doc_terms=p.term2ch('orang juice'))
    #lm.add_doc(doc_id='orange', doc_terms=p.term2ch('i do not like jaffa cake'))
    #lm.add_doc(doc_id='apple', doc_terms=p.term2ch('i have apple juice'))
    #print lm.pr
    lm.calculate(doc_terms=p.term2ch('orange juice'))
    
    
