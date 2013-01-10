Things to be done
-----------------

- [ ]   We need to de-couple the dataset from the classifiers
        We can follow scikit's dataset.target and dataset.data approach
        This will make it easier for MI to deal with data before classification

- [x]   Best way, is to implement the dataset as a Vector Space, 
        since this is an IR Library.

        * Vector Space will look like scikit's dataset. [see above]
        * Function to convert ot TF and/or IDF each document, or all.
        * Let's offer a way to serialize new queries, 
          however, no need to put queries in a Vector Space as we do now.

- [ ]   We need add pruning and MI (Mutual Information) again to our code
        Use it to skip columns from the VSM as well.

- [x]   We need to add basic TF-IDF search capabilities to our Vecotr Space.
        Both Euclidean and Cosine distances should be added here.

- [ ]   We need a way to dump VSM into file (pickle) and read it back
        Do padding automatically if not done before comparisons or tf.idf

- [ ]   Add statistics to VSM, ie. most frequent terms, histograms, etc.
        We probably add special class for that, MI can go here too.

- [ ]   We need to implement Ye's shapelet classifier.
        Probably implement it as standalone, not here in irlib.
