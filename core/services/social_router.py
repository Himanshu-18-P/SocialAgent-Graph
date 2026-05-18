from core.platforms.reddit import RedditPlatform


class SocialRouter:

    @staticmethod
    def upload(
        platform: str,
        title: str,
        body: str,
        subreddit: str = "test"
    ):

        if platform == "reddit":

            reddit_platform = RedditPlatform()

            return reddit_platform.create_post(
                subreddit_name=subreddit,
                title=title,
                body=body
            )

        raise ValueError(f"Unsupported platform: {platform}")