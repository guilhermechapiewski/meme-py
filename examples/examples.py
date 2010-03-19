#!/usr/bin/env python
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

print '========== Get guilherme_chapiewski Meme =========='
meme = Meme.get(name='guilherme_chapiewski')
print meme
print meme.title
print meme.description 
print meme.url

print '========== Memes that guilherme_chapiewski is following =========='
print meme.following()

print '========== 50 Memes that guilherme_chapiewski is following =========='
print meme.following(count=50)

print '========== Memes following guilherme_chapiewski Meme =========='
print meme.followers()

print '========== 50 Memes following guilherme_chapiewski Meme =========='
print meme.followers(count=50)

print '========== Posts from guilherme_chapiewski Meme =========='
gcposts = meme.posts()
print gcposts
print '---------- Results  ----------'
for post in gcposts:
    print 'Type: %s' % post.type
    print 'Repost count: %s' % post.repost_count
    print 'Original: %s' % post.is_original
    print '----------------------------------------------'

print '========== The latest post from guilherme_chapiewski Meme =========='
latest_post = gcposts[0]
print '---------- Details  ----------'
print 'Type: %s' % post.type
print 'Repost count: %s' % post.repost_count
print 'Content: %s' % post.content
print 'Caption: %s' % post.caption
print '----------------------------------------------'

print '========== The activity around the latest post =========='
for post in latest_post.activity():
  print 'Type: %s' % post.type #repost or commment
  print 'Comment: %s' % post.comment
  print 'GUID: %s' % post.guid
  print '----------------------------------------------'



