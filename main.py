from functions import RunBot, InitPraw

reddit_handler = InitPraw()
doctor_who_subreddit_handler = reddit_handler.subreddit("doctorwho")

while(True):
  last_comment_time = RunBot(doctor_who_subreddit_handler)
