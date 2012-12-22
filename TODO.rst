Things to be done
-----------------

#.  We need to de-couple the dataset from the classifiers
    We can follow scikit's dataset.target and dataset.data approach
    This will make it easier for MI to deal with data before classification

#.  Best way, is to implement the dataset as a Vector Space, 
    since this is an IR Library.

    * Vector Space will look like scikit's dataset. [see above]
    * Function to TF/IDF each row, or the whole document.
    * Let's offer a way to serialize new queries, 
      however, no need to put queries in a Vector Space as we do now.

#.  We need add pruning and MI again to our code

#.  We need to add basic TF-IDF search capabilities to our Vecotr Space.
    Both Euclidean and Cosine distances should be added here.

#.  After decoupling dataset from classifier, we need utilities
    to convert textual data (files) to our dataset

#.  We need to implement Ye's shapelet classifier
