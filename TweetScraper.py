import twint


class TweetScraper:
    def __init__(self):
        # Config options can be found at https://github.com/twintproject/twint/wiki/Configuration
        self.config = twint.Config()
        self.config.Custom_csv = ["id", "user_id", "username", "tweet"]
        self.config.Store_csv = True
        self.config.Output = "output.csv"
        self.config.Lang = 'en'
        return

    def initializeConfig(self, maxTweets, start, end):
        if start and end and start < end:
            raise Exception("End Date cannot be before Start Date")

        if maxTweets:
            self.config.Limit = maxTweets

        if start:
            self.config.Since = start.strftime("%Y-%m-%d %H:%M:%S")

        if end:
            self.config.To = end.strftime("%Y-%m-%d %H:%M:%S")

    def searchByUsername(self, username, maxTweets, start, end):
        if not username:
            raise Exception("Username is null or empty")

        self.initializeConfig(maxTweets, start, end)
        self.config.Username = username

        twint.run.Search(self.config)

    def searchByKeyword(self, keyword, maxTweets, start, end):
        if not keyword:
            raise Exception("Keyword is null or empty")

        self.initializeConfig(maxTweets, start, end)
        self.config.Search = keyword

        twint.run.Search(self.config)