from requests.exceptions import ConnectionError, HTTPError, InvalidURL
from bs4 import BeautifulSoup
import twposter
import requests
import cssutils
import time
import os


# Downloading photos from Telegram channel


def get_page(url):
    try:
        response = requests.get(url)
        print('Status Code: {}'.format(response.status_code))
    except ConnectionError:
        return 'ConnectionError'
    except HTTPError:
        return 'HTTPEror'
    except InvalidURL:
        return 'InvalidURL'
    except Exception as e:
        return 'Exception: {}'.format(e)
    else:
        return response


def get_name_from_url(url):
    endpoints = url.split('/')
    name = endpoints[len(endpoints)-1]
    if len(name) > 30:
        return name[-32:]
    else:
        return name


def save_image(url, folder):
    image = get_page(url)
    name = get_name_from_url(url)
    path = os.path.join(folder, name)
    try:
        with open(path, 'wb') as f:
            result = f.write(image.content)
        return name
    except Exception as e:
        print('Error saving image: {}'.format(e))
        return False


def scrap(channel, post):
    channel_url = 'https://t.me/{}/{}?embed=1'.format(channel, post)
    page = get_page(channel_url)
    if isinstance(page, str):
        return page
    else:
        page = page.text
    soup = BeautifulSoup(page, 'html5lib')
    # Scraping the target element
    photo = soup.find('a', attrs={'class':'tgme_widget_message_photo_wrap'})
    video = soup.find('video', attrs={'class':'tgme_widget_message_video js-message_video'})
    msg = soup.find('div', attrs={'class':'tgme_widget_message_text js-message_text'})
    error = soup.find('div', attrs={'class':'tgme_widget_message_error'})
    # Print Text from post, if exists
    '''
    if msg != None:
        print('Text:\n' + msg.text)
    '''
    # Verify type of post
    if photo != None:
        # Format the text to CSS
        style = 'a{' + photo['style'] + '}'
        # Extract the url from CSS property
        sheet = cssutils.parseString(style)
        rules = []
        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                prop = rule.style['background-image']
                photo_url = prop.replace('url(','').replace(')','')
                # Return the photo URL
                return photo_url
    elif video != None:
        # Return the video URL
        video_url = str(video['src'])
        return 'Video'
    elif error != None:
        # 'Post not found'
        return error.text
    else:
        return 'NoPhoto'


def run(tchannel, start_post, img_folder, tweet_text, tweets_per_h):
    channel = tchannel
    npost = start_post
    nomedia_cont = 0
    verify_number = 5
    while True:
        print('.\n----- CHECKING TELEGRAM CHANNEL -----')
        content = scrap(channel, npost)
        if content.endswith('.jpg'):
            print('----- DOWNLOADING IMAGE -------------')
            result = save_image(content, img_folder)
            if result:
                print('Post {}: {}'.format(npost, result))
                print('----- POSTING IMAGE -----------------')
                twposter.tweet_media(tweet_text, img_folder, result)
            else:
                print('Post {}: Error saving photo.'.format(npost))
            npost += 1
            nomedia_cont = 0
            time.sleep(twposter.tweets_hour(tweets_per_h)) # Example: 4 tweets/h = 900 s = 15 min
        elif content == 'NoPhoto' or content == 'Video':
            print('Post {} has no photo to show. ({})'.format(npost, content))
            npost += 1
            nomedia_cont = 0
            time.sleep(10)
        elif content == 'Post not found':
            print('Post {} deleted or not posted yet.'.format(npost))
            if nomedia_cont < verify_number:
                print('Post {}: NO photo found.'.format(npost))
                nomedia_cont += 1
                npost += 1
            else:
                nomedia_cont = 0
                npost -= verify_number
                print('No post found since post number {}'.format(npost - 1))
                time.sleep(twposter.tweets_hour(tweets_per_h)/3) # Waiting to check for a new telegram post
        elif content == 'ConnectionError':
            print('There is no Internet connection!')
            print('Let\'s try again in 60 seconds')
            time.sleep(60) # If no connection it will try again in 1 min.
        else:
            print('An error ocurred: {}'.format(content))


# it will execute if run as a script, no when it's imported
if __name__ == '__main__':
    print(save_image('https://i.imgur.com/Uy2XzsN.jpg'))