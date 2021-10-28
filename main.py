from functions import run_bot, init_praw, log_error
from traceback import print_exc

reddit_handler = init_praw()
doctor_who_subreddit = reddit_handler.subreddit("doctorwho")
test_subreddit = reddit_handler.subreddit("doctorwhoredditbot")

while(True):
  try:
    run_bot(test_subreddit)
  except KeyboardInterrupt: # For quitting with ctrl+C
    break
  except:
    log_error("Reddit exception: ")
    print_exc()
