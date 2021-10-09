from time import sleep
from praw import Reddit
from os import environ
from random import randint
from datetime import datetime

def InitPraw():
  return Reddit(
    client_id = environ['CLIENT_ID'],
    client_secret = environ['CLIENT_SECRET'],
    user_agent="console:doctor-who-bot:v1.0.0 (by u/doctor-who-bot)",
    username = "doctor-who-bot",
    password = environ['PASSWORD']
  )

def LoadQuotes():
  quotes = []
  file = open('quotes.txt', 'r')
  for line in file:
    quotes.append(line)
  file.close()
  return quotes

def AlreadyReplied(replies):
  for reply in replies:
    if reply.author == "doctor-who-bot":
      return True
  return False

def GetRandomPositionOfObject(object):
  return randint(0, len(object)-1)

def ReplyRandomQuote(comment):
  quotes = LoadQuotes()
  random_quote_position = GetRandomPositionOfObject(quotes)
  comment.reply(quotes[random_quote_position])
  return quotes[random_quote_position]

def StoreReply(comment, reply):
  amount_of_lines = 0
  with open("replies.txt", "r") as file_object:
    for line in file_object:
      amount_of_lines += 1
    file_object.close()
  with open("replies.txt", "a") as file_object:
    file_object.write("Reply #" + str(int(amount_of_lines/14 + 1)))
    file_object.write("\n")
    file_object.write(" Replied comment data:")
    file_object.write("\n")
    file_object.write("   Author: " + comment.author.name)
    file_object.write("\n")
    file_object.write("   Content: " + comment.body)
    file_object.write("\n")
    file_object.write("   Date & time (UTC): " + datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'))
    file_object.write("\n")
    file_object.write("   Link: " + comment.permalink)
    file_object.write("\n")
    file_object.write("   Post:")
    file_object.write("\n")
    file_object.write("     Title: " + comment.submission.title)
    file_object.write("\n")
    file_object.write("     Author: " + comment.submission.author.name)
    file_object.write("\n")
    file_object.write("     Date & time (UTC): " + datetime.utcfromtimestamp(comment.submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'))
    file_object.write("\n")
    file_object.write("     Link: " + comment.submission.permalink)
    file_object.write("\n")
    file_object.write(" Reply data:")
    file_object.write("\n")
    file_object.write("   Replied quote: " + reply)
    file_object.write("   Date & time (UTC-3): " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    file_object.write("\n")
    file_object.write("\n")


def CheckNewPosts(posts):
  for post in posts:
    for comment in post.comments:
      if hasattr(comment, "body"):
        if "doctor" in comment.body.lower():
          if not AlreadyReplied(comment.replies):
            quote_replied = ReplyRandomQuote(comment)
            StoreReply(comment, quote_replied)
            #sleep(300)


def RunBot():
  reddit_handler = InitPraw()
  doctor_who_subreddit_handler = reddit_handler.subreddit("doctorwho")
  CheckNewPosts(doctor_who_subreddit_handler.new(limit=25))

