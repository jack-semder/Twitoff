import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet


def predict_user(user0_name, user1_name, hypo_tweet_text):
    # Grabbing both users from DB
    user0 = User.query.filter(User.username == user0_name).one()
    user1 = User.query.filter(User.username == user1_name).one()

    # Grab tweet vectors for both users
    user0_vectors = np.array([tweet.vect for tweet in user0.tweets])
    user1_vectors = np.array([tweet.vect for tweet in user1.tweets])

    # Does some model stuff
    vectors = np.vstack([user0_vectors, user1_vectors])
    labels = np.concatenate([
        np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))
    ])

    log_reg = LogisticRegression().fit(vectors, labels)

    # vectorize hypothetical tweet
    hypo_tweet_vector = vectorize_tweet(hypo_tweet_text)
    
    return log_reg.predict(hypo_tweet_vector.reshape(1, -1))[0]