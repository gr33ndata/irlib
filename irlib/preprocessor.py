''' 
Preprocessor
============
Included Preprocessors:
* Tokenized 
* N-Gram Tokenizer
* PoS Tagger (from NLTK)
* Stemmer (from NLTK)
* Cut off terms, with frequency less than min_freq
'''

# Author: Tarek Amr <@gr33ndata> 

import re
from aux import SuperList

try:
	import nltk as my_nltk
except:
	print '[!] Warning: NLTK is not installed on system'	
	my_nltk = None

	
class Preprocessor:
	
	def __init__(self, pattern='\W+', lower=False, stem=False, stemmer_name='porter', pos=False, ngram=1):
		# RE pattern used in tokenization
		self.pattern = pattern
		# Ngram: Default = 1
		self.ngram = int(ngram)
		# Convert terms to lower case
		self.lower = lower
		# Ignore PoS and Stemmers if NLTK not installed
		if not my_nltk:
			self.pos = False
			self.stem = False
		else:	
			self.pos = pos
			self.stem = stem
			self.stemmer_name = stemmer_name
			self.stemmers = {'lancaster': my_nltk.LancasterStemmer(), 'porter': my_nltk.PorterStemmer()}
		self.frequent_terms = []

	# Gets a string of text and returns tokens (terms)
	def tokenizer(self, text=''):
		if self.pos:
			# Get PoS tokens instead of real terms.
			# Here, I better use NLTK own tokenizer,
			# for more compatibility with their tagger
			terms = my_nltk.word_tokenize(text)	
			terms = my_nltk.pos_tag(terms)
			terms = [t[1] for t in terms]
		else:
			terms = re.split(self.pattern, text)
			# Filter-out empty strings and stem if asked to	
			terms = [self.stemmer(t) for t in terms if len(t.strip()) > 0]
		return terms

	# Gets a string of text and returns n-gram tokens (terms)
	def ngram_tokenizer(self, text=''):
		n = self.ngram
		terms = self.tokenizer(text=text)
		if n == 1:
			return terms
		n_grams = []
		for i in range(0,len(terms)-n+1):
			n_grams.append(" ".join(terms[i:i+n]))
		return n_grams

	def stemmer(self, term):
		if self.stem:
			# I think we better stem terms before converting them into lower-case 
			stemmer = self.stemmers[self.stemmer_name]
			term = stemmer.stem(term)
		if self.lower:
			term = term.lower()
		return term	


if __name__ == '__main__':

	p = Preprocessor()
	p.get_infrequent_terms('')
