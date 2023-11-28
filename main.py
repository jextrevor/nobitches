#!/usr/bin/env python3

import discord
import os
from dotenv import load_dotenv
import re
from PIL import Image, ImageFont
from pilmoji import Pilmoji
from io import BytesIO
from random import shuffle, randint
import asyncio

load_dotenv()

myFont = ImageFont.truetype('impact.ttf', 80)

hasWarned = False

FILLER_WORDS = [
    'and',
    'or',
    'i',
    'you',
    'but',
    'an',
    'a',
    'for',
    'yet',
    'so',
    'i\'m',
    'you\'re',
    'am',
    'are',
    'it',
    'that',
    'the'
]

def createImage(message):
    with Image.open('nobitches.png') as img:
        # Call draw Method to add 2D graphics in an image
        with Pilmoji(img) as pilmoji:
            pilmoji.text((int((737 - pilmoji.getsize(message.upper(), myFont)[0])/2), 750), message.upper(), fill="white", font=myFont)
        returnFile = BytesIO()
        # Save the edited image
        img.save(returnFile, format="PNG")
        returnFile.seek(0)
        return returnFile

def exclude_filler_words(word):
    return word not in FILLER_WORDS

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        global hasWarned
        # don't respond to ourselves
        if message.author == self.user:
            return

        match = re.search("(n|N)o .+\?", message.content)

        if match is not None:
            image = createImage(match.group())
            if message.mentions:
                print(message.mentions)
            await message.reply(f"{' '.join(list(map(lambda x: x.mention, message.mentions)))}", file=discord.File(image, filename="nobitches.png"))

        if randint(1, 40) == 1:
            words = list(filter(exclude_filler_words, message.content.split()))
            print("got the random")
            if len(words) >= 3:
                shuffle(words)
                print("gonna do it in 10 minutes")
                await asyncio.sleep(randint(2700, 21600))
                await message.reply(f"She {words[0].lower()} on my {words[1].lower()} till I {words[2].lower()}")
        
        if randint(1, 300) == 1 and hasWarned == False:
            hasWarned = True
            await asyncio.sleep(randint(21600, 54000))
            await message.reply("Quick, run, they're coming for you")

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(os.environ["DISCORD_TOKEN"])
