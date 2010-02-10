import yql

class MemeApi(object):
    def __init__(self, user, passwd):
        self.yql = yql.Public()

    def _yql_query(self, query):
        memes = []
        result = self.yql.execute(query)
        for row in result.rows:
            memes.append(Meme(row))
        return memes

    def popular(self, locale='pt'):
        query = 'SELECT * FROM meme.popular WHERE locale="%s"' % locale;
        return self._yql_query(query)
    
class Meme(object):
    def __init__(self, data):
        self.category = data['category']
        self.comment = data['comment']
        self.via_guid = data['via_guid']
        self.url = data['url']
        self.timestamp = data['timestamp']
        self.pubid = data['pubid']
        self.repost_count = data['repost_count']
        self.origin_guid = data['origin_guid']
        self.content = data['content']
        self.caption = data['caption']
        self.origin_pubid = data['origin_pubid']
        self.guid = data['guid']
        self.type = data['type']
    
    def __repr__(self):
        mask = u'Meme[guid=%s, type=%s]'
        return mask % (self.guid, self.type)
    
    def __unicode__(self):
        mask = u'MemePost[comment=%s, via_guid=%s, url=%s, timestamp=%s, \
                pubid=%s, repost_count=%s, origin_guid=%s, content=%s, \
                caption=%s, origin_pubid=%s, guid=%s, type=%s]'
        return mask % (self.comment, self.via_guid, self.url, 
                self.timestamp, self.pubid, self.repost_count, 
                self.origin_guid, self.content, self.caption, 
                self.origin_pubid, self.guid, self.type)