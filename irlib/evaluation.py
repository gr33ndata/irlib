''' 
Informations Retrieval Library
==============================
Evaluation, used to evaluate classifier's accuracy
'''

# Author: Tarek Amr <@gr33ndata> 

import sys, math

from superlist import SuperList
from progress import Progress
from preprocessor import Preprocessor

'''
ev_results = {
    'apples': {'TP': 14, 'FP': 12},
    'oranges': {'TP': 15, 'FP': 11}
}
'''

class Evaluation:

    def __init__(self, verbose=False):
        self.ev_results = {}
        self.doc_count = 0
    
    def get_classes_labels(self):
        target_classes = self.ev_results.keys()
        target_classes.sort()
        return target_classes
            
    def ev(self, calculated_id, actual_id):
        calculated_id = str(calculated_id).strip()
        actual_id =str(actual_id).strip()
        if not calculated_id in self.ev_results:
            self.ev_results[calculated_id] = {'TP': 0, 'FP': 0, 'FN': 0}
        if not actual_id in self.ev_results:
            self.ev_results[actual_id] = {'TP': 0, 'FP': 0, 'FN': 0}
        if calculated_id == actual_id:
            self.ev_results[calculated_id]['TP'] += 1
        else:
            self.ev_results[calculated_id]['FP'] += 1 
            self.ev_results[actual_id]['FN'] += 1 
        self.doc_count += 1
    
    def tp(self, class_id):
        return float(self.ev_results[class_id]['TP'])
        
    def tn(self, class_id):
        val = self.doc_count \
            - self.tp(class_id) \
            - self.fp(class_id) \
            - self.fn(class_id)
        return float(val)
    
    def fp(self, class_id):
        return float(self.ev_results[class_id]['FP'])
        
    def fn(self, class_id):
        return float(self.ev_results[class_id]['FN'])
        
                
    def tp_rate(self, class_id):
        val = self.tp(class_id) \
           / (self.tp(class_id) + self.fn(class_id))
        return val
    
    def fp_rate(self, class_id):
        val = self.fp(class_id) \
           / (self.fp(class_id) + self.tn(class_id))   
        return val
        
    def precision(self, class_id):
        if not self.fp(class_id):
            return 1
        val = self.tp(class_id) \
                / (self.tp(class_id) + self.fp(class_id))
        return val
        
    def recall(self, class_id):
        # Note: Same as TP rate
        return self.tp_rate(class_id)

    def f1score(self, class_id):
        #P = self.precision(class_id)
        #R = self.recall(class_id)
        #print 'P-R:', P, R
        #f1 = (2 * P * R) / (P + R)
        TP = self.tp(class_id)
        FP = self.fp(class_id)
        FN = self.fn(class_id)
        f1 = float(2*TP) / ((2*TP) + FP + FN)
        return f1   
        
    def macro_f1(self, percent=True):
        # Returns Average F1-Score
        f1 = w = 0
        for class_id in self.ev_results:
            w += 1
            f1 += self.f1score(class_id) 
        avg = float(f1)/w
        if percent:
            avg = avg * 100
        return avg  
           
    def overall_accuracy(self, percent=True):
        correct = 0
        incorrect = 0
        for class_id in self.ev_results:
            correct += self.ev_results[class_id]['TP'] 
            incorrect += self.ev_results[class_id]['FP']
        acc = float(correct) / (correct + incorrect)
        if percent:
            acc = acc * 100
        return acc      

    def printev(self):
        for target_class in self.get_classes_labels():
            print target_class, \
                'TP-rate', self.tp_rate(target_class), \
                'FP-rate', self.fp_rate(target_class)
        print self.overall_accuracy()
