import os
import praw

from dotenv import load_dotenv

load_dotenv()


class RedditPlatform:

    def __init__(self):

        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            username=os.getenv("REDDIT_USERNAME"),
            password=os.getenv("REDDIT_PASSWORD"),
            user_agent=os.getenv("REDDIT_USER_AGENT"),
        )

    def create_post(
        self,
        subreddit_name: str,
        title: str,
        body: str
    ):

        subreddit = self.reddit.subreddit(subreddit_name)

        submission = subreddit.submit(
            title=title,
            selftext=body
        )

        return {
            "posted": True,
            "posted_url": f"https://reddit.com{submission.permalink}"
        }