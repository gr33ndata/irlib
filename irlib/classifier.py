''' 
Informations Retrieval Library
==============================
Planned Algorithms:
* Rocchio (Nearest centroid)
* k Nearest Neighbour (kNN)
* Naive Bayes Classifier 
'''

# Author: Tarek Amr <@gr33ndata> 

import sys, math

# Should change below to new class
from aux import SuperList
# from superlist import SuperList
 

class Evaluation:
	'''
	Evaluation: Is used in the testing phase
	In our case, (review spam), this class calculates precision, recall, f-score, etc.
	However, we also make it generic for more than 2 classes classifiers
	Can also dump results in csv files for plotting graphs [Yet to be implemented]
	self.classified_as = [{
			"Deceptive": {"Deceptive": 0, "Truthful": 0},
			"Truthful": {"Deceptive": 0, "Truthful": 0}			
		}]
	'''
	def __init__(self, config=object, fold=0, dump_file=''):
		if fold:
			self.classification_notes = "[Fold %d] %s" % (fold, str(config))
		else:
			self.classification_notes = str(config)
		self.correct = 0
		self.wrong = 0	
	 
	def update(self, query_class='', calculated_class=''):
		if calculated_class == query_class:
			self.correct += 1
		else:
			self.wrong += 1

	def calculate(self, k=0, review_spam=False):
		accuracy =  (self.correct * 100.00)/ (self.correct + self.wrong)
		return accuracy
		
class Index:	
	''' 
	Index is our main class, will inherit others for each IR algorithms from it.
	Its two main data-structures are:
	* terms: This is a simple list of all terms in all training documents
	* matrix: This is our vector space, where terms, documents & classes are mapped to each other
		matrix = [{'id': 'document1',
					'class': 'spam',
					'terms': [1,0,1,0,0,1]
					}]
	* queries: should look exactly like matrix
		queries = [{'id': 'query1',
				'class': 'spam', # In testing: This is the known class, else "n/a".
				'terms': [1,0,1,1,0,1]
					}]
	'''

	# The initialization functions, we set verbose=True for debugging 
	def __init__(self, verbose=False, fold="n/a", config=object, ev=object):
		self.verbose = verbose
		self.fold = fold
		self.config = config
		self.config_data = config.get_configuration()
		self.distance_metric = self.config_data['distance_metric']
		# Set k=0 now, let kNN reset it later on
		self.k = 0
		# confugure the evaluation module
		self.ev = ev
		self.terms = SuperList()
		self.matrix = []
		self.queries = []
		if self.verbose: 
			print "\nInitialization for fold %d done!" % int(fold)

	# Index[key] returns a list of occurences of term (key) in all documents
	def __getitem__(self, key):
		try:
			index = self.terms.index(key)
			return [doc['terms'][index] for doc in self.matrix]
		except:
			if self.verbose: print sys.exc_info()
			raise KeyError

	# Gives some stats about the our training-set
	def diagnose(self):
		print "Diagnose:", self.__class__
		print "- Number of Documents:", len(self.matrix)
		print "- Number of Terms:", len(self.terms)
		#for doc in self.matrix:
		#	print doc['id'], sum(doc['terms'])
		#print "-- Terms:", self.terms

	# To align the length of all rows in matrix after new docs/terms are added to it
	def do_padding(self):
		for doc in self.matrix:
			doc['terms'].do_padding(new_len=len(self.terms), padding_data=0)
		for query in self.queries:
			query['terms'].do_padding(new_len=len(self.terms), padding_data=0)

	# We better keep matrix without log_tf at first, in case we need to do Feature Selection
	# In case of Rocchio we do the log_tf on the fly when calculating the proto_classes
	# Whereas in kNN we might need to call this function
	def matrix_to_log_tf(self):
		for doc in self.matrix:
			doc['terms'] = self.vector_log_tf(doc['terms'])

	# To be used for debugging reasons, displays index and matrix
	def display_idx(self):
		print self.terms
		for doc in self.matrix:
			print doc['id'], doc['class'], doc['terms']

	# Coverts a scalar value to its log_tf (1 + log_10(value) OR zero)
	def log_tf(self, value, do_nothing=False):
		val = float(value)
		if not do_nothing:
			val = 1 + math.log10(val) if val != 0 else float(0)
		return val
	
	# Coverts a vector value to its log_tf (1 + log_10(value) OR zero)
	def vector_log_tf(self, a=[], do_nothing=False):
		new_vector = SuperList()
		for i in range(0,a.__len__()):
			new_vector.append(self.log_tf(value=a[i], do_nothing=do_nothing))
		return new_vector

	# Divides each item in a vector (list) by a scalar number
	def divide_vector(self, vector=[], scalar=1):
		result = SuperList()
		for item in vector:
			result.append(float(item)/scalar)
		return result

	# Add to vectors (lists) to each other and return the resulting vector
	# For each one of them, we can either convert its items into log_tf before addition or not
	def add_vectors(self, a=[], b=[], log_tf_a = True, log_tf_b = True):
		if not b:
			b = SuperList()
			b.do_padding(new_len=a.__len__(), padding_data=0)
		elif a.__len__() != b.__len__():
			if self.verbose: print "add_vectors:", a.__len__(), "!=", b.__len__()
			raise Exception
		sum_vector = SuperList()
		for i in range(0,a.__len__()):
			sum_vector.append(self.log_tf(a[i], do_nothing = not log_tf_a) + self.log_tf(b[i], do_nothing = not log_tf_b))
		return sum_vector

	# Calculates the cosine of the angles between two vectors (lists)
	def cos_vectors(self, a=[], b=[]):
		if a.__len__() != b.__len__():
			if self.verbose: print "cos_vectors:", a.__len__(), "!=", b.__len__()
			raise Exception
		norm_a_sqrd = norm_b_sqrd = 0
		numerator = 0
		for i in range(0,a.__len__()):
			numerator = numerator + a[i]*b[i]
			# Do not use math.pow(), time consuming!
			norm_a_sqrd = norm_a_sqrd + (a[i]*a[i]) 
			norm_b_sqrd = norm_b_sqrd + (b[i]*b[i])
		# In some cases, when one vector is all zeros, division by zero happens
		# Normally this happens when training on small training-set
		# And all vocabulary in query is first time to be seen.
		try:
		 	return_value = numerator / (math.sqrt(norm_a_sqrd) * math.sqrt(norm_b_sqrd))
		except:
			return_value = 0
		return return_value

	# Calculate Euclidean distance between two vectors (lists)
	def euclid_vectors(self, a=[], b=[]):
		if a.__len__() != b.__len__():
			if self.verbose: print "euclid_vectors:", a.__len__(), "!=", b.__len__()
			raise Exception
		euclid_sqrd = 0
		for i in range(0,a.__len__()):
			euclid_sqrd += math.pow((a[i] - b[i]), 2)
		return math.sqrt(euclid_sqrd)

	# Calculate distance between two vectors (lists)
	def calculate_vectors_distance(self, a=[], b=[]):
		if self.distance_metric == "cos":
			return self.cos_vectors(a, b)
		elif self.distance_metric == "euclid":
			return self.euclid_vectors(a, b)

	# We call this each time we are training on a new document
	# It is given the document's doc_class and a list of the parsed doc_terms from it
	# Since each time we get a new documet, we also might get new terms in our terms and matrix list
	# So, if do_padding=True: We extend and pad all old rows in matrix to match the new length of terms now
	# Otherwise, we might be postponing this padding process after we finish adding all docs for processing reasons
	def add_doc(self, doc_id = '', doc_class='', doc_terms=[], do_padding = False):
		my_doc_terms = SuperList()
		for term in doc_terms:
			self.terms.unique_append(term)
			my_doc_terms.insert_after_padding(self.terms.index(term))
		self.matrix.append({'id': doc_id, 'class': doc_class, 'terms': my_doc_terms})
		if do_padding:
			self.do_padding()

	# We call this each time we are training on a new query
	# It is given the document's query_class and a list of the parsed query_terms from it
	# No padding here, since terms in query not learnt during training will be ignored
	def add_query(self, query_id = '', query_class='n/a', query_terms=[]):
		my_query_terms = SuperList()
		my_query_terms.do_padding(new_len=len(self.terms), padding_data=0)
		for term in query_terms:
			try:
				my_query_terms.insert_after_padding(self.terms.index(term))
			except:
				# Term not obtaied in traing phase, ignore it
				pass
		# Calling add_vectors to convert my_query_terms to log_tf values
		self.add_vectors(a=my_query_terms, log_tf_a = True)
		self.queries.append({'id': query_id, 'class': query_class, 'terms': my_query_terms})

	# This is where each classifier may do any calculations after loading traing data
	# We will leave it for each child class to overwrite it on its own way, or ignore it
	# We may add the Feature Selection here, for example: Maximum Information Gain
	# Hence, make sure all child classes call their parent's method before overwriting
	def calculate_training_data(self):
		pass

class Rocchio(Index):	
	''' 
	Rocchio
	The main data-structure here is:
	[*] proto_classes: means of all classes, including query as a class as well
	 	proto_classes = {'spam': {'log_tf': [1, 5, 3], 'docs_count': 12},
	 			'haam': {'log_tf': [3, 1, 4], 'docs_count': 8},
		}
	'''
	
	def __init__(self, **kwargs):
		Index.__init__(self,  **kwargs)	
		self.proto_classes = {}
		# Make sure K is set in configuration to zero
		self.config.update_value('k', 0)

	# Gives some stats about the our training-set
	def diagnose(self):
		Index.diagnose(self)
		#diagnose_filename = "diagnose_fold_%s.txt" % str(self.fold)		
		#fd = open(diagnose_filename, "w")
		#for i in range(0, len(self.terms)):
		#	mystr = "%s" % str(self.terms[i])
		#	for p_class in self.proto_classes:
		#		mystr = "%s, %s" % (mystr, self.proto_classes[p_class]['log_tf'][i])
		#	fd.write("%s\n" % mystr)
		#fd.close()

	# Other than parent's do_padding, we also need to pad proto_classes
	def do_padding(self):
		Index.do_padding(self)
		for pc in self.proto_classes:
			#print type(self.proto_classes[pc]['log_tf'])
			self.proto_classes[pc]['log_tf'].do_padding(new_len=len(self.terms), padding_data=0)

	# This is a common interface for all classed inherited from Index
	# In Rocchio, we will call calculate_proto_classes to compute centroids
	def calculate_training_data(self):
		Index.calculate_training_data(self)
		self.calculate_proto_classes()
		
	# Roccio calculates the mean of all vectors within each class to get a proto_class (centroid)
	# Notice in Rocchio we do not put log_tf in matrix, we calculate them later on when building proto_classes
	def calculate_proto_classes(self):
		vector_len = len(self.terms)
		sum_vector = SuperList()
		for doc in self.matrix:
			if self.proto_classes.has_key(doc['class']):
				# Updating values of existing proto-class with new doc, we only log_tf the newly added vector
				sum_vector = self. add_vectors(a=self.proto_classes[doc['class']]['log_tf'], b=doc['terms'], log_tf_a = False, log_tf_b = True)
				self.proto_classes[doc['class']] = {'log_tf': sum_vector, 'docs_count': self.proto_classes[doc['class']]['docs_count'] + 1}
			else:
				# First time to deal with the class, notice the add_vector will convert to log_tf by default
				sum_vector = self.add_vectors(a=doc['terms'], log_tf_a = True)
				self.proto_classes[doc['class']] = {'log_tf': sum_vector, 'docs_count': 1}
		for p_class in self.proto_classes.keys():
			# Calculate centroid (proto-class) mean values
			self.proto_classes[p_class]['log_tf'] = self.divide_vector(self.proto_classes[p_class]['log_tf'], 
											self.proto_classes[p_class]['docs_count'])
			# Print centroid summations
			#print "Sum of centroid for", p_class, sum(self.proto_classes[p_class]['log_tf'])

	# We treat the query document as a class of its own, for code simplicity,
	# also in case we wanna combine a group of documents together as one query
	# Query should have been entered earlier via add_doc(), with doc_class='qury'
	# Returns (class of query given in testing=True, calculated class)
	# @testing is not used for now, always true.	
	def compare_queries(self, testing=True):
		return_value = []
		for query in self.queries:
			max_cos = {"class_name": "n/a", "value": -1}
			min_euclid = {"class_name": "n/a", "value": 999999}
			#print "Comparing query:", query['class']
			for p_class in self.proto_classes.keys():
				q_distance = self.calculate_vectors_distance(query['terms'], self.proto_classes[p_class]['log_tf'])
				if q_distance > max_cos["value"]:
					max_cos["value"] = q_distance
					max_cos["class_name"] = p_class
				if q_distance < min_euclid["value"]:
					min_euclid["value"] = q_distance
					min_euclid["class_name"] = p_class
			if self.distance_metric == "cos":
				calculated_class = max_cos["class_name"]
			else:
				calculated_class = min_euclid["class_name"]
			return_value.append((query["class"], calculated_class))
			self.ev.update(query_class=query["class"], calculated_class=calculated_class)
		return return_value

class KNN(Index):
	''' 
	K Nearest Neighbour
	'''
	
	def __init__(self, k=1, **kwargs):
		Index.__init__(self,  **kwargs)
		# Try first to read k from configuration file
		# Otherwise, use k given here, or default value		
		try:
			read_k = self.config_data['k']
		except:
			read_k = k
		# We only accept odd values for k
		# otherwise, set k = k - 1
		if read_k % 2:
			self.k = read_k
		else:
			self.k = read_k - 1
		# Make sure to update value in configuration data
		self.config.update_value('k', self.k)

	def diagnose(self):
		Index.diagnose(self)
		if self.verbose: 
			print "- K is set to %d" % self.k


	# This is a common interface for all classed inherited from Index
	# In KNN, we will convert the matrix to log_tf
	def calculate_training_data(self):
		Index.calculate_training_data(self)
		self.matrix_to_log_tf()

	def _greater_than(self, a, b):
		if a["distance"] > b["distance"]: 
			return True
		else:
			return False

	def _less_than(self, a, b):
		if a["distance"] < b["distance"]: 
			return True
		else:
			return False
	
	def get_max_class_count(self, class_counter):
		top_c_name = ''
		top_c_count = 0
		for key in class_counter:
			if class_counter[key] > top_c_count:
				top_c_name = key
				top_c_count = class_counter[key]
				#print "Set top_c to:", top_c_name, top_c_count
		return (top_c_name, top_c_count)

	def get_top_class(self, nearest_docs, query_class=''):
		class_counter = {}
		#print  nearest_docs[0:self.k]
		for doc in  nearest_docs[0:self.k]:
			if class_counter.has_key(doc["class"]):
				class_counter[doc["class"]] += 1
			else:
				class_counter[doc["class"]] = 1
			res = self.get_max_class_count(class_counter)
			self.ev.update(query_class=query_class, calculated_class=res[0])
		return res
	
	# Here we compare loaded queries to decide their classes
	# @testing is always True, not used for now		
	# The list of top_k_classes will look like this:
	# [{"class": "Truthful", "distance": 0.123}]
	def compare_queries(self, testing=True):
		return_value = []
		queries_count = 0
		if self.verbose: 
			print "\nCalculating for %d queries" % len(self.queries)
		# Before doing any comparisons we need to convert the matrix to log_tf
		# Moved the below line to calculate_training_data()
		#self.matrix_to_log_tf()
		for query in self.queries:
			if self.verbose: 
				queries_count += 1
				if queries_count % (len(self.queries)/5) == 0:
					print "- %d querues has been processed" % queries_count 
			top_k_classes = SuperList()
			for doc in self.matrix:
				q_distance = self.calculate_vectors_distance(query['terms'], doc['terms'])
				item = {"class": doc['class'], "distance": q_distance}
				top_k_classes.populate_in_reverse_order(item, self._greater_than)
			if self.distance_metric == "euclid":
				top_k_classes.reverse()
			return_value.append((query["class"], self.get_top_class(nearest_docs=top_k_classes, query_class=query["class"])[0]))
		return return_value


class NaiveBayes(Index):
	''' 
	NaiveBayes Classifier
	Actually, there is no need for a vector space here.
	Instead of matrix, we will use m_variate_matrix Or m_nomial_matrix
	m_*_matrix will look as follows
	{'spam': {'freq': [1,9,5,0,0,4], 'total': 20, 'docs_count': 3}, 
	  'ham': {'freq': [1,4,5,0,3,1], 'total': 14, 'docs_count': 2}}
	Where: 
	 list: total number of times term appears in class-x (m_nomial) 
 	 list: total number of docts term appears in in class-x (m_variate) 
	'''
	def __init__(self, mode='m_variate',  **kwargs):
		Index.__init__(self,  **kwargs)	
		self.m_matrix = {}
		self.total_docs_count = 0	
		self.mode = self.config_data['mode']
		# Make sure K is set in configuration to zero
		self.config.update_value('k', 0)

	# Gives some stats about the our training-set
	def diagnose(self):
		print "Diagnose:", self.__class__
		print "- Number of Documents:", self.total_docs_count
		print "- Number of Terms:", len(self.terms)

	# To be used for debugging reasons, displays index and matrix
	def display_idx(self):
		Index.display_idx(self)
		for c in self.m_matrix:
			print c, self.m_matrix[c]

	# Other than parent's do_padding, we also need to pad proto_classes
	def do_padding(self):
		Index.do_padding(self)
		for c in self.m_matrix:
			self.m_matrix[c]['freq'].do_padding(new_len=len(self.terms), padding_data=0)

	# Helper functions, when given a list = [0,1,2,0,1,3,0]
	# It returns list with indices of non zero values [1,2,4,5]
	def _non_zero_indices(self, l):
		ret = SuperList()
		for i in range(0,len(l)):
			if l[i] != 0: ret.append(i)
		return ret

	# Unlike Rocchio and kNN, we need to overwrite the add_doc method
	def add_doc(self, doc_id = '', doc_class='', doc_terms=[], do_padding = True):
		# If multivariant, remove multiple occurences of terms in document
		#print "Bayse >> add_doc", doc_terms
		if self.mode == 'm_variate':
			doc_terms = list(set(doc_terms))
		#print doc_terms
		for term in doc_terms:
			self.terms.unique_append(term)
			# In case this is the first time to see this class
			if not self.m_matrix.has_key(doc_class):
				self.m_matrix[doc_class] = {'freq': SuperList(), 'total': 0, 'docs_count': 0}	
			self.m_matrix[doc_class]['freq'].insert_after_padding(index=self.terms.index(term))
		self.m_matrix[doc_class]['docs_count'] += 1
		if do_padding:
			self.do_padding()

	# Unlike Rocchio and kNN, we need to overwrite the add_query method
	# Here we need a way to record new terms not see during training
	# We also do not want to convert values to log_tf in Bayesian
	def add_query(self, query_id = '', query_class='n/a', query_terms=[]):
		my_query_terms = SuperList()
		my_query_terms.do_padding(new_len=len(self.terms), padding_data=0)
		new_terms_count = 0
		for term in query_terms:
			try:
				my_query_terms.insert_after_padding(self.terms.index(term))
			except:
				# Term not obtaied in traing phase
				new_terms_count += 1
		self.queries.append({'id': query_id, 'class': query_class, 'terms': my_query_terms, 'new_terms_count': new_terms_count})

	def calculate_training_data(self):
		Index.calculate_training_data(self)
		for c in self.m_matrix:
			self.m_matrix[c]['total'] = sum(self.m_matrix[c]['freq'])
			self.total_docs_count += self.m_matrix[c]['docs_count'] 
			
	# Here we compare loaded queries to decide their classes
	# @testing is always True, not used for now	
	# Remember, self.m_matrix[doc_class] = {'freq': SuperList(), 'total': 0, 'docs_count': 0}	
	def compare_queries(self, testing=True):
		return_value = []
		for query in self.queries:
			max_value = {"class_name": "n/a", "value": -99999}
			for doc_class in self.m_matrix:
				prob_c = self.m_matrix[doc_class]['docs_count'] * 1.00 / self.total_docs_count
				prob_terms = 0
				for term_index in self._non_zero_indices(query['terms']):
					if self.mode == 'm_variate':
						prob_term = (self.m_matrix[doc_class]['freq'][term_index] + 1.00) / (self.m_matrix[doc_class]['total'] + 2)
					else:
						prob_term = (self.m_matrix[doc_class]['freq'][term_index] + 1.00) / (self.m_matrix[doc_class]['total'] + len(self.terms))
					prob_terms += math.log10(prob_term)
				# Don't forget to add new terms not seen during training
				prob_terms += query['new_terms_count'] * math.log10(1.00/len(self.terms))
				# Now add class probability too
				class_val = prob_terms + math.log10(prob_c)
				if class_val > max_value["value"]:
					max_value["class_name"] = doc_class
					max_value["value"] = class_val
			return_value.append((query["class"], max_value["class_name"]))
			self.ev.update(query_class=query["class"], calculated_class=max_value["class_name"])
		return return_value

if __name__ == '__main__':

	import classifier
	config = classifier.Configuration(config_file='classifier.conf')
	config.load_configuration()

	r = NaiveBayes(verbose=True, fold=1, config=config, ev=object)
	r.add_doc(doc_id = 'd1', doc_class='spam', doc_terms=['bye', 'goodbye', 'see-ya' ])
	r.add_doc(doc_id = 'd2', doc_class='spam', doc_terms=['bye', 'adios', 'goodbye' ])
	r.add_doc(doc_id = 'd3', doc_class='spam', doc_terms=['bye', 'bye', 'goodbye' ])
	r.add_doc(doc_id = 'd4', doc_class='haam', doc_terms=['hi', 'hello', 'hola' ])
	r.add_doc(doc_id = 'd5', doc_class='haam', doc_terms=['morning', 'hi', 'hola' ])	
	r.add_doc(doc_id = 'd6', doc_class='haam', doc_terms=['hi', 'hi', 'hi', 'hello', 'hello' ])	
	r.do_padding()
	r.display_idx()
	#r.calculate_proto_classes()
	r.add_query(query_id = 'q1', query_class='qury_haam', query_terms=['bye', 'hello', 'hi'])
	r.add_query(query_id = 'q2', query_class='qury_spam', query_terms=['bye', 'bye', 'goodbye'])
	r.add_query(query_id = 'q3', query_class='qury_spam', query_terms=['bye', 'aloha', 'goodbye'])
	r.calculate_training_data()
	r.compare_queries()
	r.display_idx()


