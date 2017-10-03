# Milestone 1

In this project, we will be interested in predicting a user's location based on the footprint he leaves on social media. 
More precisely, we leverage Twitter data to perform this task: both the content of the tweets he posts and his interactions with other users.

## Dataset
We will use publicly availabe twitter data from [UIUC](https://wiki.illinois.edu/wiki/display/forward/Dataset-UDI-TwitterCrawl-Aug2012). 
It contains 3 million users profiles, 50 million tweets for 140 thousand users and 200 million users following relationships.

## Preprocessing

Since the location information in the users' profiles is noisy, we need to preprocess the dataset (for instance, remove user whose the location is "Neverland").
Also, predicting countries seems to be easier, since the timezone information is a very discriminative feature.
Thus, we will, restrain to American tweets and try to predict the State of the users.
We will perform the following preprocessing steps:
1. We include users whose registered locations are in the form of "cityName, stateName" and "cityName, stateAbbreviation", where we considered all cities listed in the Census 2000 U.S. Gazetteer.
2. We exclude users who have fewer than 10 tweets in the dataset.
3. We tokenize the tweet content into words.

## Plan
1. The first step is to predict location based on tweet content and user profile. In specific, we extract content features using the bag-of-words model, as well as other statistical features such as tweeting time distribution. Then we use different classification models (logistic regression, SVM, etc.) to predict the location.
2. The second step is to use the social network between users for prediction. The idea is to infer a user's location from his/her friends' locations. We can utilize methods such as label propagation.
3. The third step is to study combining user features (including content) and social network for location prediction. We plan to formalize the task as a graph-based semi-supervised learning problem, and use a graphical model to solve it. The challenge is how to train the model efficiently on large-scale graphs.
