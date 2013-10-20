''' 
Informations Retrieval Library
==============================
Matrix is an index for documents, terms, and their classes. 
'''

# Author: Tarek Amr <@gr33ndata> 

import sys, math
from superlist import SuperList
from progress import Progress

def log_tf(value):
    ''' The log(tf) 
        returns: 1 + log_10(value) if value != 0 
               : 0 if value == 0
    '''
    val = float(value)
    val = 1 + math.log10(val) if val != 0 else float(0)
    return val

class Matrix:

    def __init__(self, whitelist=[]):
        ''' Initilize our matrix.
            whitelist: If not empty, discard any terms not in whitelist,
                       when adding new terms via add_doc()
            terms: We will populate this with our vocabulary of terms
            docs: This is our actual 2D matrix terms/docs.
                  A list of the following dictionary,
                  { 'id': Unique ID to each document, 
                    'class': In case of labeled data, doc class label, 
                    'terms': list of 1's and 0's, i.e. term Frequencies.
                  }
        '''
        # List of unique terms (vocabulary)
        self.terms = SuperList()
        # List of document classes and terms summary
        #self.classes = {}
        self.docs = []
        self.whitelist = whitelist

    def __len__(self):
        'Returns number of loaded ducuments'
        return len(self.docs)

    def vocabulary(self, threshold_map=[]):
        '''Returns list of all unique terms if threshold_map not given.
           Otherwise, only return terms above threshold.        
        '''
        if not threshold_map:
            return self.terms
        elif len(threshold_map) == len(self.terms):
            vlist = []
            for i in range(len(self.terms)):
                if threshold_map[i] == 1:
                   vlist.append(self.terms[i])
            return vlist 
        else:
            return []
            
            
    def __str__(self):
        s  = 'Matrix:'
        s += '\n * Vocabulary read: %d' % len(self.terms)
        s += '\n * Documents read: %d' % len(self.docs)
        return s

    def dump_tf(self, filename, freqs, delimiter='\t', header=True):
        ''' Dumps term frequencies
        '''
        fd = open(filename,'w')
        # Let's first print file header
        header_line = 'term'
        header_line = header_line + delimiter + 'freq'
        if header:
            fd.write('%s\n' % header_line)
        # Now we print data lines
        terms = self.vocabulary()
        for i in range(len(terms)):
            line = terms[i]
            line = line + delimiter + str(freqs[i])
            fd.write('%s\n' % line)
        fd.close()
        
    def dump(self, filename, delimiter='\t', header=True):
        ''' Dumps matrix to a file
        '''
        fd = open(filename,'w')
        # Let's first print file header
        header_line = 'id'
        header_line = header_line + delimiter + 'class'
        for term in self.terms:
            header_line = header_line + delimiter + term
        if header:
            fd.write('%s\n' % header_line)
        # Now we print data lines
        for doc in self.docs:
            line = doc['id']
            line = line + delimiter +  doc['class']
            for term in doc['terms']:
                line = line + delimiter + str(term) 
            fd.write('%s\n' % line)
        fd.close()
    
    def dump_arff(self, filename, delimiter=',', clstype='NUMERIC'):
        ''' Dumps matrix to a file
        '''
        fd = open(filename,'w')
        header = '@RELATION %s\n\n' % filename.split('.')[0]
        header = header + '@ATTRIBUTE \'ARFFID\' NUMERIC\n'
        for term in self.terms:
            header = header + '@ATTRIBUTE \'' + term + '\' NUMERIC\n'
        header = header + '@ATTRIBUTE \'ClassLabel\' ' + clstype + '\n'
        fd.write('%s\n' % header)
        
        # Now we print data lines
        fd.write('@DATA\n')
        for doc in self.docs:
            line = doc['id']
            for term in doc['terms']:
                line = line + delimiter + str(term) 
            line = line + delimiter +  str(doc['class'])
            fd.write('%s\n' % line)
        fd.close()
        
        
    def dump_transposed(self, filename, delimiter='\t', header=True):
        fd = open(filename,'w')
        # Let's first print file header
        header_line = 'terms'
        for doc in self.docs:
            header_line = header_line + delimiter + doc['id']
        if header:
            fd.write('%s\n' % header_line)
        # Now we print data lines
        idx = 0
        for term in self.terms:
            line = term
            for doc in self.docs:
                line = line + delimiter + str(doc['terms'][idx]) 
            fd.write('%s\n' % line)
            idx += 1
        fd.close()
    
    def dump_transposed_arff(self, filename):
        fd = open(filename,'w')
        # Let's first print file header
        header = '@RELATION %s\n\n' % filename.split('.')[0]
        header = header + '@ATTRIBUTE terms STRING\n'
        for doc in self.docs:
            header = header + '@ATTRIBUTE "%s" NUMERIC\n' % doc['id']
        fd.write('%s\n' % header)
        
        # Now we print data lines
        fd.write('@DATA\n')
        idx = 0
        delimiter = ','
        for term in self.terms:
            line = '"%s"' % term
            for doc in self.docs:
                line = line + delimiter + str(doc['terms'][idx]) 
            fd.write('%s\n' % line)
            idx += 1
        fd.close()
        
    def prune_old(self, prune_map):
        ''' Helper method to remove terms (fields) of our matrix
            prune_map is a list of 0's and 1's of same length as self.terms.
            For each term, if 0, then remove it, otherwise keep it.
        '''
        if not(prune_map) or len(prune_map) != len(self.terms):
            return False
        for i in range(len(prune_map)-1,-1,-1):
            if prune_map[i] == 0:
                #print self.terms[i]
                self.terms.pop(i)
                for doc in self.docs:
                    doc['terms'].pop(i)
                    
    def prune(self, prune_map, show_progress=True):
        ''' Helper method to remove terms (fields) of our matrix
            prune_map is a list of 0's and 1's of same length as self.terms.
            For each term, if 0, then remove it, otherwise keep it.
        '''
        if not(prune_map) or len(prune_map) != len(self.terms):
            return False
        if show_progress:
            print '  Pruning terms list ...'
        new_terms =  SuperList()
        for i in range(len(prune_map)-1,-1,-1):
            if prune_map[i] == 1:
                #print self.terms[i]
                new_terms.append(self.terms[i])
        self.terms = new_terms
        if show_progress:
            print '  Pruning documents ...'
        p = Progress(n=len(self), percent=10)
        for doc in self.docs:
            new_doc_terms =  SuperList()
            for i in range(len(prune_map)-1,-1,-1):
                if prune_map[i] == 1:
                    new_doc_terms.append(doc['terms'][i])
            doc['terms'] = new_doc_terms
            if show_progress:
                p.show(message='  Pruning progress:')
                     
    def freq_levels(self, threshold=3):
        ''' Creates two lists:
            threshold_map is a list of 0's and 1's,
            where 1 means term's freq >= threshold
            freq_map is a list of terms frequences
        '''
        threshold_map = [0] * len(self.terms)
        freq_map = [0] * len(self.terms)
        for i in range(0,len(self.terms)):
            val = 0
            for doc in self.docs:
                if doc['terms'][i] != 0:
                    #val += 1 
                    val += doc['terms'][i]
            if val >= threshold:
                threshold_map[i] = 1
            freq_map[i] = val
        return (threshold_map, freq_map)         
        
    def __contains__(self, term):
        'Checks if certain terms is loaded'
        return self.terms.__contains__(term)        

    def to_be_deleted__getitem__(self, term):
        'Returns occurences of term in all documents'
        if not term in self:
            return SuperList()
        col = [doc['terms'][self.terms.index(term)] for doc in self.docs]
        return SuperList(col)
        
    def __getitem__(self, term):
        ''' If term exists in terms, retruns it position in list,
            otherwise, return -1
        '''    
        if not term in self:
            return -1
        else:
            return self.terms.index(term)
    
    def do_padding(self):
        ''' Align the length of all rows in matrix
            Each time we see a new term, list of terms is expanded,
            and the matrix row for such document is of same length too.
            But what about rows added earlier for previous documents?
            So, this method alighn all previously added rows, 
            to match the current length of the terms list.
        '''
        if len(self.docs[-1]['terms']) == len(self.docs[0]['terms']):
            return
        for doc in self.docs:
            doc['terms'].expand(new_len=len(self.terms))
        #for cls in self.classes:
        #    self.classes[cls].expand(new_len=len(self.terms))

    def _log_tf(self, value):
		val = float(value)
		val = 1 + math.log10(val) if val != 0 else float(0)
		return val
		
    def tf_idf(self, do_idf=True):
        ''' Converts matrix to tf.idf values
            do_idf: if False, convert to tf only
        '''        
        N = len(self.docs)
        df = SuperList([0] * len(self.terms))
        for doc in self.docs:
            row = SuperList([0] * len(self.terms))
            for idx in range(len(self.terms)):
                if doc['terms'][idx] > 0:
                    row[idx] = 1
            df.add(row)
        
        for doc in self.docs:
            for idx in range(len(self.terms)):
                tf = self._log_tf(doc['terms'][idx])
                idf = math.log10(float(N) / df[idx])
                if do_idf:
                    doc['terms'][idx] = tf * idf
                else:
                    doc['terms'][idx] = tf

 
    def add_doc(self, doc_id = '', doc_class='', doc_terms=[], 
                frequency=False, do_padding=False, 
                unique_ids=False, stopwords=[]):
        ''' Add new document to our matrix:
            doc_id: Identifier for the document, eg. file name, url, etc. 
            doc_class: You might need this in classification.
            doc_terms: List of terms you got after tokenizing the document.
                       Terms can be typles; string and frequencies
            frequency: If true, term occurences is incremented by one.
                        Else, occurences is only 0 or 1 (a la Bernoulli)
            do_padding: Boolean. Check do_padding() for more info.
            unique_ids: When true, if two documents are added with same id,
                        then their terms are summed up into only one record.
            stopwords: If not empty, ignore those stop words in doc_terms 
        ''' 
        # Update list of terms if new term seen.
        # And document (row) with its associated data.
        my_doc_terms = SuperList()
        # Discard anything not in whitelist if it is not empty
        if self.whitelist:
            doc_terms = [t for t in doc_terms if t in self.whitelist]
        # Discard anything in stopwords if not empty
        if stopwords:
            doc_terms = [t for t in doc_terms if t not in stopwords]
        for term in doc_terms:
            if type(term) == tuple:
                term_idx = self.terms.unique_append(term[0])
                my_doc_terms.increment_after_padding(term_idx,term[1])
            else:
                term_idx = self.terms.unique_append(term)
                if frequency:
                    my_doc_terms.increment_after_padding(term_idx,1)
                else:
                    my_doc_terms.insert_after_padding(term_idx,1)
        # In the rare event when whitelisting causes an empty doc_terms list
        # We add at least one zero in the list of my_doc_terms
        if not my_doc_terms:
            zeros = [float(0)] * len(self.vocabulary())
            my_doc_terms = SuperList(zeros)
            
            
        if unique_ids:
            found = 0
            for doc in self.docs:
                if doc['id'] == doc_id:
                    doc['terms'].add(my_doc_terms)
                    found = 1
            if not found:        
                self.docs.append({'id': doc_id, 
                                  'class': doc_class, 
                                  'terms': my_doc_terms}) 
        else:
            self.docs.append({  'id': doc_id, 
                                'class': doc_class, 
                                'terms': my_doc_terms})
        # Update list of document classes if new class seen.
        #self.classes.unique_append(doc_class)
        #if self.classes.has_key(doc_class):
        #else:
        #    self.classes[doc_class].add(my_doc_terms)
        #    self.classes[doc_class] = my_doc_terms
        if do_padding: 
            self.do_padding()
        

    def query_to_vector(self, q_terms, frequency=False,):
        ''' Converts query to a list alligned with our self.terms.
            Terms not seen before will be ignored.
            q_terms: list of query terms
            frequency: return a multinomial or multivariate list?
        '''
        my_query_vector = SuperList()
        my_query_vector.expand(new_len=len(self.terms))
        for term in q_terms:
            try:
                term_idx = self.terms.index(term)
            except:
                # Term not seen before, skip
                continue
            #print term, self.terms.index(term)
            if frequency:
                my_query_vector.increment_after_padding(term_idx,1)
            else:
                my_query_vector.insert_after_padding(term_idx,1)
        return my_query_vector
        
    def get_stats(self):
        return Stats(self)




'''
classes = {
    'class1': {'terms': [1,2,0,3], 'totel': 6}
}
terms = []
'''    
class Stats:

    def __init__(self, matrix):
        self.mx = matrix
        self.N  = 0
        self.classes = {}
        
        #self.terms = SuperList()       
        #for c in self.mx.classes:
        #    self.classes[c] = {}
        #    self.classes[c]['terms'] = self.mx.classes[c]
        #    self.terms.add(self.classes[c]['terms'])
        #    self.classes[c]['total'] = sum(self.classes[c]['terms'])
        #    self.N += self.classes[c]['total']
        #self.mi_terms = []
        
    def __str__(self):
        s  = 'Matrix Stats:'
        s += '\n * Vocabulary/Terms: %d/%d' % (len(self.terms), self.N)
        return s
        
    def getN(self):
        ''' Get total number of terms, counting their frequencies too.
            Notice: This is not the same as len(vocabulary)
        '''
        return self.N
        
    def get_terms_freq(self, normalized=False):
        ''' Returns 2d matrix of vocabulary terms and their occurences
            if normalized is True, devide by total number of terms
        '''
        terms = self.mx.terms
        freq = self.terms.div(self.N) if normalized else self.terms
        return [terms, freq] 
            
    def pr_term(self, t):
        ' Get probability of term t '
        i = self.mx[t]
        if i == -1:
            return 0
        return float(self.terms[i]) / self.N

    def pr_class(self, c):
        ' Get probability of class c '
        return float(self.classes[c]['total']) / self.N
        
    def pr_joint(self, t, c):
        'Get joint probability between term t and class c'
        i = self.mx[t]
        if i == -1:
            return 0
        return float(self.classes[c]['terms'][i]) / self.N
        
    def mi(self):
        for t in self.mx.vocabulary():
            mi = 0
            for c in self.classes:
                try:
                    mi += self.pr_joint(t,c) * math.log10( self.pr_joint(t,c) / ( self.pr_term(t) * self.pr_class(c) ))
                except:
                    # Oh, log(0), let's set mi = 0
                    mi = 0
            self.mi_terms.append(mi) 
        print self.classes    
        print self.mi_terms
        
if __name__ == '__main__':

    pass
