''' 
Review Spam Classifier 
======================
What it reallt does:
* Load configuration 
* Load preprocessor (preprocessor.py)
* Load classifier (irlib.py) specified by configuration 
* Train on all folds but one
* Test on remaining fold
* Permutate and do previous two steps on all folds
* Get results
'''

# Author: Tarek Amr <@gr33ndata> 

import os
import re
import sys

# Adding this to path to be able to import irlib
sys.path.append('../../')

# Importing the irlib stuff
from irlib.classifier import NaiveBayes
from irlib.classifier import Rocchio  
from irlib.classifier import KNN  
from irlib.classifier import Evaluation 
from irlib.preprocessor import Preprocessor  
from irlib.configuration import Configuration  


VERBOSE = True

def get_doc_id(fold=1, filename=""):
	doc_id = 'fold' + str(fold) + ':' + filename.split(".")[0]
	return doc_id


# Parse not any more than the first_n_files in folder
# @ml: Object for our classifier class (Rocchio, kNN, etc)
# @config: Our configuration class (class as in OOP not ML)
# @prep: Preprocessor class; tokenizers, stemmers, etc.
def parse_files(fold=1, mode = "training", first_n_files = 10000, ml=object, config=object, prep=object):
	config_data = config.get_configuration()
	#DOCSDIR = config_data['docs_dir']
	#fold_path = DOCSDIR + str(fold)	+ "/original-text-files"
	fold_path = config.get_fold_path(fold)
	files = os.listdir(fold_path)
	#print files	
	for filename in files[0:first_n_files]:
		class_name = ""
		for c in config_data['classes']:
			if filename.startswith(c):
				class_name = config_data['classes'][c]
		# Skip if failed to identify file's class
		if not class_name:
			continue	
		doc_id = get_doc_id(fold, filename)
		fd = open('%s/%s' % (fold_path, filename), 'r')
		file_data = fd.read()
		terms = prep.ngram_tokenizer(text=file_data)
		if mode == 'training':
			ml.add_doc(doc_id = doc_id, doc_class=class_name, doc_terms=terms)
		else:
			# Class known from filename
			ml.add_query(query_id = doc_id, query_class=class_name, query_terms=terms)	
		fd.close()

# Let's do some workout now on all folders but one
def training(config, test_fold, ml, prep):
	folds = config.get_all_folds_but(test_fold)
	for fold in folds:
		parse_files(fold = fold, mode = 'training', first_n_files = 1000, ml=ml, config=config, prep=prep)

# Let's test on the remaining folder
def testing(config, test_fold, ml, ev, prep):
	parse_files(fold = test_fold, mode = 'testing', first_n_files = 10000, ml=ml, config=config, prep=prep)
	ml.compare_queries()

# Call this if anything goes wrong, for clean exit
def classifier_exit():
	if VERBOSE: 
		print sys.exc_info()
	print "\n[!] Houston, we have a problem [!]" 
	raise
	sys.exit()

# Our main function
def main():

	# Load configuration from file
	config = Configuration(config_file='classify.conf')
	try:
		config.load_configuration()
		config_data = config.get_configuration()
	except:
		print "Error loading configuration file."
		print "Classifier aborting."
		raise 	
	
	#config.display_configuration()
	print config

	#sys.exit()
	
	myfolds = config.get_folds()
	correctness = 0

	#Preporcessor: tokenizer, stemmer, etc.
	prep_lower = config_data['lower']
	prep_stem = config_data['stem']
	prep_pos = config_data['pos']
	prep_ngram = config_data['ngram'] 
	prep = Preprocessor(pattern='\W+', lower=prep_lower, stem=prep_stem, pos=prep_pos, ngram=prep_ngram)

	for myfold in myfolds:
		ev = Evaluation(config=config, fold=myfold)
		if config_data['classifier'] == 'rocchio':
			ml = Rocchio(verbose=VERBOSE, fold=myfold, config=config, ev=ev)
		elif config_data['classifier'] == 'knn':
			ml = KNN(verbose=VERBOSE, fold=myfold, config=config, ev=ev)
		else:
			ml = NaiveBayes(verbose=VERBOSE, fold=myfold, config=config, ev=ev)
		training(config, myfold, ml, prep )
		ml.do_padding()
		ml.calculate_training_data()
		#r.display_idx()
		ml.diagnose()
		testing(config, myfold, ml, ev, prep)
		
		k = config_data['k']
		results = ev.calculate(review_spam=True, k=k)
		print 'Accuracy for fold %d: %s' % (myfold, results)

		correctness += results	

	print "\nAverage accuracy for all folds:", correctness / len(myfolds) 


if __name__ == '__main__':

	# Profiling mode is not to be used in production,
	# only used for profiling the code's performance.
	profiling_mode = False
	if profiling_mode: 
		import cProfile
		import pstats
		cProfile.run('main()','classifier_prof')
		p_stats = pstats.Stats('classifier_prof')
		p_stats.sort_stats('time').print_stats(10)
	else:
		try:
			main()
		except:
			classifier_exit()
			


	



