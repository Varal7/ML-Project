# Milestone 3

In this project, we are interested in performing location inference based on a user's tweets and interactions with other users.  

## Software infrastucture

We will use python for the data cleaning, data preprocessing, and feature extraction.

For baseline models, i.e., Logistic Regression and SVM, we will use the implementation of Multi-core LIBLINEAR. (Scikit-learn does not support multi-core training, and might be very slow on huge datasets. However, we might still use it for data preprocessing and evaluation.)

For content-based methods (probabilistic model) and network-based method (label propagation), we plan to implement from scratch.

For conditional random fields, we plan to utilize the code from Tsinghua University Knowledge Engineering Group. The challenge is how to learn CRF efficiently in large networks. We will explore sampling based learning algorithms, and the code will be implemented from scratch.

We will also try deep learning models. Specifically, we will be using PyTorch.


## Work Division

Victor Quach will work on baselines, content-based methods and network-based methods.

Yujie Qian will work on CRF and sampling based learning algorithms.

Yujia Bao will work on deep learning models, and evalutation.

We will collaborate in the experiments, and writing the report.
