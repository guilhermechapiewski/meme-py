from meme import MemeApi

meme_api = MemeApi(user='gchapiewski', passwd='mypasswd')

memes = meme_api.popular(locale='zh')

for meme in memes:
    print meme.caption