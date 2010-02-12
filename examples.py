from meme import Meme

# --> examples - posts
print '========== Popular memes =========='
print Meme.Posts.popular()

print '========== Popular memes from Brazil =========='
print Meme.Posts.popular(locale='pt')

print '========== Sample search =========='
posts = Meme.Posts.search('meme rocks')
print posts

print '---------- Results for "meme rocks" ----------'
for post in posts:
    print 'Content: %s' % post.content
    print 'Caption: %s' % post.caption
    print '----------------------------------------------'

# --> examples - memes
meme = Meme.get(name='guilherme_chapiewski')
print '========== guilherme_chapiewski Meme =========='
print meme
print meme.title
print meme.description 
print meme.url

print '========== Memes following guilherme_chapiewski Meme =========='
print meme.following()

print '========== 50 Memes following guilherme_chapiewski Meme =========='
print meme.following(count=50)
