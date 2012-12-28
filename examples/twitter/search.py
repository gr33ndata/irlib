# Search in tweets

import os, sys

# Adding this to path to be able to import irlib
sys.path.append('../../')

from irlib.preprocessor import Preprocessor
from irlib.matrix import Matrix

def readfiles(fold_path='all-folds/fold1/'):

    prep = Preprocessor()
    mx = Matrix()

    files = os.listdir(fold_path)
    for filename in files:
        fd = open('%s/%s' % (fold_path, filename), 'r')
        file_data = fd.read()
        terms = prep.ngram_tokenizer(text=file_data)
        mx.add_doc(doc_id=filename, doc_terms=terms, 
                frequency=True, do_padding=True)


    print 'Number of read documents:', len(mx.docs)
    print 'Number of read terms', len(mx.terms)
    #print mx.terms[0:5], mx.terms[-5:-1]
    print mx.terms
    print mx.docs

def search():

    while True:
        q = raw_input("Search: ")
        q = q.strip()
        if not q:
            return
        else:
            #search here
            pass
        
def main():
    readfiles()
    #search()
    
    
if __name__ == "__main__":
    main()

