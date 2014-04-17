''' 
Informations Retrieval Library
==============================
LM is an implementation of ngram Language Model 
'''

# Author: Tarek Amr <@gr33ndata> 

import sys, math

class UnseenTerms:

    def __init__(self):
        # Count unseen n-grams per each class
        self.doc_counts = {}
        # Count unseen n-grams per correct/incorrect results
        self.cic_counts = {}
    
    def _seen_unseel_label(self, seen, unseen):
        if seen + unseen:
            label = '%0.2f' % (float(unseen) / (seen+unseen))
        else:
            label = '%0.2f' %  0
        #label = str(unseen)
        return label
        
    def per_cic(self, calculated_id='', actual_id='', seen_unseen=None):
        calculated_id = str(calculated_id).strip()
        actual_id =str(actual_id).strip()
        unseen_ratio_str = self._seen_unseel_label(*seen_unseen)
        if not unseen_ratio_str in self.cic_counts:
            self.cic_counts[unseen_ratio_str] = [0,0]
        if calculated_id == actual_id:
            self.cic_counts[unseen_ratio_str][0] += 1
        else:
            self.cic_counts[unseen_ratio_str][1] += 1
         
         
    def per_doc(self, doc_id='', seen_unseen=None):
        if not doc_id in self.doc_counts:
            self.doc_counts[doc_id] = {
                'seen': 0,
                'unseen': 0
            }  
        self.doc_counts[doc_id]['seen'] += seen_unseen[0]    
        self.doc_counts[doc_id]['unseen'] += seen_unseen[1]  
        #if unseen:
        #    self.cls_counts[doc_id]['unseen'] += 1
        #else:
        #    self.cls_counts[doc_id]['seen'] += 1

    
    def display(self, per_doc=True, per_cic=True):
        #print '***!', self.counts
        if per_doc:
            print '\nUnseen n-grams as per actual doc_ids'
            doc_ids = self.doc_counts.keys()
            doc_ids.sort()
            for doc_id in doc_ids:
                unseen = self.doc_counts[doc_id]['unseen'] 
                total = self.doc_counts[doc_id]['unseen'] + self.doc_counts[doc_id]['seen']
                unseen_ratio =  float(unseen) / total
                print 'Ratio of unseen (%s): %0.4f' % (doc_id, unseen_ratio) 
        if per_cic:
            print ''
            print 'Correct/Incorrect Unseen Ratios'
            cic_x = []
            correct = []
            incorrect = []
            cic_labels = self.cic_counts.keys()
            cic_labels.sort()
            for label in cic_labels:
                cic_x.append(str(label))
                correct.append(str(self.cic_counts[label][0]))
                incorrect.append(str(self.cic_counts[label][1]))
            print 'CIC X = [' + ','.join(cic_x) + ']'
            print 'Correct   = [' + ','.join(correct) + ']'
            print 'Incorrect = [' + ','.join(incorrect) + ']'
    
class LM:

    
    def __init__(self, n=3, lpad='', rpad='', 
                 smoothing='Laplace', laplace_gama=1,
                 corpus_mix=0, corpus_mode='Miller',
                 verbose=False):
        '''
        Initialize our LM
        n: Order of ngram LM, e.g. for bigram LM, n=2
        lpad, rpad: Left and right padding. 
                    If empty string '', then don't pad, else
                    For each document read pad terms
                    with n-1 repitition on lpad and/or rpad
        smoothing: 'Laplace' or 'Witten'
        laplace_gama: Multiply 1 and V by this factor gamma
        corpus_mix: 0 (default) only use document probabilites
                  : or value between 0 and 1 lambda
                  : or c (or l) for Log-likelihood Odds model (Cooper LDA)
        corpus_mode: 'Hiemstra' or 'Miller'
                   : This tell us how to calculate pr_corpus(t)
                   : In fact, 'Hiemstra' makes sense only with Multivaria LM
                   : Whereas the LM here is Multinomial. 
        '''
        self.n = n
        #(self.n, self.m) = n if type(n) == tuple else (n,0)
        # Counters for joint probabilities
        # Count for w_1, w_2, w_3 ... w_{n-1}, w_n
        self.term_count_n = {}
        # Count for w_1, w_2, w_3 ... w_{n-1}
        self.term_count_n_1 = {}
        # To be used in case of mixing doc prob with corpus prob.
        self.corpus_count_n = {'ngrams': {}, 'total': 0} 
        self.corpus_count_n_1 = {'ngrams': {}, 'total': 0}
        self.doc_lengths = {}
        # The vocabulary of all classes (for Laplace smoothing)
        self.vocabulary = set()
        self.lpad=lpad
        self.rpad=rpad
        self.smoothing = smoothing
        self.laplace_gama = float(laplace_gama)
        if not type(corpus_mix) is str:
            self.corpus_mix = min(float(corpus_mix),1)
        else:
            self.corpus_mix = corpus_mix
        self.corpus_mode = corpus_mode
        self.joiner = ''
        self.unseen_counts = UnseenTerms()
        self.verbose = verbose

    def display(self, per_doc=True, per_cic=True):
        '''
        Displays statistics about our LM
        '''
        voc_list = []
        doc_ids = self.term_count_n.keys()
        doc_ids.sort()
        for doc_id in doc_ids:
            ngrams = len(self.term_count_n[doc_id]['ngrams'])
            print 'n-Grams (doc %s): %d' % (str(doc_id), ngrams)
            ngrams1 = len(self.term_count_n_1[doc_id]['ngrams'])
            print '(n-1)-Grams (doc %s): %d' % (str(doc_id), ngrams1)
            voc_list.append(ngrams)
        print 'Classed Vocabularies:', voc_list
        print ''
        corpus_ngrams = len(self.corpus_count_n['ngrams']) 
        print 'n-Grams (collection): %d' % (corpus_ngrams)
        corpus_ngrams1 = len(self.corpus_count_n_1['ngrams']) 
        print '(n-1)-Grams (collection): %d' % (corpus_ngrams1)
        self.unseen_counts.display(per_doc, per_cic)
        # Display overlapping n-grams between classes
        #self.overlaps()
    
    def get_ngram_counts(self):
        ''' Returns a list of n-gram counts
            Array of classes counts and last item is for corpus
        '''
        ngram_counts = {
            'classes': [],
            'classes-1': [],
            'corpus': 0,
            'corpus-1': 0
        }
        doc_ids = self.term_count_n.keys()
        doc_ids.sort()
        for doc_id in doc_ids:
            #print self.term_count_n[doc_id]
            class_ngrams = len(self.term_count_n[doc_id]['ngrams'])
            class_n1grams = len(self.term_count_n_1[doc_id]['ngrams'])
            ngram_counts['classes'].append(class_ngrams)
            ngram_counts['classes-1'].append(class_n1grams)
        corpus_ngrams = len(self.corpus_count_n['ngrams'])
        corpus_n1grams = len(self.corpus_count_n_1['ngrams'])
        ngram_counts['corpus'] = corpus_ngrams
        ngram_counts['corpus-1'] = corpus_n1grams
        return ngram_counts   
            
    def overlaps(self):
        omx = []
        doc_ids = self.term_count_n.keys()
        doc_ids.sort()
        for doc_id in doc_ids:
            row = [0] * len(doc_ids)
            omx.append(row)
        for i in range(len(doc_ids)):
            doc_id_i = doc_ids[i]
            ngrams = len(self.term_count_n[doc_id_i]['ngrams'])
            omx[i][i] = ngrams
            for j in range(i):
                doc_id_j = doc_ids[j]
                ongrams = 0
                #for ngram in self.term_count_n[doc_id_j]['ngrams']:
                for ngram in self.term_count_n[doc_id_i]['ngrams']:
                    #if ngram in self.term_count_n[doc_id_i]['ngrams']:
                    if ngram in self.term_count_n[doc_id_j]['ngrams']:
                        ongrams += 1
                    omx[i][j] = 0 #ongrams
                    omx[j][i] = ongrams
        print '\nn-gram overlaps:'
        print doc_ids            
        for i in range(len(omx)):
            row = []
            for j in range(len(omx[i])):
                row.append( round( float(omx[i][j] * 100) / omx[i][i],2 ) )
                #row.append(omx[i][j])
            print row
    
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
        '''
        Pad doc from the left and right before adding,
        depending on what's in self.lpad and self.rpad
        If any of them is '', then don't pad there. 
        '''
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
   
    def update_lengths(self, doc_id ='', doc_length=0):
        if not doc_id in self.doc_lengths:
            self.doc_lengths[doc_id] = {'lengths': [], 'mean': -1}
        self.doc_lengths[doc_id]['lengths'].append(int(doc_length))
        
    def get_mean_lengths(self, doc_id =''):
        my_mean_len = 0
        others_mean_len = []
        for d_id in self.doc_lengths:  
            if self.doc_lengths[d_id]['mean'] == -1:
                dlen = self.doc_lengths[d_id]['lengths']
                doc_mean_len = float(sum(dlen)) / len(dlen)
                self.doc_lengths[d_id]['mean'] = doc_mean_len
            else:
                doc_mean_len = self.doc_lengths[d_id]['mean']
            if d_id == doc_id:
                my_mean_len = doc_mean_len
            else:
                others_mean_len.append(doc_mean_len)      
        oth_mean_len = float(sum(others_mean_len)) / len(others_mean_len)
        return (my_mean_len, oth_mean_len)
                
    def add_doc(self, doc_id ='', doc_terms=[], doc_length=-1):
        '''
        Add new document to our Language Model (training phase)
        doc_id is used here, so we build seperate LF for each doc_id
        I.e. if you call it more than once with same doc_id,
        then all terms given via doc_terms will contribute to same LM
        doc_terms: list of words in document to be added 
        doc_length: the length of the document, you can provide it yourself,
                    otherwise, we use len(doc_terms) instead.
        '''
        if doc_length == -1:
            self.update_lengths(doc_id=doc_id, doc_length=len(doc_terms))
        else:
            self.update_lengths(doc_id=doc_id, doc_length=int(doc_length)) 
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
        
    def pr_ngram(self, doc_id, ngram, new_doc=False, log=True, logbase=2, doc_length=-1):
        ngram_n = self.joiner.join(ngram)
        ngram_n_1 = self.joiner.join(ngram[:-1])
        ngram_n_count = self.term_count_n[doc_id]['ngrams'].get(ngram_n,0)
        ngram_n_1_count = self.term_count_n_1[doc_id]['ngrams'].get(ngram_n_1,0)
        # Apply smoothing
        if self.smoothing == 'Laplace':
            pr = self.laplace(ngram_n_count, ngram_n_1_count, doc_id)
            if self.corpus_mix == 'c' or self.corpus_mix == 'l':
                corpus_ngram_n_count = self.corpus_count_n['ngrams'].get(ngram_n,0)
                corpus_ngram_n_1_count = self.corpus_count_n_1['ngrams'].get(ngram_n_1,0)
                pr_dash = self.laplace(corpus_ngram_n_count - ngram_n_count,
                                  corpus_ngram_n_1_count - ngram_n_1_count,
                                  doc_id='')
                pr_mix = float(pr) / float(pr_dash)   
            elif type(float(self.corpus_mix)) is float and self.corpus_mix > 0:  
                pr_corpus = self.pr_corpus(ngram_n, ngram_n_1)
                pr_mix = self.corpus_mix * pr_corpus + (1 - self.corpus_mix) * pr
            else:
                pr_mix = pr
        elif self.smoothing == 'Witten':
            wittenn = ngram_n_1_count
            wittent = len([key for key in self.term_count_n[doc_id]['ngrams'] if key.startswith(ngram_n_1)])
            pr = self.witten(ngram_n_count, wittenn, wittent, log, new_doc)
            pr_mix = pr
        else:
            pr = float(ngram_n_count) / float(ngram_n_1_count)
            if type(float(self.corpus_mix)) is float and self.corpus_mix > 0:  
                pr_corpus = self.pr_corpus(ngram_n, ngram_n_1)
                pr_mix = self.corpus_mix * pr_corpus + (1 - self.corpus_mix) * pr
            else:
                pr_mix = pr
                
        # Update seen/unseen counts
        if ngram_n_count:
            seen = True    
        else:
            seen = False
        if log:
            return (-math.log(pr_mix,logbase),seen)
        else:
            return (pr_mix,seen)
    
    def pr_corpus(self, ngram_n, ngram_n_1):
        if self.corpus_mode == 'Hiemstra':
            df = 0
            df_total = 0
            for doc_id in self.term_count_n_1:
                if self.term_count_n[doc_id]['ngrams'].get(ngram_n,0):
                    df += 1
                df_total += 1
            pr = float(df) / float(df_total)
            if not pr:
                pr += 0.0001
        else:
            corpus_ngram_n_count = self.corpus_count_n['ngrams'].get(ngram_n,0)
            corpus_ngram_n_1_count = self.corpus_count_n_1['ngrams'].get(ngram_n_1,0)
            pr = self.laplace(corpus_ngram_n_count, 
                              corpus_ngram_n_1_count, 
                              doc_id='')
        return pr
            
    def pr_doc(self, doc_id, log=True, logbase=2, doc_length=-1):
        ''' This method may be overridden by implementers
            Here we assume uniform Pr(doc) within Bayes rule
            i.e. Pr(doc/string) = Pr(string/doc)
            rather than Pr(doc/string) = Pr(string/doc) * Pr(doc)
        ''' 
        if log:
            return 0
        else:
            return 1
                        
    def calculate(self, doc_terms=[], actual_id='', doc_length=-1):
        '''
        Given a set of terms, doc_terms
        We find the doc in training data (calc_id),
        whose LM is more likely to produce those terms
        Then return the data structure calculated back
        doc_length is passed to pr_ngram() and pr_doc()
            it is up to them to use it or not.
            normally, it should be ignored if doc_length == -1
        calculated{
            prob: calculated probability Pr(calc_id/doc_terms)
            calc_id: Document ID in training data.
            actual_id: Just returned back as passed to us.
            seen_unseen_count: Counts for terms seen/unseen in training data
        }  
        ''' 
        calculated = {
            'prob': -1,
            'calc_id': '',
            'actual_id': actual_id,
            'seen_unseen_count': (0,0)
        }
        terms = self.lr_padding(doc_terms)
        ngrams = self.to_ngrams(terms) 
        for doc_id in self.term_count_n:
            #print '\n', doc_id, ':'
            doc_pr = 0
            new_doc = True
            seen_count = 0
            unseen_count = 0
            for ngram in ngrams:
                (ngram_pr, ngram_seen) = self.pr_ngram(doc_id, ngram, 
                        new_doc=new_doc, log=True, logbase=2, doc_length=doc_length)
                doc_pr += ngram_pr
                new_doc = False
                if ngram_seen:
                    seen_count += 1
                else:
                    unseen_count += 1
            doc_pr += self.pr_doc(doc_id, doc_length=doc_length) 
            if self.verbose:            
                print doc_id, actual_id, doc_pr  
            if calculated['prob'] == -1 or doc_pr < calculated['prob']:
                calculated['prob'] = doc_pr
                calculated['calc_id'] = doc_id
                calculated['seen_unseen_count'] = (seen_count, unseen_count)
        self.unseen_counts.per_doc(doc_id=calculated['actual_id'], 
            seen_unseen=calculated['seen_unseen_count'])
        self.unseen_counts.per_cic(calculated_id=calculated['calc_id'], 
            actual_id=calculated['actual_id'],
            seen_unseen=calculated['seen_unseen_count'])
        return calculated     
            
                

if __name__ == '__main__':

    #Preprocessor
    def term2ch(text):
        return [ch for ch in text]

    lm = LM(n=2, verbose=True, smoothing='Laplace', corpus_mix=0)
    
    #print lm.to_ngrams(term2ch('hello dear world'))
    #sys.exit()
    
    #lm.add_doc(doc_id='apple', doc_terms=term2ch('i see glass of apple juice'))
    lm.add_doc(doc_id='apple', doc_terms=term2ch('the tree is full or apples'))
    #lm.add_doc(doc_id='orange', doc_terms=term2ch('i see the orange tree shaking'))
    lm.add_doc(doc_id='orange', doc_terms=term2ch('orange orange juice'))
    #lm.add_doc(doc_id='orange', doc_terms=term2ch('i do not like jaffa cake'))
    #lm.add_doc(doc_id='apple', doc_terms=term2ch('i have apple juice'))
    #print lm.pr
    result = lm.calculate(doc_terms=term2ch('orango juice'))
    print result
    
    print lm.term_count_n
    print lm.term_count_n_1
    print lm.vocabulary
 
 

    
