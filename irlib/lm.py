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

    
    def __init__(self, n=3, lpad='', rpad='', joiner='', 
                 verbose=False):
        '''
        Initialize our LM
        n: Pur LM's ngram, e.g. for bigram LM, n=2
        lpad, rpad: Left and right padding. 
                    If empty string '', then don't pad, else
                    For each document read pad terms
                    with n-1 repitition on lpad and/or rpad
        joiner: What to use to join ngrams, practically it doesn't matter
        '''
        self.n = n
        # Counters for joint probabilities
        # Count for w_1, w_2, w_3 ... w_{n-1}, w_n
        self.term_count_n = {}
        # Count for w_1, w_2, w_3 ... w_{n-1}
        self.term_count_n_1 = {}
        # The vocabulary of all classes (for Laplace smoothing)
        self.vocabulary = set()
        self.lpad=lpad
        self.rpad=rpad
        self.joiner = joiner
        self.verbose = verbose

    def to_ngrams(self, terms):
        ''' Converts terms to all possibe ngrams 
            terms: list of terms
        '''
        if len(terms) <= self.n:
            return terms
        if self.n == 1:
            ngrams = [[term] for term in terms]
        else:
            n_grams = []
            for i in range(0,len(terms)-self.n+1):
                n_grams.append(terms[i:i+self.n])
        return n_grams
    
    def lr_padding(self, terms):
        lpad = rpad = []
        if self.lpad:
            lpad = [self.lpad] * (self.n - 1) 
        if self.rpad:
            rpad = [self.rpad] * (self.n - 1) 
        return lpad + terms + rpad
        
    def update_counts(self, doc_id ='', ngrams=[]):
        if not doc_id in self.term_count_n:
            self.term_count_n[doc_id] = {'ngrams': {}, 'total': 0}
        if not doc_id in self.term_count_n_1:
            self.term_count_n_1[doc_id] = {'ngrams': {}, 'total': 0}
        for ngram in ngrams:
            # Generate n-grams and sub-ngrams
            # For example (n=2): ['t1','t2','t3','t4']
            # ngram_n: ['t1 t2','t2 t3', 't3 t4']
            # ngram_n_1: ['t1','t2','t3']
            ngram_n = self.joiner.join(ngram)
            ngram_n_1 = self.joiner.join(ngram[:-1])
            if ngram_n in self.term_count_n[doc_id]['ngrams']:
                self.term_count_n[doc_id]['ngrams'][ngram_n] += 1
            else:
                self.term_count_n[doc_id]['ngrams'][ngram_n] = 1
            self.term_count_n[doc_id]['total'] += 1
            if ngram_n_1 in self.term_count_n_1[doc_id]['ngrams']:
                self.term_count_n_1[doc_id]['ngrams'][ngram_n_1] += 1
            else:
                self.term_count_n_1[doc_id]['ngrams'][ngram_n_1] = 1
            self.term_count_n_1[doc_id]['total'] += 1     
        
    def add_doc(self, doc_id ='', doc_terms=[]):
        for term in doc_terms: 
            self.vocabulary.add(term)
        terms = self.lr_padding(doc_terms)
        ngrams = self.to_ngrams(terms)    
        self.update_counts(doc_id, ngrams)  
    
    def pr_ngram(self, doc_id, ngram, smooting='Laplace', log=True, logbase=2):
        add_numer = 0
        add_denom = 0
        if smooting == 'Laplace':
            add_numer = 1
            add_denom = len(self.vocabulary)
        ngram_n = self.joiner.join(ngram)
        ngram_n_1 = self.joiner.join(ngram[:-1])
        pr = float(self.term_count_n[doc_id]['ngrams'].get(ngram_n,0) + add_numer) \
             / float(self.term_count_n_1[doc_id]['ngrams'].get(ngram_n_1,0) + add_denom)
        if self.verbose:
            print ngram, pr
        if log:
            return -math.log(pr,logbase)
        else:
            return pr
    
    def pr_doc(self, doc_id, log=True, logbase=2):
        ''' This method may be overridden by implementers
        ''' 
        #print 'Old pr_doc()'
        if log:
            return 0
        else:
            return 1
                        
    def calculate(self, doc_terms=[], actual_id=''):
        calculated = {
            'prob': -1,
            'calc_id': '',
            'actual_id': actual_id
        }
        terms = self.lr_padding(doc_terms)
        ngrams = self.to_ngrams(terms)  
        for doc_id in self.term_count_n:
            #print '\n', doc_id, ':'
            doc_pr = 0
            for ngram in ngrams:
                doc_pr += self.pr_ngram(doc_id, ngram, 
                        smooting='Laplace', log=True, logbase=2)
            doc_pr += self.pr_doc(doc_id) 
            if self.verbose:            
                print doc_id, actual_id, doc_pr  
            if calculated['prob'] == -1 or doc_pr < calculated['prob']:
                calculated['prob'] = doc_pr
                calculated['calc_id'] = doc_id
        return calculated     
            
                
class LM_Old:

    ''' This is to be deleted, replaced with LM now'''

    def __init__(self, n=3, verbose=False):
        '''
        Initializes our Language Model
        ngram = n-gram (default = 3)
        term_count = {
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
        self.verbose = verbose
        self.n = n
        self.term_count = {}
        self.vocabulary = set()
    
    def get_vocabulary(self):
        return list(self.vocabulary)
        
    def logpr(self, x, base=2):
        if x == 0:
            return -math.log(0.0000001,base)
        else:
            return -math.log(x,base)
    
    def term_pr(self, doc_id, term, smooting='Laplace', log=True, logbase=2):
        add_numer = 0
        add_denom = 0
        if smooting == 'Laplace':
            add_numer = 1
            add_denom = len(self.vocabulary)
        pr = float(self.term_count[doc_id]['terms'].get(term,0) + add_numer) \
             / float(self.term_count[doc_id]['total'] + add_denom)
        if self.verbose:
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

    def calculate(self, doc_terms=[], actual_id=''):
        if self.verbose:
            print self.term_count
        calculated_id = {
            'id_prob': -1,
            'calc_id': '',
            'actual_id': actual_id
        }
        terms = self.ngrams(doc_terms)
        for doc_id in self.term_count:
            #print '\n', doc_id, ':'
            doc_pr = 0
            for term in terms:
                doc_pr += self.term_pr(doc_id, term, 
                        smooting='Laplace', log=True, logbase=2)
            if self.verbose:            
                print doc_id, actual_id, doc_pr  
            if calculated_id['id_prob'] == -1 or doc_pr < calculated_id['id_prob']:
                calculated_id['id_prob'] = doc_pr
                calculated_id['calc_id'] = doc_id
        return calculated_id            
    
if __name__ == '__main__':

    p = Preprocessor()
    
    lm = LM(n=3, verbose=True)
    
    #print lm.to_ngrams(p.term2ch('hello dear world'))
    #sys.exit()
    
    lm.add_doc(doc_id='apple', doc_terms=p.term2ch('i see glass of apple juice'))
    lm.add_doc(doc_id='apple', doc_terms=p.term2ch('the tree is full of apples'))
    #lm.add_doc(doc_id='orange', doc_terms=p.term2ch('i see the orange tree shaking'))
    lm.add_doc(doc_id='orange', doc_terms=p.term2ch('orang juice'))
    #lm.add_doc(doc_id='orange', doc_terms=p.term2ch('i do not like jaffa cake'))
    #lm.add_doc(doc_id='apple', doc_terms=p.term2ch('i have apple juice'))
    #print lm.pr
    lm.calculate(doc_terms=p.term2ch('orango juice'))
    #print lm.term_count_n
    #print lm.term_count_n_1
    #print lm.vocabulary
    
