''' 
Informations Retrieval Library
==============================
Metrics
'''

# Author: Tarek Amr <@gr33ndata> 

import math

class Metrics:

    def euclid_vectors(self, a=[], b=[]):
        ''' Calculate Euclidean distance between two vectors (lists)
        '''
        if len(a) != len(b):
            print len(a), '!=', len(b)
            raise Exception
        euclid_sqrd = 0
        for i in range(0,a.__len__()):
            euclid_sqrd += ((a[i] - b[i])*(a[i] - b[i]))
        return math.sqrt(euclid_sqrd)

    def cos_vectors(self, a=[], b=[]):
        ''' Calculates the cosine distance between two vectors (lists)
        '''
        if len(a) != len(b):
            print len(a), '!=', len(b)
            raise Exception
        norm_a_sqrd = norm_b_sqrd = 0
        numerator = 0
        for i in range(0,len(a)):
            numerator = numerator + a[i]*b[i]
            # Do not use math.pow(), time consuming!
            norm_a_sqrd = norm_a_sqrd + (a[i]*a[i]) 
            norm_b_sqrd = norm_b_sqrd + (b[i]*b[i])
        # In some cases, when one vector is all zeros, division by zero happens
        # Normally this happens when training on small training-set
        # And all vocabulary in query is first time to be seen.
        denominator = max(0.0000001, 
            (   
                math.sqrt(norm_a_sqrd) *
                math.sqrt(norm_b_sqrd)
            )
        )
        return_value = numerator / denominator
        return return_value
        
        
    def dot_product(self, a=[], b=[]):
        ''' Calculates the dot product between two vectors (lists)
        '''
        if len(a) != len(b):
            print len(a), '!=', len(b)
            raise Exception
        numerator = 0
        for i in range(0,len(a)):
            numerator = numerator + a[i]*b[i]
        if not numerator:
            return 0 
        return_value = float(numerator) 
        return return_value

if __name__ == '__main__':

    m = Metrics()
    print "Euclid:", m.euclid_vectors([1,1],[4,5])
    print "Cosine:", m.cos_vectors([1,1,1],[1,1,1])
    print "Dot Product:", m.dot_product([1,1,1],[1,1,1])

