''' 
Informations Retrieval Library
==============================
Matrix is an index for documents, terms, and their classes. 
'''

# Author: Tarek Amr <@gr33ndata> 

import sys, math
from superlist import SuperList

def log_tf(value):
    ''' The log(tf) 
        returns: 1 + log_10(value) if value != 0 
               : 0 if value == 0
    '''
    val = float(value)
    val = 1 + math.log10(val) if val != 0 else float(0)
    return val

class Matrix:

    def __init__(self):
        # List of unique terms (vocabulary)
        self.terms = SuperList()
        # List of document classes and terms summary
        self.classes = {}
        self.docs = []

    def __len__(self):
        'Returns number of loaded ducuments'
        return len(self.docs)

    def vocabulary(self):
        'Returns list of unique terms'
        return self.terms
            
    def __str__(self):
        s  = 'Matrix:'
        s += '\n * Vocabulary read: %d' % len(self.terms)
        s += '\n * Documents read: %d' % len(self.docs)
        return s

    def __contains__(self, term):
        'Checks if certain terms is loaded'
        return self.terms.__contains__(term)        

    def to_be_deleted__getitem__(self, term):
        'Returns occurences of term in all documents'
        if not term in self:
            return SuperList()
        col = [doc['terms'][self.terms.index(term)] for doc in self.docs]
        return SuperList(col)
        
    def __getitem__(self, term):
        ''' If term exists in terms, retruns it position in list,
            otherwise, return -1
        '''    
        if not term in self:
            return -1
        else:
            return self.terms.index(term)
    
    def do_padding(self):
        ''' Align the length of all rows in matrix
            Each time we see a new term, list of terms is expanded,
            and the matrix row for such document is of same length too.
            But what about rows added earlier for previous documents?
            So, this method alighn all previously added rows, 
            to match the current length of the terms list.
        '''
        if len(self.docs[-1]) == len(self.docs[0]):
            return
        for doc in self.docs:
            doc['terms'].expand(new_len=len(self.terms))
        #for cls in self.classes:
        #    self.classes[cls].expand(new_len=len(self.terms))

    def tf_idf(self, do_idf=True):
        ''' Converts matrix to tf.idf values
            do_idf: if False, convert to tf only
        '''
        N = len(self)
        for doc in self.docs:
            for idx in range(len(doc)):
                df = self[self.terms[idx]].nonzero_count()
                tf = log_tf(doc['terms'][idx])
                idf = float(N) / df if do_idf else 1 
                doc['terms'][idx] = tf * idf
 
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
        # Update list of terms if new term seen.
        # And document (row) with its associated data.
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
        # Update list of document classes if new class seen.
        #self.classes.unique_append(doc_class)
        if self.classes.has_key(doc_class):
            self.classes[doc_class].add(my_doc_terms)
        else:
            self.classes[doc_class] = my_doc_terms
        if do_padding: 
            self.do_padding()
        

    def query_to_vector(self, q_terms, frequency=False,):
        ''' Converts query to a list alligned with our self.terms.
            Terms not seen before will be ignored.
            q_terms: list of query terms
            frequency: return a multinomial or multivariate list?
        '''
        my_query_vector = SuperList()
        my_query_vector.expand(new_len=len(self.terms))
        for term in q_terms:
            try:
                term_idx = self.terms.index(term)
            except:
                # Term not seen before, skip
                continue
            #print term, self.terms.index(term)
            if frequency:
                my_query_vector.increment_after_padding(term_idx,1)
            else:
                my_query_vector.insert_after_padding(term_idx,1)
        return my_query_vector
        
    def get_stats(self):
        return Stats(self)

'''
classes = {
    'class1': {'terms': [1,2,0,3], 'totel': 6}
}
terms = []
'''    
class Stats:

    def __init__(self, matrix):
        self.mx = matrix
        self.N  = 0
        self.classes = {}
        self.terms = SuperList()       
        for c in self.mx.classes:
            self.classes[c] = {}
            self.classes[c]['terms'] = self.mx.classes[c]
            self.classes[c]['total'] = sum(self.classes[c]['terms'])
            self.terms.add(self.classes[c]['terms'])
            self.N += self.classes[c]['total']
        self.mi_terms = []
        
    def __str__(self):
        s  = 'Matrix Stats:'
        s += '\n * Vocabulary/Terms: %d/%d' % (len(self.terms), self.N)
        return s
        
    def getN(self):
        ''' Get total number of terms, counting their frequencies too.
            Notice: This is not the same as len(vocabulary)
        '''
        return self.N
        
    def get_terms_freq(self, normalized=False):
        ''' Returns 2d matrix of vocabulary terms and their occurences
            if normalized is True, devide by total number of terms
        '''
        terms = self.mx.terms
        freq = self.terms.div(self.N) if normalized else self.terms
        return [terms, freq] 
            
    def pr_term(self, t):
        ' Get probability of term t '
        i = self.mx[t]
        if i == -1:
            return 0
        return float(self.terms[i]) / self.N

    def pr_class(self, c):
        ' Get probability of class c '
        return float(self.classes[c]['total']) / self.N
        
    def pr_joint(self, t, c):
        'Get joint probability between term t and class c'
        i = self.mx[t]
        if i == -1:
            return 0
        return float(self.classes[c]['terms'][i]) / self.N
        
    def mi(self):
        for t in self.mx.vocabulary():
            mi = 0
            for c in self.classes:
                try:
                    mi += self.pr_joint(t,c) * math.log10( self.pr_joint(t,c) / ( self.pr_term(t) * self.pr_class(c) ))
                except:
                    # Oh, log(0), let's set mi = 0
                    mi = 0
            self.mi_terms.append(mi) 
        print self.classes    
        print self.mi_terms
        
if __name__ == '__main__':

    pass
