import discord
import requests
from owoify import owoify
import random
from reddit import RedditFetcher
import asyncio
import os
from dotenv import load_dotenv
import os.path
import pickle


load_dotenv()


DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
NEWS_TOKEN = os.getenv('NEWS_TOKEN')
NEWS_URL = 'https://cryptopanic.com/api/v1/posts/?auth_token={0}&filter=hot'.format(NEWS_TOKEN)
NOID_IMAGE = 'https://i.imgur.com/hA9eBGB.png'
PENTACLE_ETH_URL = 'https://pentacle.ai/eth-ecosystem.json'
HETRO_LINKS = ['https://i.imgur.com/fyPhlfN.mp4', 'https://i.imgur.com/C4y03Gh.mp4', 'https://i.imgur.com/eIP3BbH.mp4', 'https://i.imgur.com/3SrxqD9.jpeg']

NEWS_COMMANDS = ['!news']
FEMBOY_COMMANDS = ['!femboy', '!downbad']
NOID_COMMAND = '!noid'
HETRO_COMMAND = '!hetro'
PENTACLE_COMMANDS = ['!pentacle']
UWU_OPTIONS = ['owo', 'uwu', 'uvu']


class Nekobot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents)
        self.fetchers = [RedditFetcher('CuteTraps'), RedditFetcher('femboyhentai'), RedditFetcher('traphentai')]

        if os.path.exists('posted.pickle'):
            with open('posted.pickle', 'rb') as f:
                self.posted_cache = pickle.load(f)
        else:
            self.posted_cache = set()

    def save_posted_cache(self):
        with open('posted.pickle', 'wb') as f:
            pickle.dump(self.posted_cache, f, protocol=pickle.HIGHEST_PROTOCOL)

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
                img_url = fetcher.fetch_random(self.posted_cache)
                if img_url != None:
                    urls.append(img_url)

        if len(urls) == 0:
            await message.channel.send(owoify("I'm so sorry, I ran out of content!", random.choice(UWU_OPTIONS)))
            return

        img_url = random.choice(urls)
        for fetcher in self.fetchers:
            self.posted_cache.add(img_url)
            self.save_posted_cache()
        await message.channel.send(img_url)

    async def search_pentacle(self, message):
        components = message.content.split(' ')
        if len(components) < 2:
            await message.channel.send(owoify("Please provide a search topic!", random.choice(UWU_OPTIONS)))
            return

        async with message.channel.typing():
            r = requests.get(url=PENTACLE_ETH_URL)
            topics = r.json()['children']
            items = []
            for topic in topics:
                for item in topic['children']:
                    items.append(item)
        
        for item in items:
            if item['name'].lower() == components[1].lower():
                embed = discord.Embed(title=item['name'])
                embed.set_image(url=item['img'])
                for subitem in item['children']:
                    if subitem['name'] == 'Links':
                        for link in subitem['children']:
                            embed.add_field(name=link['name'], value='[View]({0})'.format(link['url']))

                await message.channel.send(embed=embed)
                return
        
        await message.channel.send(owoify("I'm so sorry, I couldn't find what you were looking for!", random.choice(UWU_OPTIONS)))
        return        


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

        if message.content.startswith(HETRO_COMMAND):
            await message.channel.send(random.choice(HETRO_LINKS))
            return
        
        if message.content.startswith(NOID_COMMAND):
            await message.channel.send(NOID_IMAGE)
            return

        for pentacle_command in PENTACLE_COMMANDS:
            if message.content.startswith(pentacle_command):
                await self.search_pentacle(message)
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
