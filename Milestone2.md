# Milestone 2

In this project, we are interested in performing location inference based on a user's tweets and interactions with other users.  

We will consider the realistic semi-supervised scenario where a portion of user locations are known.  
More precisely, we are given an oriented graph where the vertices are the users and an edge goes from A to B if A mentions B in a tweet or if A follows B.
All the vertices also carry user-dependent information (such as the content of his tweets).
Some of the vertices are labeled with the user's location.  
Given this partially labeled network, the goal is then to retrieve the missing labels.

## Model evaluation

In order to evaluate our models, we will keep from our dataset only the users whose location we know.  
These users will be split into a training set, a validation set, and a testing set: 

The evaluation consists in comparing the predicted labels of the testing set with respect to the ground truth.  
We will use evaluation metrics for multi-class classification problems, such as accuracy.  

From this evaluation, we hope to discover a trend in the mistakes that our model makes and be able to iterate over its design.

## Model design

Our first model will disregard the edges information (relationships between users) and only consider the content of the tweets to infer their location.
Our hope is that the use of certain words or phrases are already a discriminative feature of a person's location (i.e. refering to the landmarks or using local idioms).  
To test this hypothesis, we will apply logistic regression and SVM on hand-crafted features.  

Then, we will explore different methods to leverage the network information, such as label propagation or conditional random fields.  

As the machine learning class progresses, we hope to get a better overview of the methods that could be relevant for our project.

## References

Z. Cheng, J. Caverlee, and K. Lee. [You are where you tweet: a content-based approach to geo-locating twitter users](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.230.1907&rep=rep1&type=pdf).

L. Backstrom, E. Sun, and C. Marlow. [Find me if you can: improving geographical prediction with social and spatial proximity](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.191.901&rep=rep1&type=pdf).

A. Zubiaga, A. Voss, R. Procter, M. Liakata, B. Wang, A. Tsakalidis. [Towards real-time, country-level location classification of worldwide tweets](https://arxiv.org/pdf/1604.07236.pdf). 

