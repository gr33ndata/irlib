''' 
Informations Retrieval Library
==============================
Progress is a helper class to count progress 
'''

# Author: Tarek Amr <@gr33ndata> 

class Progress:

    def __init__(self, n, percent=10):
        ''' Initializes progress class
            n: number of items to be progressed 
            percent: print at which percentage steps
        '''
        self.count = 0
        self.n = n
        self.percent = percent
        self.step = self.n / self.percent
        
    def reset(self):
        ''' Resets counter
        '''
        self.count = 0
            
    def show(self, message='Current progress:'):
        ''' Call show whenever an item is processed,
            it will only display progress at percentages steps
        '''
        # Don't show anything if very small step
        if self.step < 1:
            return
        self.count += 1
        if self.count % self.step:
            return 0
        else:
            print '%s %#3d %%' % (message, (self.count * self.percent) / self.step)
            return 1
            
