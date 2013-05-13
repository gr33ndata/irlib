''' 
Informations Retrieval Library
==============================
Progress is a helper class to count progress 
'''

# Author: Tarek Amr <@gr33ndata> 

class Progress:

    def __init__(self, n, percent=10):
        ''' Initializes progress class
            n: number of items being progressed 
            percent: print at how many percentages
        '''
        self.count = 0
        self.n = n
        self.percent = percent
        self.step = self.n / self.percent
        
    def reset(self):
        self.count = 0
            
    def show(self):
        self.count += 1
        if not(self.count % self.step):
            print 'Current progress: %d %%' % ((self.count * self.percent) / self.step)
        
