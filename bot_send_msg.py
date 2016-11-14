#!/usr/bin/python
import praw
import pdb
import re
import os
from config_bot import *
from random import choice


# ------ WARNING: DO NOT SPAM.  If the bot hits more than 120 users in any hour, reddit will shut your bot down ----------



# Check that the file that contains our username exists
if not os.path.isfile("config_bot.py"):
    print "You must create a config file with your username and password."
    print "Please see config_skel.py"
    exit(1)

# Create the Reddit instance
user_agent = ("Gif Sender 0.2")
r = praw.Reddit(user_agent=user_agent)

# and login
r.login(REDDIT_USERNAME, REDDIT_PASS)


# Have we run this code before? If not, create an empty list
if not os.path.isfile("users_talked_to.txt"):
    users_talked_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("users_talked_to.txt", "r") as f:
        users_talked_to = f.read()
        users_talked_to = users_talked_to.split("\n")
        users_talked_to = filter(None, users_talked_to)


# Function: sends message to user un
# returns nothing
# Ex: sendNiceMessage("UsernameGoesHere")
def sendNiceMessage(un):
  cuteImgs = {
  "https://imgur.com/nBLMKLi": "gif of an happy otter",
  "http://i.imgur.com/bWufrLO.png": "bunny with a backpack",
  "http://i.imgur.com/i6ktwqw.gifv": "gif of a sleepy cat",
  "http://data.whicdn.com/images/173034984/large.jpg": "picture of a fluffy kitten"
  }

  imgUrl = choice(cuteImgs.keys())
  imgDesc = cuteImgs[imgUrl]
  mainMsg = "Hello! I saw you post and thought you're a cool person.  I have no reddit gold, but I hope you'll take this " + imgDesc + " as an acceptable substitute: \n" + imgUrl
  reqBotMsg = "\n Keep being awesome! \n ----------------- \n This is a bot.  You are the recipient of an automated message.  If you believe this message was sent to you in error, you're selling yourself short.  (If you have feedback, all replies are read by a human.)"

  r.send_message(un, "This Bot Thinks You're Awesome", mainMsg + reqBotMsg)
  print("I sent message to " + un)


# Function: finds users who posted top-level items in subreddit subName and calls sendNiceMessage on them
# returns nothing
# Ex: crawlSubreddit("askreddit")
def crawlSubreddit(subName):
  # Get the top 20 values from our subreddit
  subreddit = r.get_subreddit(subName)
  for submission in subreddit.get_hot(limit=20):
      try:
        user = submission.author.name
        # If we haven't sent to user
        if (user not in users_talked_to):
          sendNiceMessage(user)

            # Store the current user into our list
          users_talked_to.append(user)
      except Exception as e: print(e)


# Function: finds users who commented in threads containing threadKeyword in subreddit subName and calls sendNiceMessage on them
# returns nothing
# Ex: crawlThread("femalefashionadvice", "random fashion thoughts - november 09")
# Ex: crawlThread("trollxchromosomes", "trump")
def crawlThread(subName, threadKeyword):
  # Get the top 20 values from our subreddit
  subreddit = r.get_subreddit(subName)
  threadKeyword = threadKeyword.lower()

  for submission in subreddit.get_hot(limit=20):
      # Only crawl threads with threadKeyword
      if re.search(threadKeyword, submission.title, re.IGNORECASE):
        flat_comments = praw.helpers.flatten_tree(submission.comments)

        for comment in flat_comments:
          try:
            if (not (comment is None)) and (not (comment.author is None)):
              user = comment.author.name
              # If we haven't sent to user before
              if (user not in users_talked_to):
                sendNiceMessage(user)

                # Store the current user into our list
                users_talked_to.append(user)

          except Exception as e: print(e)

# Function: finds every user who commented in the top numSubmissions in subreddit subName
# params: numSubmissions is an int between 0 and 10
# returns nothing
# deepCrawlSubreddit("actuallesbians", 20)
def deepCrawlSubreddit(subName, numSubmissions):
  # Get the top 5 values from our subreddit
  subreddit = r.get_subreddit(subName)
  for submission in subreddit.get_hot(limit=numSubmissions):
      if not submission.author.name == "AutoModerator":

        flat_comments = praw.helpers.flatten_tree(submission.comments)

        for comment in flat_comments:
          try:
            if (not (comment is None)) and (not (comment.author is None)):
              # print submission.title
              user = comment.author.name
              # If we haven't replied to this post before
              if (user not in users_talked_to):
                sendNiceMessage(user)

                # Store the current id into our list
                users_talked_to.append(user)

          except Exception as e: print(e)


# WARNING: DO NOT SPAM.  If the bot hits more than 120 users in an hour, reddit will shut your bot down
# Recommended that you check out the threads in the sub before sending the bot in, to reduce likelihood of spam
# deepCrawlSubreddit most likely to get you in trouble here


# Call your functions here!

#crawlThread("femalefashionadvice", "random fashion thoughts - november 09")
#deepCrawlSubreddit("actuallesbians", 20)
#crawlThread("trollxchromosomes", "because it liked one of my")



# Write our updated list back to the file
with open("users_talked_to.txt", "w") as f:
    for user in users_talked_to:
        f.write(user + "\n")
