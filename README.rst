Information Retrieval Library 
=============================

I started writing this library as part of my `Information Retrieval and Natural Language Processing (IR and NLP) <http://www.uea.ac.uk/study/module/mod-detail/CMPSMB29>`_ module in the `University of East Anglia <http://www.uea.ac.uk/>`_. It was mainly meant to detect Review Spam (Machine Learning - Classification). However, It has more functionalities such as `Vector Space Model (VSM) <http://en.wikipedia.org/wiki/Vector_space_model>`_, as well as some other IR functions such as tokenizing, n-grams, stemming and PoS (Part of Speech) tagging.

Installation
-------------

You sure need to have Python installed on your computer.

Another **optional** module might be needed, `NLTK <http://nltk.org/>`_ 
This is only needed in case of stemming and PoS (part of speech) tagging 

To install the package, write::

    python setup.py install


Code Organization
-----------------

First of all, the code is divided into the following main components:

#. matrix.py
#. metrics.py
#. classifier.py
#. preprocessor.py
#. configuration.py
#. superlist.py

matrix.py: This is where documents (vecotor space) index is implemented.

metrics.py: Distance measures (cosine and euclidean distance).

classifier.py: The following classifiers are implemented here:

* Rocchio: Rocchio Classifier 
* KNN: k-NN Classifier
* Bayes: Naive Bayes Classifier
 
The above 3 classes (class as in object oriented programming not machine learning), are inherited from 'Index'
One more class here is 'Evaluation', which is used to calculate accuracy during testing.

preprocessor.py is the module where files parsing tokenizing, stemming and PoS tagging are implemented
More feature selection algorithms (such as Mutual Information Gain), should be implemented here.
 
How to use for Vector Space IR
-------------------------------

The main modules to use here are matrix.py and metrics.py,
however you might find the preprocessor.py useful too::

    # Load the three modules:
    from irlib.preprocessor import Preprocessor
    from irlib.matrix import Matrix
    from irlib.metrics import Metrics
  
    # Create instances for their classes:
    prep = Preprocessor()
    mx = Matrix()
    metric = Metrics()

For simplicity, let's assume you have a single text file tweets.txt,
And each line represent a seperate tweet (document).

We will read the file, line after the other, 
and then use the preprocessor to tokenize the line into words.
There are more options for the ngram_tokenizer, such as producing bigrams,
converting tokens into lower space, stemming and converting to PoS.
However, we will stick to the default options for now.
Then we will load the document into our VSM, aka Matrix. 
More on the frequency and do_padding options later on:: 

    fd = open('tweets.txt','r')
    for line in fd.readlines(): 
        terms = prep.ngram_tokenizer(text=line)
        mx.add_doc( doc_id='some-unique-identifier', 
                    doc_terms=terms, 
                    frequency=True, 
                    do_padding=True)
        
Now, we are done with loading our documents, let someone search for a tweet::

    q = raw_input("Enter query to search for a tweet: ")

Again, we can use the preprocessor to tokenize the query.
We also need to align the terms used in the query with ones read from ducuments,
i.e. we need them both to be put in equal length lists and ignore terms in query
not seen before when reading the documents::

    terms = prep.ngram_tokenizer(text=q)
    q_vector = query_to_vector(terms, frequency=False)

Finally, to get the best matching document to our query, 
we can loop on all documents in the Matrix and find the one with least distance.
We will just show the looping here, you can easily compare distances, 
and sort documents according to their relevance if you want to:: 

    for doc in self.mx.docs:
        distance = metric.euclid_vectors(doc['terms'], q_vector)

We are done for now, but before moving to the next section let me discuss 
the following:

The add_doc() method in Matrix has two more options we skipped earlier:
    
* frequency:: 

    If True, then we are using a multinomial mode (You usually will need this) 
    i.e. if terms occurs n times in document, then it frequency is n.
    If False, then we are using a multivariate (Bernoulli) mode, 
    i.e. if terms occurs in document at least one time, then it frequency is 1        
    otherwise its frequency is zero.
    As mentioned above, you will normally need the multinomial mode,
    We just put the Bernoulli mode for the sake of Naive Bayesian Classifier
    
* do_padding::

    Each time we add new document, we also see new terms, 
    hence if terms represent columns in our matrix and documents represent rows,
    we might end with new rows of bigger length than order rows.
    So, padding here is to align the length of older rows with newer ones.
    So you either set this to True with each new document, 
    or call mx.do_padding() when done.

Wait a minute, two more notes:    

* We haven't converted our VSM into tf.idf in the previous example, 
however, you normally need to do so. So you have to call the follwing method, 
right after loading your documents and before doing searches::

    mx.tf_idf()

We have used the Euclidean distance in our example, yet you may need to use 
cosine distance instead, so, here is the method for that::

    metric.cos_vectors() 


How to use for classification
------------------------------

Your code should does the following

* Reading and parseing the configuration file::

	# You first need to import the configuration class
	from irlib.configuration import Configuration 

	# Then you load configuration
	# Sample configuration file in the root directory: sample.conf
	config = Configuration(config_file='your_file.conf')
	config.load_configuration()
 
* Initiate the preprocessors::

	# You first need to import the configuration class
	from irlib.preprocessor import Preprocessor

	# Then you create a new preprocessor object
	# prep = Preprocessor(pattern='\W+', lower=True, stem=False, pos=False, ngram=2)

	# However, you normally get the values from the confiuration
	config_data = config.get_configuration()
	prep = Preprocessor(pattern='\W+', lower=config_data['lower'], stem=config_data['stem'], 
						pos=config_data['pos'], config_data['ngram'])

* Initiate your evaluation module::
	
	# You first need to import this
	from irlib.classifier import Evaluation 

	# You give it the configuration class object, see above
	# For now, you can safely set fold = 0

	# This is used for cross-testing, 
	# to keep track which part of dataset is being used for testing at the moment
	ev = Evaluation(config=config, fold=myfold)

* Select and initiate the desired Classifier [Rocchio, KNN or Naive Bayes]::

	# Once more don't forget to import your desired classe(s)
	#from irlib.classifier import Rocchio  
	#from irlib.classifier import KNN 
	from irlib.classifier import NaiveBayes 
	
	# VERBOSE = True or False
	# Fold, see above for more details
	# Objects for both configuration and evaluation classes
	ml = NaiveBayes(verbose=VERBOSE, fold=myfold, config=config, ev=ev)

* Training::

	# Read your files one after the other (example fd = open('file1.txt', 'r'))
	# You may use our preprocessor for tokenizing data got from fd.read()
	terms = prep.ngram_tokenizer(text=file_data)

	# Then add document to your classifier
	# doc_id: you can call it anything you want
	# You should tell the classifier which class the doc belongs to
	# This should be the same as ones mentioned in configuration file
	ml.add_doc(doc_id = doc_id, doc_class=class_name, doc_terms=terms)

* Some house keeping::

	# You shall first call do padding to align and tide read data
	ml.do_padding()

	# Then you should do the actual learning from training data
	ml.calculate_training_data()

	# This one is optional, in case you need more details to be printed 
	ml.diagnose()

* Testing::

	# Just as in training, you can use the preprocessor
	terms = prep.ngram_tokenizer(text=file_data)

	# Then add the document, we call them queries this time, notice function name
	ml.add_query(query_id = doc_id, query_class=class_name, query_terms=terms)	

* Get Evaluation results::

	# Remember the evaluation class we created earlier
	# Now we can call it to tell us some nice results
	results = ev.calculate(review_spam=True, k=k)

* If we are doing cross checking here, the previous 4 steps are repeated for all folds 

Contacts
--------
 
+ Name: Tarek Amr 
+ Twitter: @gr33ndata




