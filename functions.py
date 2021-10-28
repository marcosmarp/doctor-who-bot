from datetime import datetime
from time import sleep
from praw import Reddit
from os import environ
import random
import pytz
from sys import stderr

commands = ['!doctor']

def log_error(message):
  print(message, file=stderr)
  print("---------------", file=stderr)

def init_praw():
  return Reddit(
    client_id = environ['CLIENT_ID'],
    client_secret = environ['CLIENT_SECRET'],
    user_agent="console:doctor-who-bot:v1.0.1 (by u/doctor-who-bot)",
    username = "doctor-who-bot",
    password = environ['PASSWORD']
  )

def post_have_comments(post):
  return (post.num_comments > 0)

def load_quotes():
  with open('quotes.txt', 'r', encoding='utf-8') as file:
    quotes = list(file)

  return quotes

def already_replied(replies):
    return any(reply.author == "doctor-who-bot" for reply in replies)

def reply_random_quote(comment):
  reply = """
  {0}

  ^(I'm a bot and this action was performed automatically)
  
  ^(Feedback? Bugs?: )[^(Github)](https://github.com/marcosmarp/doctor-who-bot)
  """
  reply = reply.format(random.choice(load_quotes()))
  comment.reply(reply)

def inform_reply_on_screen(comment):
  now = datetime.now(pytz.timezone('America/Argentina/Buenos_Aires'))
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
  print("           " + dt_string + ": replied " + comment.author.name + "'s comment", file=stderr)
  print("---------------", file=stderr)

def check_for_command(comment):
  for command in commands:
    if command in comment.body.lower():
      return True
  return False

def get_command(comment):
  for command in commands:
    if command in comment.body.lower():
      return command

def check_comments(comments):
  for comment in comments:
      if hasattr(comment, "replies"):
        check_comments(comment.replies)

      if not hasattr(comment, "body"):
        log_error("Empty comment")
        continue
      print("   Comment have body", file=stderr)

      if comment.author is None:
        log_error("Comment deleted")
        continue
      print("   Checking " + comment.author.name + "'s comment", file=stderr)

      if not check_for_command(comment):
        log_error("Comment doesn't mention a command'")
        continue
      command = get_command(comment)
      print("       Comment mentions " + command, file=stderr)

      if already_replied(comment.replies):
        log_error("Comment already replied")
        continue
      print("         Comment yet to be replied", file=stderr)

      reply_random_quote(comment)
      inform_reply_on_screen(comment)

      continue

def check_new_posts(posts):
  for post in posts:
    if post.author is None:
      log_error("Post deleted")
      continue
    print("Checking " + post.author.name + "'s '" + post.title + "' post", file=stderr)

    if not post_have_comments(post):
      log_error("Post doesn't have comments")
      continue
    print(" Post have comments", file=stderr)

    check_comments(post.comments)


def run_bot(subreddit_handler):
 check_new_posts(subreddit_handler.new(limit=25))
 sleep(30)
