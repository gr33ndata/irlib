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

class MI:

    def __init__(self, mx=None, verbose=False):
        self.mx = mx
        self.mi = [0] * len(self.mx.vocabulary())
        
    def __getitem__(self, term):
        ''' If term exists in terms, retruns its MI,
            otherwise, return -1
        '''    
        term_idx = self.mx[term]
        if term_idx == -1:
            return -1
            
