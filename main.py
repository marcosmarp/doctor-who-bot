from datetime import datetime
from functions import RunBot, MinutesBetweenTimes

while(True):
  if 'last_comment_time' in locals():
    if MinutesBetweenTimes(last_comment_time, datetime.now()) >= 10:
      RunBot()
  else:
    global last_comment_time
    last_comment_time = datetime(1990, 10, 9, 4, 19, 15) 
