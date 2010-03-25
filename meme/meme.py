import yql
from copy import deepcopy

API_KEY = 'dj0yJmk9RW1TaFkzN1NNcVFMJmQ9WVdrOVJXRlZjbnBpTm1zbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1hYg--' # gc
SECRET = 'd09162c0f9d12b3845668301a2776bec8fa5bd23' # gc

class MemeNotFound(Exception):
    """Raised when Meme is not found."""

class Repository(object):
    def __init__(self):
        self.yql = yql.Public()
        self.yql_private = None
    
    #TODO
    # def _private_yql_query(self, query):
    #    if not self.yql_private:
    #        self.yql_private = yql.ThreeLegged(API_KEY, SECRET)
    #        request_token, auth_url = self.yql_private.get_token_and_auth_url()
    #        access_token = self.yql_private.get_access_token(request_token, verifier)
            
    #    self.yql_private.execute(query, token=access_token)

class MemeRepository(Repository):
    
    def _yql_query(self, query):
        result = self.yql.execute(query)
        if result.count == 1:
            return [Meme(result.rows)]
        return [Meme(row) for row in result.rows]
    
    def get(self, name):
        query = 'SELECT * FROM meme.info WHERE name = "%s"' % name
        meme = self._yql_query(query)
        if meme:
            return meme[0]
        raise MemeNotFound("Meme %s was not found!" % name)

    def multiple(self, *guids):
        guids = ["'%s'" % guid for guid in guids]
        query = 'SELECT * FROM meme.info WHERE owner_guid in (%s)' % ','.join(guids)
        memes = self._yql_query(query)
        if memes:
            return memes
        raise MemeNotFound("No Meme found in you guid list")

    def search(self, query, count):
        query = 'SELECT * FROM meme.people(%d) WHERE query="%s"' % (count, query)
        memes = self._yql_query(query)
        if memes:
            return memes
        raise MemeNotFound("No Meme found in your search")
    
    def following(self, guid, count):
        query = 'SELECT * FROM meme.following(%d) WHERE owner_guid = "%s"' % (count, guid)
        return self._yql_query(query)

    def followers(self, guid, count):
        query = 'SELECT * FROM meme.followers(%d) WHERE owner_guid = "%s"' % (count, guid)
        return self._yql_query(query)
    
class PostRepository(Repository):

    def __init__(self):
        super(PostRepository, self).__init__()
        self.meme_repository = MemeRepository()

    def _yql_query(self, query):
        result = self.yql.execute(query)
        if result.count == 1:
            return [Post(result.rows)]
        return [Post(row) for row in result.rows]

    def _yql_query_proxy(self, query, filled=False):
        posts = self._yql_query(query)
        if filled:
            return self.fill_memes(posts)
        return posts

    def popular(self, locale, count):
        query = 'SELECT * FROM meme.popular(%s) WHERE locale="%s"' % (count, locale)
        return self._yql_query(query)

    def search(self, query, count):
        query = 'SELECT * FROM meme.search(%d) WHERE query="%s"' % (count, query)
        return self._yql_query(query)
    
    def posts(self, guid, count, filled=False):
        query = 'SELECT * FROM meme.posts(%d) WHERE owner_guid="%s"' % (count, guid)
        return self._yql_query_proxy(query, filled)
    
    def postsByUser(self, name, count):
        query = 'SELECT * FROM meme.posts(%d) WHERE owner_guid in (SELECT guid FROM meme.info WHERE name = "%s")' % (count, name)
        return self._yql_query(query)
    
    def activity(self, guid, pubid, count):
        query = 'SELECT * FROM meme.post.info(%d) WHERE owner_guid="%s" AND pubid="%s"' % (count, guid, pubid)
        return self._yql_query(query)

    def fill_memes(self, posts):
        posts = deepcopy(posts)
        guids = set()
        for post in posts:
            guids.add(post.guid)
            if post.origin_guid:
                guids.add(post.origin_guid)
            if post.via_guid:
                guids.add(post.via_guid)
        memes = self.meme_repository.multiple(*guids)
        memes_map = {}
        for meme in memes:
            memes_map[meme.guid] = meme
        for post in posts:
            post.meme = memes_map.get(post.guid)
            post.origin_meme = memes_map.get(post.origin_guid)
            post.via_meme = memes_map.get(post.via_guid)
        return posts
    
    def topPosts(self, name, count, media):
        #The most reposted original posts from that user
        if media:
             media = " type:%s" % media
        query = "from:%s sort:reposts%s" % (name, media)
        return self.search(query, count)


class Meme(object):
    def __init__(self, data=None):
        if data:
            self.guid = data['guid']
            self.name = data['name']
            self.title = data['title']
            self.description = data['description']
            self.url = data['url']
            self.avatar_url = data['avatar_url']
            self.language = data['language']
            self.follower_count = data['followers']
        
        self.meme_repository = MemeRepository()
        self.post_repository = PostRepository()
    
    def following(self, count=10):
        return self.meme_repository.following(self.guid, count)
    
    def followers(self, count=10):
        return self.meme_repository.followers(self.guid, count)
    
    def search(self, query, count=10):
        return self.meme_repository.search(query, count)
    
    def posts(self, count=10, filled=False, name=None):
        if not name:
            posts = self.post_repository.posts(self.guid, count)
        else:
            posts = self.post_repository.postsByName(name, count)
        if not filled:
            return posts
        else:
            return self.post_repository.fillMemes(posts)
    
    def topPosts(self, name=self.name, count=10, media=""):
        return self.post_repository.topPosts(name, count, media)
        
    def __repr__(self):
        return u'Meme[guid=%s, name=%s]' % (self.guid, self.name)

class Post(object):
    def __init__(self, data):
        #required data
        self.guid = data['guid'] #meme id
        self.pubid = data['pubid'] #post id
        self.type = data['type']
        self.timestamp = data['timestamp']
        
        #optional data
        self.repost_count = data.get('repost_count') #absent only in comments
        self.url = data.get('url') #absent only in comments
        self.content = data.get('content') #absent only in comments and reposts
        self.caption = data.get('caption')
        self.comment = data.get('comment')        
        self.origin_guid = data.get('origin_guid') #if empty then not a repost
        self.origin_pubid = data.get('origin_pubid')
        self.via_guid = data.get('via_guid')

        #filled memes - only if provided in data dict
        self.meme = data.get('meme')
        self.origin_meme = data.get('origin_meme')
        self.via_meme = data.get('via_meme')
        
        self.post_repository = PostRepository()
        
        if not self.origin_guid:
            self.is_original = True
        else:
            self.is_original = False
    
    def activity(self, count=10):
        return self.post_repository.activity(self.guid, self.pubid, count)
    
    
    def __repr__(self):
        return u'Post[guid=%s, pubid=%s, type=%s, reposts=%s]' % (self.guid, self.pubid, self.type, self.repost_count)
