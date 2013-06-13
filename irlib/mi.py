''' 
Informations Retrieval Library
==============================
MI is an implementation of Mutual Information
'''

# Author: Tarek Amr <@gr33ndata> 

import sys, math

from superlist import SuperList
from progress import Progress
from preprocessor import Preprocessor
from matrix import Matrix
from matrixexpress import MatrixExpress

class MI:

    def __init__(self, mx=None, verbose=False):
        self.mx = mx
        self.mi = [0] * len(self.mx.vocabulary())
        self.count_all = 0
        self.count_classes = {}
        self.init_count()
    
    def init_count(self):
        for doc in self.mx.docs:
            if not doc['class'] in self.count_classes:
                  self.count_classes[doc['class']] = 0
            class_total = sum(doc['terms'])      
            self.count_classes[doc['class']] += class_total
            self.count_all += class_total
            
    def pr_term(self, term_idx):
        ' Get probability of term term_idx'
        count_term = 0
        for doc in self.mx.docs:
            count_term += float(doc['terms'][term_idx])
        return count_term / self.count_all

    def pr_class(self, class_name):
        ' Get probability of class c '
        return float(self.count_classes[class_name]) / self.count_all       
    
    def pr_joint(self, term_idx, class_name):
        'Get joint probability between term t and class c'
        count_term = 0
        for doc in self.mx.docs:
            if doc['class'] == class_name:
                count_term += float(doc['terms'][term_idx])
        return count_term / self.count_all
        
    def __getitem__(self, term):
        ''' If term exists in terms, retruns its MI,
            otherwise, return -1
        '''    
        term_idx = self.mx[term]
        if term_idx == -1:
            return -1
        term_mi = 0
        for class_name in self.count_classes:
            p_joint = self.pr_joint(term_idx,class_name)
            #q_joint = 1 - p_joint
            p_term = self.pr_term(term_idx)
            #q_term = 1 - p_term
            p_class = self.pr_class(class_name)
            #q_class = 1 - p_class
            try:
                term_mi += p_joint * math.log10(p_joint/(p_term*p_class))
            except:
                pass
            #try:
                #term_mi += q_joint * math.log10(q_joint/(q_term*q_class))
            #except:
            #    pass
        return term_mi
              
if __name__ == '__main__':
        
    mx = MatrixExpress()
    mx.add_doc(doc_id='1',
               doc_terms=['apple', 'mac', 'iphone'],
               doc_class= 'apple',
               frequency=True, do_padding=True)
    mx.add_doc(doc_id='2',
               doc_terms=['windows', 'word', 'excel'],
               doc_class= 'microsoft',
               frequency=True, do_padding=True)
    mx.add_doc(doc_id='3',
               doc_terms=['computer', 'mac', 'iphone', 'ipad'],
               doc_class= 'apple',
               frequency=True, do_padding=True)
    mx.add_doc(doc_id='4',
               doc_terms=['excel', 'computer', 'computer', 'office'],
               doc_class= 'microsoft',
               frequency=True, do_padding=True)
               
    mi = MI(mx)
    for term in mx.vocabulary():
        print term, mi[term]
