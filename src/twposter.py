import tweepy
import os


# Posting media & text on Twitter


# IMPORTANTE Get these keys from https://developer.twitter.com/
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# Validate the keys in order to use the API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def tweet_text(text):
    # Tweeting text only
    try:
        response = api.update_status(status=text)
        print("Tweeted: {}".format(response._json["text"]))
    except Exception as e:
        print("Error: {}".format(e))


def tweet_media(text, folder, name):
    # Tweeting media and text
    media_path = os.path.join(folder, name)
    try:
        response = api.update_with_media(media_path, text)
        print("Tweeted: {}".format(response._json["text"]))
    except Exception as e:
        print("Error: {}".format(e))


def tweets_hour(n):
    # Returns time in seconds between channel checking
    seconds = 3600 / n
    return seconds


if __name__ == "__main__":
    print("This is not main!")
