from datetime import datetime
from functions import RunBot, MinutesBetweenTimes, InitPraw

last_comment_time = datetime(1990, 10, 9, 4, 19, 15) # Making sure that first loop runs and the time check begins with the second loop
reddit_handler = InitPraw()
doctor_who_subreddit_handler = reddit_handler.subreddit("doctorwhobot")

while(True):
  #if MinutesBetweenTimes(last_comment_time, datetime.now()) >= 10:
    RunBot(doctor_who_subreddit_handler)
