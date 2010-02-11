from meme import MemeApi

def print_memes(memes):
    for meme in memes:
        print meme.caption

# api instance
meme_api = MemeApi(user='gchapiewski', passwd='mypasswd')

# examples
print_memes(meme_api.popular())
print_memes(meme_api.popular(locale='en'))

