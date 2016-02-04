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
    q_vector = mx.query_to_vector(terms, frequency=False)

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

Pruning your matrix
--------------------

You might need to remove terms with frequency lower that some threshold.
After loading your documents into the matrix, you can prune it using the following steps

* Calculate the frequencies for terms, using freq_levels(), it takes a pruning threshild and returns two lists:

    1. prune_map: list of 0's and 1's, a 0 means remove this term, and 1 means keep it. In same order as list returned by vocabulary()
    2. freq_map: This is the acutua frequencies each term. In same order as list returned by vocabulary()
    
* Here is an example::
    
    prune_map, freq_map = mx.freq_levels(threshold=3)

* After that, to do the actual pruning pass the prune_map variable to prune()::

    mx.prune(prune_map, show_progress=True)
    
Save matrix to file
--------------------

You can save matrix to a file, either for loading it later on, or to use it with a different machine learning software.
Supported file types are CSV (both comma or tab seperated) and ARFF (for using it with `Weka <http://www.cs.waikato.ac.nz/ml/weka/>`_) 

* To dump data into a CSV file::

    mx.dump('filename.csv', delimiter='\t', header=True)
    
* To dump it into ARFF file::

    mx.dump_arff('filename.arff', clstype='{1,2}')
    
* Notice that class labels in Weka are normally the last item in your featureset. Their type is normally set to 'Nominal attributes'. Hence, if for example you have 3 class labels A, B and C, you then should set clstype='{A,B,C}'. Recall that while reading your documents and adding them to the matrix using add_doc(), you can actaully set class labels there as follows::

    mx.add_doc(doc_id = '42', doc_class='A', doc_terms=['the', 'apple', 'was', 'on', 'the', 'tree'])

Load matrix from file
----------------------

If you have your matric saved into a CSV/TSV file, you can load it from there in the future. 

* To load data from a CSV file::

    mx = Matrix()
    mx.load('filename.csv', delimiter='\t')

We ignore black lists and white lists in this case, since we assume data was filtered before it being dumped in the first place. 

Now you can deal with the matrix, just like the ones you built from scratch using add_doc() earlier. 

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

The n-Gram Language Model
--------------------------

The n-Gram Language Model (LM) is implemented in lm.py

In the following example we are going to implement a character-based LM. 

* We will start by importing the LM class, as well as the Preprocessor so that we can convert our docs into characters::

    from irlib.lm import LM 
    from irlib.preprocessor import Preprocessor 
    
* To initialize our Language Model::

    # n: The order of the ngram LM, e.g. for bigram LM, n=2
    # smoothing: Use 'Laplace', aka Add One Smoothing
    # laplace_gama: Multiply 1 & V by this factor gamma, i.e. Add Half instead of One
    lm = LM(n=2, verbose=True, smoothing='Laplace', laplace_gama=0.5) 
    
* Add documents in a similar fashion to that of the Matrix. We use p.term2ch() to convert strings into list of characters.::

    lm.add_doc(doc_id='apple', doc_terms=p.term2ch('the tree is full or apples'))
    lm.add_doc(doc_id='orange', doc_terms=p.term2ch('orange orange juice'))

* For a new query, 'orango juice', we can use the following command to see which doc_id it is more likely being a member of.::

    result = lm.calculate(doc_terms=p.term2ch('orango juice'))
    
* The result form lm.calculate() is a dictionary with the following fileds::

    # prob: calculated probability of query being member of a document.
            Or more precisely, we calculate the conditional probabilities
            of all doc_id's given the query terms, Pr(doc_id/doc_terms).
            The doc_id giving us the highest probability is returned as calc_id.
    # calc_id: This is what we need to check. 
               The id of document in the training data, 
               where the query is more likely to be a member of.
    # actual_id: If toy know the doc_id a query beforehand, 
                 then you can pass it to lm.calculate(),
                 and it will be returned back into this filed.
                 This is useful for caliberation and testing. 
    # seen_unseen_count: Counts for seen/unseen terms in training data  

Contribution
-------------

To contribute to *irlib*, first create an account on `github <http://github.com/>`_. Once this is done, fork the `irlib repository <http://github.com/gr33ndata/irlib>`_ to have you own repository,
clone it using 'git clone' on the computers where you want to work. Make
your changes in your clone, push them to your github account, test them
on several computer, and when you are happy with them, send a pull
request to the main repository.

Testing
--------

Normally, you can run test using make command as follows::

    $ make test

However, if you want to run the underlying python code, then type:

    $ python test.py     
      
Contacts
--------
 
+ Name: `Tarek Amr <http://tarekamr.appspot.com/>`_
+ Twitter: `@gr33ndata <https://twitter.com/gr33ndata>`_

