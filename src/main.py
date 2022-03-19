"""
Tweet photos from telegram channel posts
Using tweepy as Twitter library and Telegram HTTP API
This bot was created by https://t.me/luisgve
"""

import tmehelper


# Target Sample: 'https://t.me/travelpics/5056'
try:
    tmehelper.run(
        channel_id="travelpics",
        start_post=5060,
        img_folder="img",
        tweet_text="This awesome landscape was found on a public #Telegram channel",
        tweets_per_hour=5,
    )
except KeyboardInterrupt:
    print(">>> Program Closed! <<<")
