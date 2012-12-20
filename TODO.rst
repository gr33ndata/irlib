Things to be done
-----------------

1. We need to de-couple the dataset from the classifiers
   We can follow scikit's dataset.target and dataset.data approach
   This will make it easier for MI to deal with data before classification

2. We need add pruning and MI again to our code

3. After decoupling dataset from classifier, we need utilities
   to convert textual data (files) to our dataset

4. We need to implement Ye's shapelet classifier
