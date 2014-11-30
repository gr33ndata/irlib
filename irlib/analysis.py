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
    
    def add(self, tokenz):
        ''' Add more tokenized text to self.freq_dict 
        '''
        for token in tokenz:
            self.freq_dict[token] = self.freq_dict.get(token,0) + 1

    def __getitem__(self, term):
        return self.freq_dict.get(term, -1)

    def __len__(self):
        return len(self.freq_dict)

    def __str__(self):
        return 'Class Instance of Freq ({n} terms)'.format(n=len(self))

    def to_array(self):
        ''' Converts self.freq_dict to self.freq_list 
        '''
        #for tok in self.freq_dict:
        #    self.freq_list.append({'token': tok, 'freq': self.freq_dict[tok]})
        return [{'token': tok, 'freq': self.freq_dict[tok]} for tok in self.freq_dict]
    
    def freq_cmp(self, a, b):
        ''' Helper functions used in sorting self.freq_list      
        '''
        if a['freq'] > b['freq']:
            return  1
        else:
            return -1
            
    def display(self):
        for key in self.freqz:
            print key, self.freqz[key]
        
    def topn(self, n=1):
        ''' Returns top n tokens by their frequencies
            Defaul value for n is 1, i.e. most frequent token
        '''
        topn_list = self.to_array()
        topn_list.sort(self.freq_cmp, reverse=True)
        return topn_list[:n]
    
    def print_topn(self, n=1):
        for item in self.topn(n):    
            print item['token'], item['freq']

if __name__ == '__main__':

    f = Freq()
    f.add(['apple', 'juice'])
    f.add(['apple', 'pie'])
    f.add(['orange', 'juice'])
    f.add(['banana', 'split'])
    print f
    f.print_topn(10)