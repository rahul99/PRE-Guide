# PRE-Guide
Personalized Recommendation Engine: Guided by Behavior

## Summary
Recommendation Engine application guided by behavior. The behavior of the person is inferred using his/her temporal activites in the Social Media platforms such as Facebook/Twitter/linkedIn. In the inference phase, the social media activity of the user is recorded and a trained topic model predicts the topic that a user has been talking about or is showing interest in. This behavior can be used as a guide to recommend products to the user. Within the scope of this project, we show a prototype to demonstrate book recommendation based on Social behavior.
In the offline phase, we train topic-models to predict the behavior of the person and export these models for evaluation. The models can re-trained and updated periodically.

## Backend
[1] We work on [Twitter 20 Newsgroups Dataset](https://archive.ics.uci.edu/ml/datasets/Twenty+Newsgroups) to do topic-modelling. Specifically, Given several tweets of a user in a particular time window, we predict the probability of a topic in each tweet and pick the top-k categories on a ranked list.

[2] We work on [Goodbooks-10k Dataset](http://fastml.com/goodbooks-10k-a-new-dataset-for-book-recommendations/) to find out find out the ranked list of books in each category.

[3] A mapping is required to create between categories in [1] and [2].

[4] Optional: If needed, we can use [Book Dataset](https://github.com/uchidalab/book-dataset/tree/master/Task2), that contains a huge collection of book names in each category

## Frontend
[1] A web server will be setup, that takes in input as the username of the person. 

[2] We query this username in the Twitter API and crawl the last K tweets of this person as a list of JSON objects.

[3] This list is sent to backend where recommendation computations happen as follows:

  [a] Collect the JSON list, parse it and create a sequence of feature vectors, one for each json
  
  [b] Predict a topic for each feature vector. Add the probabilities and create a cumulative list of top-k categories.
  
  [c] Query a top recommended book in each category and create a list of this category.
    
[4] The client API collects this list and displays in the browser in the order.

