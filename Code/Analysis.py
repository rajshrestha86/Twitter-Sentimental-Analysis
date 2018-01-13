import re
import tweepy
from textblob import TextBlob
from tweepy import OAuthHandler

class TwitterClient(object):
    """
        Twitter String Setiment Analysis
    """
    def __init__(self):
        _consumer_key="JxBXYqQYuGd5gQODWXpcg9NMN"
        _consumer_secret="l0oMDNtbJ8YcTz3BqyBfYqg8bDFMS19WDIaQbm7UomYQBpwYwJ"
        _access_token="952162333496758273-oN14hur5kx3ZMom0JPu2KNVxSUdG0Sf"
        _access_token_secret="OViw4ObGdvAVUqgetYNnTiB0bUvzkQJ8nRFLnKHgmOFlI"

#       Authorization in API server.
        try:
            # Creating a OAuthHandler Object
            self.auth=OAuthHandler(_consumer_key, _consumer_secret)
            # Set Access Token and Secret
            self.auth.set_access_token(_access_token, _access_token_secret)
            # Create Tweepy API object to fetch tweets
            self.api=tweepy.API(self.auth)

        except:
            print("Error: Authentication Failed")


    def tweet_process(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w +:\ / \ / \S +)", " ", tweet).split())


    def get_sentiment(self, tweet):
        # Find sentiment of a tweet
        predict=TextBlob(tweet)

        if predict.sentiment.polarity>0:
            return 'Positive'
        elif predict.sentiment.polarity==0:
            return 'Neutral'
        else:
            return 'Negative'

    def get_tweets(self, query, _count=10):
        tweets=[]
        # Fetch Tweets
        try:
            # call twitter api to fetch tweets
            print(query)
            downloaded_tweets=self.api.search(q=query, count=_count)
            for tweet in downloaded_tweets:
                # Tweet Data
                res_tweet={}
                res_tweet['text']=tweet.text
                res_tweet['sentiment']=self.get_sentiment(self.tweet_process(tweet.text))

            #     Append result
                if tweet.retweet_count>0:
                    # Check duplicate results for tweets
                    if res_tweet not in tweets:
                        tweets.append(res_tweet)
                else:
                    tweets.append(res_tweet)

            return tweets

            #
        except tweepy.TweepError as e:
            print("Error has occured. "+str(e))




    def test(self):
        print("Test successful")


def main():
    t=TwitterClient()
    get=input("Please enter the keyword to get latest tweets: ")
    count=input("How many tweets do you want? ")
    latest_tweets=t.get_tweets(query=get, _count=count)


    # picking positive tweets from tweets
    ptweets = [tweet for tweet in latest_tweets if tweet['sentiment'] == 'Positive']
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in latest_tweets if tweet['sentiment'] == 'Negative']
    # picking negative tweets from tweets
    neutraltweets = [tweet for tweet in latest_tweets if tweet['sentiment'] == 'Neutral']

    print("Total number of tweets: ", count)
    print("Number of positive tweets: ", len(ptweets))
    print("Number of Negative tweets: ", len(ntweets))
    print("Number of Neutral: ", len(neutraltweets))
    print('\n')
    print("Displaying all the tweets.")

    for tweet in latest_tweets:
        print('Tweet: '+tweet['text'])
        print('Sentiment: '+tweet['sentiment'])



if __name__=='__main__':
    main()