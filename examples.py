from meme import Meme

# auth
#MemeApi.authenticate(user='gchapiewski', passwd='mypasswd')

# --> examples - posts
print '========== Popular memes =========='
print Meme.Posts.popular()

print '========== Popular memes from Brazil =========='
print Meme.Posts.popular(locale='pt')

# --> examples - memes
meme = Meme.get(name='guilherme_chapiewski')
print '========== guilherme_chapiewski Meme =========='
print meme

print '========== Memes following guilherme_chapiewski Meme =========='
print meme.following()

print '========== 50 Memes following guilherme_chapiewski Meme =========='
print meme.following(count=50)