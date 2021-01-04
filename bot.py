import datetime
import os

from requests_html import HTMLSession
from slackclient import SlackClient
from tinydb import TinyDB, Query

CHANNEL = "U5C3D0Z4N" # maxammann
# CHANNEL = "G466ZEQ0K"   # #augsburg
MESSAGE = "Lecker, lecker lecker! :tada:"

slack_token = os.environ["SLACK_BOT_TOKEN"]
sc = SlackClient(slack_token)
session = HTMLSession()

db = TinyDB('urls.json')
table = db.table('events')

r = session.get('https://tuerantuer.de/cafe/wochenplan/')

yummyImages = r.html.find(".site_content", first=True).find('img[class*=wp-image-]')

# print(sc.api_call("conversations.list", types="public_channel,private_channel"))

for yummyImage in yummyImages:
    imageUrl = yummyImage.attrs['src']

    Event = Query()

    if table.search(Event.url == imageUrl):
        print("No need to post! Already posted URL!")
        break

    result = sc.api_call(
        "chat.postMessage",
        channel=CHANNEL,
        text=MESSAGE,
        attachments=[{
            "fallback": "Wochenplan from Cafe TaT",
            "image_url": imageUrl
        }]
    )

    table.insert({'url': imageUrl, 'time': str(datetime.datetime.now())})

    if not result["ok"]:
        print(result)
        print("Failed to send message to Slack")
