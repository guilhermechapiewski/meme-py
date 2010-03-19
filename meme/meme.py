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
            return Meme(result.rows)
        return [Meme(row) for row in result.rows]
    
    def get(self, name):
        query = 'SELECT * FROM meme.info WHERE name = "%s"' % name
        meme = self._yql_query(query)
        if meme:
            return meme
        raise MemeNotFound("Meme %s was not found!" % name)

    def multiple(self, *guids):
        guids = ["'%s'" % guid for guid in guids]
        query = 'SELECT * FROM meme.info WHERE owner_guid in (%s)' % ','.join(guids)
        memes = self._yql_query(query)
        if memes:
            return memes
        raise MemeNotFound("No Meme found in you guid list")
    
    def following(self, guid, count):
        query = 'SELECT * FROM meme.following(%d) WHERE owner_guid = "%s"' % (count, guid)
        return self._yql_query(query)

    def followers(self, guid, count):
        query = 'SELECT * FROM meme.followers(%d) WHERE owner_guid = "%s"' % (count, guid)
        return self._yql_query(query)
    
class PostRepository(Repository):
    def _yql_query(self, query):
        result = self.yql.execute(query)
        if result.count == 1:
            return [Post(result.rows)]
        return [Post(row) for row in result.rows]

    def popular(self, locale, count):
        query = 'SELECT * FROM meme.popular(%s) WHERE locale="%s"' % (count, locale)
        return self._yql_query(query)
    
    def search(self, query, count):
        query = 'SELECT * FROM meme.search(%d) WHERE query="%s"' % (count, query)
        return self._yql_query(query)
    
    def posts(self, guid, count):
        query = 'SELECT * FROM meme.posts(%d) WHERE owner_guid="%s"' % (count, guid)
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
        return self.post_repository.posts(self.guid, count)
        
    def __repr__(self):
        return u'Meme[guid=%s, name=%s]' % (self.guid, self.name)

class Post(object):
    def __init__(self, data):
        self.guid = data['guid'] #meme id
        self.pubid = data['pubid'] #post id
        self.type = data['type']
        self.caption = data['caption']
        self.content = data['content']
        self.comment = data.get('comment')
        self.url = data['url']
        self.timestamp = data['timestamp']
        self.repost_count = data['repost_count']
        
        #if empty then not a repost
        self.origin_guid = data.get('origin_guid')
        self.origin_pubid = data.get('origin_pubid')
        self.via_guid = data.get('via_guid')
        
        if not self.origin_guid:
            self.is_original = True
        else:
            self.is_original = False
    
    
    def __repr__(self):
        return u'Post[guid=%s, pubid=%s, type=%s]' % (self.guid, self.pubid, self.type)
