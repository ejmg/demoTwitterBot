"""
this is a demonstration bot for the tutorial on Ageof.Info. It demonstrates
some of the things possible with the Tweepy module, such as pagination

author: elias garcia
version: 28.12.16
"""

from secret import ACCESS_SECRET, ACCESS_TOKEN, CONSUMER_KEY, CONSUMER_SECRET
import tweepy as ty
import random


def setTwitterAuth():
    """
    obtains authorization from twitter API
    """
    # sets the auth tokens for twitter using tweepy
    auth = ty.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = ty.API(auth)
    return api


def tweetHelloWorld(api):
    """
    this method tweets hello world to twitter with your bot, Hello World!
    """
    api.update_status("This is an automated tweet"
                      " using a bot! Hello, World! #{}"
                      .format(random.randint(0, 10000)))


def getTimeline(api, user):
    """
    this method gets the last 100 tweets from the user's timeline. This returns
    a list of tweet objects, check Twitter's docs to learn more about them.
    """
    tweets = api.user_timeline(user.screen_name, count=100)
    tweets = [tweet for tweet in tweets]
    # this will print out the FULL contents of the first tweet object in the
    # list. This is useful to see the data fields available to use for other
    # methods you may want to make.
    print(tweets[0])
    return tweets


def getLastTweet(api, user):
    api.update_status("My last tweet is as"
                      " follows...#{}".format(random.randint(0, 10000)))
    tweets = getTimeline(api, user)
    # take the tweets and remake the list with *only* their text values
    tweets = [tweet.text for tweet in tweets]

    # this print statement will put out the last 100 tweets if you want to see
    # see them. Remember, this one is text only and will be a lot less messy.
    # print(tweets)

    # try catch for various errors that are possible with the api.
    try:
        # should not be possible...but anywho
        if len(tweets) == 1:
            api.update_status("This shouldn't be possible...#{}!"
                              .format(random.randint(0, 10000)))
        else:
            tweet = tweets[0]
            # wait a minute...
            api.update_status(tweet[:14] + "...wait, my last tweet was about"
                              " tweeting my last tweet, do'oh! #{}".
                              format(random.randint(0, 10000)))
    except ty.RateLimitError:
        print("You've hit the API limit! Try your bot in about an hour.")
    except ty.TweepError as e:
        print("You've hit another error. This could be a lot of things, but "
              "I'll leave that to you to debug. The error is {}".format(e))


def searchTweet(api, searchTerm):
    """
    gets 100 search results of the string, search, and returns them as a list
    of tweet objects
    """
    # I use the Cursor method of tweepy to crawl through search results,
    # while simultaneously using list comprehension to make a standard list
    # of the results. Cursor is used for pulling large numbers of tweets
    # (think of thousands)
    searchResults = [status for status in ty.
                     Cursor(api.search, q=searchTerm).items(100)]
    return searchResults


def replyHelloWorld(api, searchResults):
    randomTweet = searchResults[random.randint(0, len(searchResults) - 1)]
    tweet = ("@{} This is a demo search for 'hello world' with a bot, hello"
             " world! #{}".format(randomTweet.user.screen_name,
                                  random.randint(0, 10000)))
    tweetID = randomTweet.id
    api.update_status(tweet, tweetID)


if __name__ == "__main__":
    # set up authorization with twitter via tweepy
    api = setTwitterAuth()
    # tweet hello world!
    tweetHelloWorld(api)

    # let's get the user object of your bot's account
    user = api.me()
    # let's print the user object so you can see the fields it has
    print(user)

    # here's your username! Notic how we accessed it?
    print(user.screen_name)
    # Now let's use some of those fields to see your following/followers
    api.update_status("I have {} followers and follow {} accounts! #{}"
                      .format(user.followers_count, user.friends_count,
                              random.randint(0, 10000)))

    # Now let's get the last tweet of yours...
    getTimeline(api, user)
    getLastTweet(api, user)

    # let's search for the literal "hello world" <-- notice how I escape the
    # quotes below. This will get me the terms with that specific string.
    searchResults = searchTweet(api, "\"Hello World \"")

    # lets tweet at one of the tweets we found with search
    replyHelloWorld(api, searchResults)
