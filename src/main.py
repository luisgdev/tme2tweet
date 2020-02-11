import tmehelper

'''
Tweet photos from telegram channel posts
Using tweepy as Twitter library and Telegram HTTP API
This bot was created by https://t.me/luisgve
'''


# Put your Settings below
# Remember to set your keys on twposter.py
# Target Example: 'https://t.me/travelpics/5056'
channel_id = 'travelpics'
start_post = 5060
img_folder = 'img'
tweets_per_hour = 5
tweet_text = 'This awesome landscape was taken from a public #Telegram channel'

# Executing program
try:
    tmehelper.run(channel_id, start_post, img_folder, tweet_text, tweets_per_hour)
except KeyboardInterrupt:
    print('>>> Program Closed! <<<')