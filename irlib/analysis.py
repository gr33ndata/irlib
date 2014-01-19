#!/usr/bin/env python

''' 
Informations Retrieval Library
===============================
Analysis has some text analysis tools
'''

# Author: Tarek Amr <@gr33ndata> 


class Freq:

    def __init__(self):
        self.freq_dict = {}
        self.freq_list = []
        
    def _to_array(self):
        ''' Converts self.freq_dict to self.freq_list 
        '''
        for tok in self.freq_dict:
            self.freq_list.append({'tok': tok, 'freq': self.freq_dict[tok]})
    
    def _freq_cmp(self, a, b):
        ''' Helper functions used in sorting self.freq_list      
        '''
        if a['freq'] > b['freq']:
            return  1
        else:
            return -1
               
    def add(self, tokenz):
        ''' Add more tokenized text to self.freq_dict 
        '''
        for token in tokenz:
            self.freq_dict[token] = self.freq_dict.get(token,0) + 1
            
    def display(self):
        for key in self.freqz:
            print key, self.freqz[key]
        
    def topn(self, n=1):
        ''' Returns top n tokens by their frequencies
            Defaul value for n is 1, i.e. most frequent token
        '''
        self._to_array()
        self.freq_list.sort(self._freq_cmp, reverse=True)
        return self.freq_list
    
    def print_topn(self, n=1):
        for item in self.topn(n):    
            print item['tok'], item['freq']

if __name__ == '__main__':

    f = Freq()
    f.add(['apple', 'juice'])
    f.add(['apple', 'pie'])
    f.add(['orange', 'juice'])
    f.add(['banana', 'split'])
    #f.display()
    f.print_topn(10)