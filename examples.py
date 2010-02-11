from meme import MemeApi

def print_memes(memes):
    for meme in memes:
        print meme.caption

# auth
#MemeApi.authenticate(user='gchapiewski', passwd='mypasswd')

# examples
print_memes(MemeApi.popular())
print_memes(MemeApi.popular(locale='pt'))

# SELECT * FROM meme.following WHERE owner_guid in 
# (select guid from meme.info where name = "guilherme_chapiewski")

#print_users
#MemeApi.get_meme('guilherme_chapiewski').following()