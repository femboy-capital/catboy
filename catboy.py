import discord
import requests
from owoify import owoify
import random
from reddit import RedditFetcher
import asyncio
import os
from dotenv import load_dotenv


load_dotenv()


DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
NEWS_TOKEN = os.getenv('NEWS_TOKEN')
NEWS_URL = 'https://cryptopanic.com/api/v1/posts/?auth_token={0}&filter=hot'.format(NEWS_TOKEN)

NEWS_COMMANDS = ['!news']
FEMBOY_COMMANDS = ['!femboy', '!downbad']

UWU_OPTIONS = ['owo', 'uwu', 'uvu']


class Nekobot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents)
        self.fetchers = [RedditFetcher('CuteTraps'), RedditFetcher('femboyhentai'), RedditFetcher('traphentai')]

    async def fetch_news(self, message):
        async with message.channel.typing():
            r = requests.get(url=NEWS_URL)
            news = r.json()

            article = random.choice(news['results'])
            uwu_title = owoify(article['title'], random.choice(UWU_OPTIONS))

        description = '[{0}]({1})'.format(owoify("Read this article", random.choice(UWU_OPTIONS)), article['url'])
        embed = discord.Embed(title=uwu_title, description=description)
        await message.channel.send(embed=embed)

    async def fetch_femboy(self, message):
        urls = []
        async with message.channel.typing():
            for fetcher in self.fetchers:
                img_url = fetcher.fetch_random()
                if img_url != None:
                    urls.append(img_url)

        if len(urls) == 0:
            await message.channel.send(owoify("I'm so sorry, I ran out of content!", random.choice(UWU_OPTIONS)))
            return

        img_url = random.choice(urls)
        for fetcher in self.fetchers:
            fetcher.use_url(img_url)
        await message.channel.send(img_url)

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return # don't listen to self
        
        for news_command in NEWS_COMMANDS:
            if message.content.startswith(news_command):
                await self.fetch_news(message)
                return
        
        for femboy_command in FEMBOY_COMMANDS:
            if message.content.startswith(femboy_command):
                await self.fetch_femboy(message)
                return

    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            welcome_msg = owoify('Welcome to Femboy Capital, {0}! Please enjoy your stay!'.format(member.display_name), 'uwu')
            await asyncio.sleep(1)
            await guild.system_channel.send(welcome_msg)


if __name__ == '__main__':
    client = Nekobot()
    client.run(DISCORD_TOKEN)
