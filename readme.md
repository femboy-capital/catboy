# catboy
catboy is a horrible discord bot. he has 4 commands right now:
* `!news` - fetch a hot article from cryptopanic and uwu-ify it
* `!femboy` - fetch a femboy from reddit
* `!pentacle [topic]` - search pentacle.ai for an ETH topic and post related links
* `!noid` - noid

he also says hello to new server members. 

## setup
```sh
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

then put your `DISCORD_TOKEN` and `NEWS_TOKEN` keys in `.env`.

## run
```sh
$ python catboy.py
```