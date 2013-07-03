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

class UnseenTerms:

    def __init__(self):
        self.counts = {}
        
    def update(self, doc_id='', unseen=True):
        if not doc_id in self.counts:
            self.counts[doc_id] = {
                'seen': 0,
                'unseen': 0
            }       
        if unseen:
            self.counts[doc_id]['unseen'] += 1
        else:
            self.counts[doc_id]['seen'] += 1

    def display(self):
        #print '***!', self.counts
        for doc_id in self.counts:
            unseen = self.counts[doc_id]['unseen'] 
            total = self.counts[doc_id]['unseen'] + self.counts[doc_id]['seen']
            unseen_ratio =  unseen * 1.0 / total
            print 'Document:', doc_id
            print 'Unseen ratio:', unseen_ratio 
    
    
class LM:

    
    def __init__(self, n=3, lpad='', rpad='', 
                 smoothing='Laplace', laplace_gama=1,
                 corpus_mix=0, 
                 verbose=False):
        '''
        Initialize our LM
        n: Pur LM's ngram, e.g. for bigram LM, n=2
        lpad, rpad: Left and right padding. 
                    If empty string '', then don't pad, else
                    For each document read pad terms
                    with n-1 repitition on lpad and/or rpad
        smoothing: 'Laplace' or 'Witten'
        laplace_gama: Multiply 1 and V by this factor gamma
        corpus_mix: 0 (default) only use document probabilites
                  : otherwise use this value as 0 < lambda <= 1 
        '''
        self.n = n
        # Counters for joint probabilities
        # Count for w_1, w_2, w_3 ... w_{n-1}, w_n
        self.term_count_n = {}
        # Count for w_1, w_2, w_3 ... w_{n-1}
        self.term_count_n_1 = {}
        # To be used in case of mixing doc prob with corpus prob.
        self.corpus_count_n = {'ngrams': {}, 'total': 0} 
        self.corpus_count_n_1 = {'ngrams': {}, 'total': 0}
        # The vocabulary of all classes (for Laplace smoothing)
        self.vocabulary = set()
        self.lpad=lpad
        self.rpad=rpad
        self.smoothing = smoothing
        self.laplace_gama = float(laplace_gama)
        self.corpus_mix = min(float(corpus_mix),1)
        self.joiner = ' '
        self.unseen_counts = UnseenTerms()
        self.verbose = verbose

    def display(self):
        '''
        Displays statistics about our LM
        '''
        for doc_id in self.term_count_n:
            ngrams = len(self.term_count_n[doc_id]['ngrams'])
            print 'n-Grams (doc %s): %d' % (str(doc_id), ngrams)
            ngrams1 = len(self.term_count_n_1[doc_id]['ngrams'])
            print '(n-1)-Grams (doc %s): %d' % (str(doc_id), ngrams1)
        self.unseen_counts.display()
    
    def to_ngrams(self, terms):
        ''' Converts terms to all possibe ngrams 
            terms: list of terms
        '''
        if len(terms) <= self.n:
            return terms
        if self.n == 1:
            n_grams = [[term] for term in terms]
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
            # Update n-gram counts for doc_id
            if ngram_n in self.term_count_n[doc_id]['ngrams']:
                self.term_count_n[doc_id]['ngrams'][ngram_n] += 1
            else:
                self.term_count_n[doc_id]['ngrams'][ngram_n] = 1
            self.term_count_n[doc_id]['total'] += 1
            # Update n-gram counts for corpus
            if ngram_n in self.corpus_count_n['ngrams']:
                self.corpus_count_n['ngrams'][ngram_n] += 1
            else:
                self.corpus_count_n['ngrams'][ngram_n] = 1
            self.corpus_count_n['total'] += 1
            # Update (n-1)-gram counts for doc_id    
            if ngram_n_1 in self.term_count_n_1[doc_id]['ngrams']:
                self.term_count_n_1[doc_id]['ngrams'][ngram_n_1] += 1
            else:
                self.term_count_n_1[doc_id]['ngrams'][ngram_n_1] = 1
            self.term_count_n_1[doc_id]['total'] += 1 
            # Update (n-1)-gram counts for corpus
            if ngram_n_1 in self.corpus_count_n_1['ngrams']:
                self.corpus_count_n_1['ngrams'][ngram_n_1] += 1
            else:
                self.corpus_count_n_1['ngrams'][ngram_n_1] = 1
            self.corpus_count_n_1['total'] += 1 
   
        
    def add_doc(self, doc_id ='', doc_terms=[]):
        for term in doc_terms: 
            self.vocabulary.add(term)
        terms = self.lr_padding(doc_terms)
        ngrams = self.to_ngrams(terms)    
        self.update_counts(doc_id, ngrams)  
    
    def laplace(self, x, y, doc_id):
        add_numer = 1 * self.laplace_gama
        laplace_mode = 'n-1'
        if laplace_mode == 'ch':
            v = len(self.vocabulary)
        elif laplace_mode == 'ch^n-1':
            v = math.pow(len(self.vocabulary),self.n-1)
        else:
            if doc_id:
                v = len(self.term_count_n_1[doc_id]['ngrams'])
            else:
                v = len(self.corpus_count_n_1['ngrams'])
        add_denom = v * self.laplace_gama
        return float(x + add_numer) / float(y + add_denom)
    
    def witten(self, count, n, t, log, new_doc):
        self.return_unseen = True if new_doc else False
        #print 'Witten (New Doc? %s)' %  new_doc 
        #print 'W:', count, n, t
        if count:
            return float(count) / (n+t)
        elif self.return_unseen:
            return float(t) / (n+t)
        elif log:
            return 1
        else:
            return 1   
        
    def pr_ngram(self, doc_id, ngram, new_doc=False, log=True, logbase=2):
        ngram_n = self.joiner.join(ngram)
        ngram_n_1 = self.joiner.join(ngram[:-1])
        ngram_n_count = self.term_count_n[doc_id]['ngrams'].get(ngram_n,0)
        ngram_n_1_count = self.term_count_n_1[doc_id]['ngrams'].get(ngram_n_1,0)
        corpus_ngram_n_count = self.corpus_count_n['ngrams'].get(ngram_n,0)
        corpus_ngram_n_1_count = self.corpus_count_n_1['ngrams'].get(ngram_n_1,0)
        # Apply smoothing
        if self.smoothing == 'Laplace':
            pr = self.laplace(ngram_n_count, ngram_n_1_count, doc_id)
            if self.corpus_mix:
                pr_corpus = self.laplace(corpus_ngram_n_count, 
                                         corpus_ngram_n_1_count, 
                                         doc_id='')
        elif self.smoothing == 'Witten':
            #print ngram_n, '-', ngram_n_1
            #wittenn = self.term_count_n[doc_id]['total']
            wittenn = ngram_n_1_count
            #wittent = len(self.term_count_n_1[doc_id]['ngrams']) 
            wittent = len([key for key in self.term_count_n[doc_id]['ngrams'] if key.startswith(ngram_n_1)])
            pr = self.witten(ngram_n_count, wittenn, wittent, log, new_doc)
        else:
            pr = float(ngram_n_count) / float(ngram_n_1_count)
            if self.corpus_mix:
                pr_corpus = float(corpus_ngram_n_count) / float(corpus_ngram_n_1_count)
        # Update seen/unseen counts
        if ngram_n_count:    
            self.unseen_counts.update(doc_id=doc_id, unseen=False)
        else:
            self.unseen_counts.update(doc_id=doc_id, unseen=True)
        # Shall we mix probability with corpus or not?
        if self.corpus_mix:
            pr_mix = self.corpus_mix * pr_corpus + (1 - self.corpus_mix) * pr
        else:
            pr_mix = pr
        if self.verbose:
            print 'Pr(%s) = %s' % (ngram, pr_mix)
        if log:
            return -math.log(pr_mix,logbase)
        else:
            return pr_mix
    
    def pr_doc(self, doc_id, log=True, logbase=2):
        ''' This method may be overridden by implementers
            Here we assume uniform Pr(doc) within Bayes rule
            i.e. Pr(doc/string) = Pr(string/doc)
            rather than Pr(doc/string) = Pr(string/doc) * Pr(doc)
        ''' 
        if log:
            return 0
        else:
            return 1
                        
    def calculate(self, doc_terms=[], actual_id=''):
        '''
        Given a set of terms, doc_terms
        We find the doc in training data (calc_id),
        whose LM is more likely to produce those terms
        Then return the data structure calculated back
        calculated{
            prob: calculated probability Pr(calc_id/doc_terms)
            calc_id: Document ID in training data.
            actual_id: Just returned back as passed to us.
        }  
        ''' 
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
            new_doc = True
            for ngram in ngrams:
                doc_pr += self.pr_ngram(doc_id, ngram, 
                        new_doc=new_doc, log=True, logbase=2)
                new_doc = False
            doc_pr += self.pr_doc(doc_id) 
            if self.verbose:            
                print doc_id, actual_id, doc_pr  
            if calculated['prob'] == -1 or doc_pr < calculated['prob']:
                calculated['prob'] = doc_pr
                calculated['calc_id'] = doc_id
        return calculated     
            
                

if __name__ == '__main__':

    p = Preprocessor()
    
    lm = LM(n=2, verbose=True, smoothing='Laplace', corpus_mix=0)
    
    #print lm.to_ngrams(p.term2ch('hello dear world'))
    #sys.exit()
    
    #lm.add_doc(doc_id='apple', doc_terms=p.term2ch('i see glass of apple juice'))
    lm.add_doc(doc_id='apple', doc_terms=p.term2ch('the tree is full or apples'))
    #lm.add_doc(doc_id='orange', doc_terms=p.term2ch('i see the orange tree shaking'))
    lm.add_doc(doc_id='orange', doc_terms=p.term2ch('orange orange juice'))
    #lm.add_doc(doc_id='orange', doc_terms=p.term2ch('i do not like jaffa cake'))
    #lm.add_doc(doc_id='apple', doc_terms=p.term2ch('i have apple juice'))
    #print lm.pr
    result = lm.calculate(doc_terms=p.term2ch('orango juice'))
    print result
    #print lm.term_count_n
    #print lm.term_count_n_1
    #print lm.vocabulary
    
