# Information Retrieval Library #

Writing this library was part of my Information Retrieval assignment in University of East Anglia.
It was mainly meant to detect Review Spam (Machine Learning - Classification).
However, I tried to make the code as generic as possible to be used for other classification problems.
I also added some other IR functions such as tokenizing, n-grams, stemming and part of speech tagging 

## Installation ##

You sure need to have Python installed on your computer.

Another *optional* module might be needed, [NLTK](http://nltk.org/) 
This is only needed in case of stemming and PoS (part of speech) tagging 

## Code Organization ##

First of all, the code is divided into 3 main components:

1. classifier.py
2. configuration.py
3. preprocessor.py

classifier.py is the main module where the following classifiers are implemented:

+ Rocchio: Rocchio Classifier 
+ KNN: k-NN Classifier
+ Bayes: Naive Bayes Classifier
 
The above 3 classes (class as in object oriented programming not machine learning), are inherited from 'Index'
One more class here is 'Evaluation', which is used to calculate accuracy during testing.

preprocessor.py is the module where files parsing tokenizing, stemming and PoS tagging are implemented
If we have time to add feature selection (such as Mutual Information Gain), it should be implemented here.
 
## How to use ##

Your code should does the following

+ Read and parse the configuration file

	> You first need to import the configuration class

	from irlib.configuration import Configuration 

	> Then you load configuration

	> Sample configuration file in the root directory: sample.conf

	config = Configuration(config_file='your_file.conf')

	config.load_configuration()
 
+ Initiate the preprocessors

	> You first need to import the configuration class

	from irlib.preprocessor import Preprocessor

	> Then you create a new preprocessor object

	> prep = Preprocessor(pattern='\W+', lower=True, stem=False, pos=False, ngram=2)

	> However, you normally get the values from the confiuration

	config_data = config.get_configuration()

	prep = Preprocessor(pattern='\W+', lower=config_data['lower'], stem=config_data['stem'], 
						pos=config_data['pos'], config_data['ngram'])

+ Initiate your evaluation module
	
	> You first need to import this

	from irlib.classifier import Evaluation 

	> You give it the configuration class object, see above

	> For now, you can safely set fold = 0

	> This is used for cross-testing, 
	> to keep track which part of dataset is being used for testing at the moment

	ev = Evaluation(config=config, fold=myfold)

+ Select and initiate the desired Classifier [Rocchio, KNN or Naive Bayes]

	> Once more don't forget to import your desired classe(s)
	
	>from irlib.classifier import Rocchio  
	
	>from irlib.classifier import KNN 
	
	from irlib.classifier import NaiveBayes 
	
	> VERBOSE = True or False
	
	> Fold, see above for more details
	
	> Objects for both configuration and evaluation classes
	
	ml = NaiveBayes(verbose=VERBOSE, fold=myfold, config=config, ev=ev)

+ Training 

	> Read your files one after the other (example fd = open('file1.txt', 'r'))

	> You may use our preprocessor for tokenizing data got from fd.read()

	terms = prep.ngram_tokenizer(text=file_data)

	> Then add document to your classifier

	> doc_id: you can call it anything you want

	> You should tell the classifier which class the doc belongs to

	> This should be the same as ones mentioned in configuration file
 
	ml.add_doc(doc_id = doc_id, doc_class=class_name, doc_terms=terms)

+ Some house keeping

	> You shall first call do padding to align and tide read data

	ml.do_padding()

	> Then you should do the actual learning from training data

	ml.calculate_training_data()

	> This one is optional, in case you need more details to be printed 

	ml.diagnose()

+ Testing

	> Just as in training, you can use the preprocessor

	terms = prep.ngram_tokenizer(text=file_data)

	> Then add the document, we call them queries this time, notice function name

	ml.add_query(query_id = doc_id, query_class=class_name, query_terms=terms)	

+ Get Evaluation results

	> Remember the evaluation class we created earlier
	
	> Now we can call it to tell us some nice results

	results = ev.calculate(review_spam=True, k=k)

+ If we are doing cross checking here, the previous 4 steps are repeated for all folds 

## Contacts ##
 
+ Name: Tarek Amr 
+ Twitter: @gr33ndata


