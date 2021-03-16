#!/bin/env python3
import requests
from lxml import html
import json
from pathlib import Path
import os

def load_posted_images():
    with postedImagesPath.open() as f:
        return json.load(f)

def save_posted_images(postedImages):
    with postedImagesPath.open(mode='w') as f:
        json.dump(postedImages, f)

page = requests.get('https://tuerantuer.de/cafe/wochenplan/')
tree = html.fromstring(page.content)

yummyImages = tree.xpath('//div[@class="content-area"]//img[contains(@class, "wp-image")]/@src')

postedImagesPath = Path.home() / 'yummybot.cache'

if not postedImagesPath.exists():
    save_posted_images([])

postedImages = load_posted_images()

for yummyImage in yummyImages:
    if yummyImage in postedImages:
        continue

    requests.post("https://webhook", json = { "text": "Lecker, lecker lecker! :tada:\n![Weekly YummyBot report](%s)" % (yummyImage)})

    postedImages.append(yummyImage)
    
save_posted_images(postedImages)
