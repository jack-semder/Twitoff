from os import getenv
import tweepy
import spacy
from .models import DB, Tweet, User


# Get our API keys from environment variables
key = getenv('TWITTER_API_KEY')
secret = getenv('TWITTER_API_KEY_SECRET')


# Connect to twitter API
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)


nlp = spacy.load('my_model')  # might need 'my_model/'


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_or_update_user(username):
    twitter_user = TWITTER.get_user(screen_name=username)

    # Does this user exist in our DB already?
    db_user = User.query.get(twitter_user.id)
    if db_user is None:
        db_user = User(id=twitter_user.id, username=username)
    
    # Get users' tweets
    tweets = twitter_user.timeline(
        count=200,
        exclude_replies=True,
        include_rts=False,
        tweet_mode='extended'
    )

    # Add each tweet to DB
    for tweet in tweets:
        tweet_vector = vectorize_tweet(tweet.full_text)
        db_tweet = Tweet(
            id=tweet.id, 
            text=tweet.full_text[:300],
            vect=tweet_vector
        )
        db_user.tweets.append(db_tweet)  # link this tweet to user
        DB.session.add(db_tweet)


    # Add user to DB 
    DB.session.add(db_user)

    # Save changes to DB
    DB.session.commit()

    # exception handling
    try:
        pass # some code
    except Exception:
        pass # run this code if exception occured