import dotenv
import os
import praw

import stream

dotenv.load_dotenv('./.env')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDDIT_USER = os.getenv('REDDIT_USER')
REDDIT_PASS = os.getenv('REDDIT_PASS')

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     username=REDDIT_USER,
                     password=REDDIT_PASS,
                     user_agent='r/autobestof')
