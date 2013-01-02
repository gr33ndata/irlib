# Using IR to answer your question
# Not so smart question and answer system

import os, sys
import random

# Adding this to path to be able to import irlib
sys.path.append('../../')

from irlib.preprocessor import Preprocessor
from irlib.matrix import Matrix
from irlib.metrics import Metrics

#qa_list = {'id':{'q': 'question', 'a': 'answer')}

class QA:
    
    def __init__(self):
        self.file_name = 'qa.txt'
        self.qa_list = {}
        self.qa_id = 0
        self.prep = Preprocessor()
        self.mx = Matrix()
        self.metric = Metrics()
        
    def randomize(self, a):
        for i in range(len(a)):
            a[i] = random.randint(0,1)

    def readfile(self):

        fd = open(self.file_name,'r')
        for line in fd.readlines():
            line = line.strip().lower().split(':')
            if len(line) != 2:  
                continue
            elif line[0] == 'q':
                q_line = ' '.join(line[1:])
                self.qa_id += 1
                self.qa_list[self.qa_id] = {'q': q_line, 'a': ''}
                terms = self.prep.ngram_tokenizer(text=q_line)
                self.mx.add_doc(doc_id=self.qa_id, doc_terms=terms, 
                        frequency=True, do_padding=True)
            elif line[0] == 'a': 
                a_line = ' '.join(line[1:])
                self.qa_list[self.qa_id]['a'] = a_line
        
        #print 'Number of read questions and answers:', len(self.mx.docs)
        #print 'Number of read terms', len(self.mx.terms)
               
    def ask(self, q=''):

        q_id = 0
        q_distance = 99999

        terms = self.prep.ngram_tokenizer(text=q)
        q_vector = self.mx.query_to_vector(terms, frequency=False)

        if sum(q_vector) == 0:
            self.randomize(q_vector)

        for doc in self.mx.docs:
            distance = self.metric.euclid_vectors(doc['terms'], q_vector)
            if distance < q_distance:
                q_distance = distance
                q_id = doc['id']
    
        print 'Tarek:', self.qa_list[q_id]['a']
    
def main():

    qa = QA()
    qa.readfile()

    while True:
        q = raw_input("\nAsk me something: ")
        q = q.strip()
        if not q:
            return
        else:
            qa.ask(q=q)

    
    
if __name__ == "__main__":
    main()

