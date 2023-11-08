#!/usr/bin/env python3

import discord
import os
from dotenv import load_dotenv
import re
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from random import shuffle, randint
import asyncio

load_dotenv()

myFont = ImageFont.truetype('impact.ttf', 80)

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
    'you\'re'
]

def createImage(message):
    # Open an Image
    img = Image.open('nobitches.png')

    # Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(img)

    _, _, w, h = I1.textbbox((0, 0), message.upper(), font=myFont)
    I1.text(((737-w)/2, 750), message.upper(), font=myFont, fill=(255,255,255))
    returnFile = BytesIO()
    # Save the edited image
    img.save(returnFile, format="PNG")
    returnFile.seek(0)
    return returnFile

def exclude_filler_words(word):
    return word.lower() not in FILLER_WORDS

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
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
            words = filter(exclude_filler_words, message.content.split())
            print("got the random")
            if len(words) >= 3:
                shuffle(words)
                print("gonna do it in 10 minutes")
                await asyncio.sleep(600)
                await message.reply(f"She {words[0].lower()}ing on my {words[1].lower()} till I {words[2].lower()}")

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(os.environ["DISCORD_TOKEN"])
