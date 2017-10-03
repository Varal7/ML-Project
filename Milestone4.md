# Milestone 4

In this project, we are interested in performing location inference based on a user's tweets and interactions with other users.  

## Preprocessing

1. We only included users whose registered locations are in the form of "cityName, stateName" and "cityName, stateAbbreviation", where we considered all cities listed in the Census 2000 U.S. Gazetteer.
2. We exclude users who have fewer than 10 tweets in the dataset.
3. We tokenize the tweet content into words.


## Feature engineering - content-based approach

Our first idea was to use a bag-of-words model but that led to a very sparse representation and all the problems with high dimensionality.  

Instead, we use Mutual Information [1].
Using the trainig set, we compute for a given word ``w`` and a given location ``l``:

```math
MI(w,l) = log \frac{n count(w,l)}{count(w)count(l)}
```

Then, for a given user, we aggregate these values using both the average and the maximum value (over all the words used in all of his tweets).

## Model - content-based approach

As a baseline, we implement Logistic Regression and SVM using Python and the Multi-core LIBLINEAR library.

## Evaluation 

We evaluate our predictions through:

- Accuracy: checks whether our prediction is correct
- Accuracy@3: checks whether the correct prediction is among our top-3 predicted locations
- Distance error (mean and median): the distance between our prediction and the correct location (in kilometers)

## Results - content-based approach


### Logistic Regression

```
Acc: 0.4812
Acc@3: 0.6732
Mean error distance: 709.17
Median error distance: 247.80
```

### SVM
```
Acc: 0.4783
Acc@3: 0.6742
Mean error distance: 715.21
Median error distance: 251.67
```

## References

[1] Cover, T.M.; Thomas, J.A. (1991). Elements of Information Theory (Wiley ed.) 
