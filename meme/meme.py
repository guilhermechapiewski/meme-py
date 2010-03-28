import yql

class MemeNotFound(Exception):
    """Raised when Meme is not found."""

class Repository(object):
    def __init__(self):
        self.yql = yql.Public()
        self.yql_private = None

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

    def search(self, query, count):
        query = 'SELECT * FROM meme.people(%d) WHERE query = "%s"' % (count, query)
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

    def get(self, owner_guid, pubid):
        query = 'SELECT * FROM meme.posts WHERE owner_guid = "%s" and pubid = "%s"' % (owner_guid, pubid)
        return self._yql_query(query)

    def popular(self, locale, count):
        query = 'SELECT * FROM meme.popular(%s) WHERE locale = "%s"' % (count, locale)
        return self._yql_query(query)

    def search(self, query, count):
        query = 'SELECT * FROM meme.search(%d) WHERE query = "%s"' % (count, query)
        return self._yql_query(query)
    
    def get_by_meme(self, owner_guid, count):
        query = 'SELECT * FROM meme.posts(%d) WHERE owner_guid = "%s"' % (count, owner_guid)
        return self._yql_query(query)
    
    def get_most_reposted_by_meme(self, name, media, count):
        search_for_media = ''
        if media:
            search_for_media = "type:%s" % media
        
        query = "from:%s sort:reposts %s" % (name, search_for_media)
        return self.search(query, count)
    
    def activity(self, guid, pubid, count):
        query = 'SELECT * FROM meme.post.info(%d) WHERE owner_guid = "%s" AND pubid = "%s"' % (count, guid, pubid)
        return self._yql_query(query)

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
    
    def posts(self, count=10):
        return self.post_repository.get_by_meme(self.guid, count)
    
    def most_reposted_posts(self, media='', count=10):
        return self.post_repository.get_most_reposted_by_meme(self.name, media, count)
        
    def __repr__(self):
        return u'Meme[guid=%s, name=%s]' % (self.guid, self.name)

class Post(object):
    def __init__(self, data=None):
        if data:
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
        
            if not self.origin_guid:
                self.is_original = True
            else:
                self.is_original = False
        
        self.post_repository = PostRepository()
    
    def activity(self, count=10):
        return self.post_repository.activity(self.guid, self.pubid, count)
    
    def __repr__(self):
        return u'Post[guid=%s, pubid=%s, type=%s, reposts=%s]' % (self.guid, self.pubid, self.type, self.repost_count)
