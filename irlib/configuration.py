# Reads configuration parameters from file 'classifier.conf'. 
# Used for sharing the configuration between all modules 

# Author: Tarek Amr <@gr33ndata> 

class Configuration:
	
	# Initialize some variables and default values
	def __init__(self, config_file='classifier.conf'):
		self.config_file=config_file
		self.configuration = {}
		self.configuration['classes'] = {}
		self.configuration['k'] = 0
		self.configuration['pos'] = False
		self.configuration['stem'] = False
		self.configuration['ngram'] = 1

	# Remove white spaces and convert to lowercase
	def parse_config_attribute(self, attr=''):
		a = attr.strip().lower()
		return a

	# Remove white spaces and convert to lowercase
	# Compile true and false strings	
	def parse_config_value(self, value=''):
		v = value.strip().lower()
		if v == 'true':
			v = True
		elif v == 'false':
			v = False
		return v

	# Split lines into attributes and values
	def extract_attr_value(self, conf_line=''):
		(attr, value) = conf_line.split(':')
		a = self.parse_config_attribute(attr)
		v = self.parse_config_value(value)
		return (a,v)

	def update_value(self, attr, value):
		self.configuration[attr] = value	

	def populate_class_names(self, conf_line=''):
		conf_line = conf_line[1:].strip('(').strip(')')
		(c_id, c_name) = conf_line.split(':')
		self.configuration['classes'][c_id] = c_name		

	def load_configuration(self):
		fd = open(self.config_file, 'r')
		for line in fd.readlines():
			line = line.strip()
			if line.startswith('#'):
				pass # comment line
			elif line.startswith('$'):
				self.populate_class_names(line)
			elif line:
				(attr, value) = self.extract_attr_value(line)
				self.configuration[attr] = value
		self.configuration['k'] = int(self.configuration['k'])
		fd.close()

	def get_configuration(self):
		return self.configuration

	def get_fold_path(self, fold=0):
		path = "%s/%s%s" % (self.configuration['data_path'], self.configuration['folds_prefix'], str(fold))
		return path

	# Returns the configuration hash-table (a la C/C++ Structures)
	def display_configuration(self):
		for item in self.configuration:
			print item, self.configuration[item]

	# Returns a summary of configuration as a string
	def __str__(self):
		enabled_options = []
		if not self.configuration:
			return "No configuration loaded yet!"
		else:
			if self.configuration['classifier'] == 'knn':
				try:
					classifier_str = "%s-NN" % self.configuration['k']
				except:
					classifier_str = "k-NN"
				enabled_options.append("Metric: %s, " % self.configuration['distance_metric'])
			elif self.configuration['classifier'] == 'rocchio':
				classifier_str = self.configuration['classifier'].title()
				enabled_options.append("Metric: %s, " % self.configuration['distance_metric'])
			elif self.configuration['classifier'] == 'bayes':
				classifier_str = self.configuration['classifier'].title()
				enabled_options.append("Mode: %s, " % self.configuration['mode'])
			else:
				classifier_str = "No proper classifier set!"
			if self.configuration['pos'] == True:
				enabled_options.append("PoS, ")
			if self.configuration['stem'] == True:
				enabled_options.append("Stemmer(%s), " % self.configuration['stemmer_name'])
			if int(self.configuration['ngram']) > 1:
				enabled_options.append("%d-gram, " % int(self.configuration['ngram']))
			enabled_options.append("%d Folds" % int(self.configuration['folds_count']))
			conf_str = "%s [%s ]" % (classifier_str, "".join(enabled_options))
			return conf_str

	# Returns a list (array) of our fold numbers
	def get_folds(self):
		folds = [i for i in range(1,int(self.configuration['folds_count'])+1)]
		return folds

	# Return a list of our fold numbers, except f
	def get_all_folds_but(self,fold=1):
		if fold > int(self.configuration['folds_count']):
			raise Exception
		folds = self.get_folds()
		return  folds[0:fold-1]+folds[fold:len(folds)+1]	

