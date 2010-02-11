from meme import MemeApi

def print_memes(memes):
    for meme in memes:
        print meme.caption

# auth
#MemeApi.authenticate(user='gchapiewski', passwd='mypasswd')

# examples
print_memes(MemeApi.popular())
print_memes(MemeApi.popular(locale='pt'))
