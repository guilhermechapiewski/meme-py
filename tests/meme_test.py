import unittest

from mockito import *

from meme.meme import Meme, Post, MemeRepository, PostRepository, MemeNotFound

class MemeRepositoryTest(unittest.TestCase):
    
    def test_should_get_meme_by_name(self):
        yql_mock = Mock()
        yql_query = 'SELECT * FROM meme.info WHERE name = "some_name"'
        query_result = Mock()
        query_result.rows = {'guid':'123', 'name':'some_name', 
                'title':'Cool Meme title', 'description':'Meme description', 
                'url':'http://meme.yahoo.com/some_name',
                'avatar_url':'http://img.yahoo.com/avatar/123.jpg', 
                'language':'pt', 'followers':5}
        query_result.count = 1
        when(yql_mock).execute(yql_query).thenReturn(query_result)
        
        repository = MemeRepository()
        repository.yql = yql_mock
        
        meme = repository.get('some_name')
        assert meme.guid == '123'

    def test_should_get_memes_following_a_meme(self):
        yql_mock = Mock()
        
        
        owner_guid = "123fooGUID"
        #this should be exactly the same query as the 'following' method
        yql_query = 'SELECT * FROM meme.following(%d) WHERE owner_guid = "%s"' % (1, owner_guid)
        
        query_result = Mock()
        query_result.rows = {'guid':'123', 'name':'some_name', 
                'title':'Cool Meme title', 'description':'Meme description', 
                'url':'http://meme.yahoo.com/some_name',
                'avatar_url':'http://img.yahoo.com/avatar/123.jpg', 
                'language':'pt', 'followers':2}
        query_result.count = 1
        when(yql_mock).execute(yql_query).thenReturn(query_result)
        
        repository = MemeRepository()
        repository.yql = yql_mock
                
        meme = repository.following(owner_guid, 1)
    
        assert meme.guid == '123'

        
        yql_query_following = 'SELECT * FROM meme.following(%d) WHERE owner_guid = "%s"' % (2, owner_guid)
        query_following_result = Mock()
        query_following_result.rows = []
        query_following_result.rows.append({'guid':'456', 'name':'some_other_name', 
                'title':'Cool Meme title', 'description':'Meme description', 
                'url':'http://meme.yahoo.com/some_name',
                'avatar_url':'http://img.yahoo.com/avatar/123.jpg', 
                'language':'pt', 'followers':10})
        query_following_result.rows.append({'guid':'789', 'name':'some_other_creative_name', 
                'title':'Cool Meme title', 'description':'Meme description', 
                'url':'http://meme.yahoo.com/some_name',
                'avatar_url':'http://img.yahoo.com/avatar/123.jpg', 
                'language':'pt', 'followers':20})
        query_following_result.count = 2
        when(yql_mock).execute(yql_query_following).thenReturn(query_following_result)
        
        repository = MemeRepository()
        repository.yql = yql_mock
                
        memes = repository.following(owner_guid, 2)
    
        assert len(memes) == 2
        
        assert memes[0].guid == '456'
        assert memes[1].guid == '789'


    def test_should_get_meme_followers(self):
        yql_mock = Mock()
        
        owner_guid = "123fooGUID"
        yql_query =  'SELECT * FROM meme.followers(%d) WHERE owner_guid = "%s"' % (1, owner_guid)
        
        query_result = Mock()
        query_result.rows = {'guid':'123', 'name':'some_name', 
                'title':'Cool Meme title', 'description':'Meme description', 
                'url':'http://meme.yahoo.com/some_name',
                'avatar_url':'http://img.yahoo.com/avatar/123.jpg', 
                'language':'pt', 'followers':2}
        query_result.count = 1
        when(yql_mock).execute(yql_query).thenReturn(query_result)
        
        repository = MemeRepository()
        repository.yql = yql_mock
                
        meme = repository.followers(owner_guid, 1)
    
        assert meme.guid == '123'


        yql_query_following =  'SELECT * FROM meme.followers(%d) WHERE owner_guid = "%s"' % (2, owner_guid)
        query_following_result = Mock()
        query_following_result.rows = []
        query_following_result.rows.append({'guid':'456', 'name':'some_other_name', 
                'title':'Cool Meme title', 'description':'Meme description', 
                'url':'http://meme.yahoo.com/some_name',
                'avatar_url':'http://img.yahoo.com/avatar/123.jpg', 
                'language':'pt', 'followers':10})
        query_following_result.rows.append({'guid':'789', 'name':'some_other_creative_name', 
                'title':'Cool Meme title', 'description':'Meme description', 
                'url':'http://meme.yahoo.com/some_name',
                'avatar_url':'http://img.yahoo.com/avatar/123.jpg', 
                'language':'pt', 'followers':20})
        query_following_result.count = 2
        when(yql_mock).execute(yql_query_following).thenReturn(query_following_result)

        repository = MemeRepository()
        repository.yql = yql_mock

        memes = repository.followers(owner_guid, 2)
        assert len(memes) == 2
        assert memes[0].guid == '456'
        assert memes[1].guid == '789'

    def test_should_raise_meme_not_found_error(self):
        yql_mock = Mock()
        yql_query = 'SELECT * FROM meme.info WHERE name = "some_name"'
        query_result = Mock()
        query_result.rows = []
        query_result.count = 0
        when(yql_mock).execute(yql_query).thenReturn(query_result)

        repository = MemeRepository()
        repository.yql = yql_mock

        self.assertRaises(MemeNotFound, repository.get, ('some_name',))

class PostRepositoryTest(unittest.TestCase):
    
    def test_should_get_popular_posts_by_language(self):
        yql_mock = Mock()
        yql_query = 'SELECT * FROM meme.popular(2) WHERE locale="pt"'
        query_result = Mock()
        query_result.rows = []
        query_result.rows.append({'guid':'123', 'pubid':'123', 
                'type':'post', 'caption':'blah', 'content':'blah', 
                'comment':'blah', 'url':'http://meme.yahoo.com/p/123', 
                'timestamp':'1234567890', 'repost_count':'12345'})
        query_result.rows.append({'guid':'456', 'pubid':'456', 
                'type':'post', 'caption':'blah', 'content':'blah', 
                'comment':'blah', 'url':'http://meme.yahoo.com/p/456', 
                'timestamp':'1234567890', 'repost_count':'12345'})
        query_result.count = 2
        when(yql_mock).execute(yql_query).thenReturn(query_result)

        repository = PostRepository()
        repository.yql = yql_mock

        posts = repository.popular('pt', 2)
        assert len(posts) == 2
        assert posts[0].guid == '123'
        assert posts[1].guid == '456'

    def test_should_search_posts(self):
        yql_mock = Mock()
        yql_query = 'SELECT * FROM meme.search(10) WHERE query="a sample query"'
        query_result = Mock()
        query_result.rows = {'guid':'123', 'pubid':'123', 
                'type':'post', 'caption':'blah', 'content':'blah', 
                'comment':'blah', 'url':'http://meme.yahoo.com/p/123', 
                'timestamp':'1234567890', 'repost_count':'12345'}
        query_result.count = 1
        when(yql_mock).execute(yql_query).thenReturn(query_result)

        repository = PostRepository()
        repository.yql = yql_mock

        posts = repository.search('a sample query', 10)
        assert len(posts) == 1
        assert posts[0].guid == '123'
        
    def test_should_get_meme_posts(self):
        yql_mock = Mock()
        yql_query = 'SELECT * FROM meme.posts(2) WHERE owner_guid="foo123bar"'
        query_result = Mock()
        query_result.rows = []
        query_result.rows.append({'guid':'123', 'pubid':'123', 
                'type':'post', 'caption':'blah', 'content':'blah', 
                'comment':'blah', 'url':'http://meme.yahoo.com/p/123', 
                'timestamp':'1234567890', 'repost_count':'12345'})
        query_result.rows.append({'guid':'456', 'pubid':'456', 
                'type':'post', 'caption':'blah', 'content':'blah', 
                'comment':'blah', 'url':'http://meme.yahoo.com/p/456', 
                'timestamp':'1234567890', 'repost_count':'12345'})
        query_result.count = 2
        when(yql_mock).execute(yql_query).thenReturn(query_result)

        repository = PostRepository()
        repository.yql = yql_mock

        posts = repository.posts('foo123bar', 2)
        assert len(posts) == 2
        assert posts[0].guid == '123'
        assert posts[1].guid == '456'

    def test_should_get_meme_posts_by_user(self):
        yql_mock = Mock()
        yql_query = query = 'SELECT * FROM meme.posts(2) WHERE owner_guid in (SELECT guid FROM meme.info WHERE name = "foomeme")'
        query_result = Mock()
        query_result.rows = []
        query_result.rows.append({'guid':'fooguid', 'pubid':'123', 
                'type':'post', 'caption':'blah', 'content':'blah', 
                'comment':'blah', 'url':'http://meme.yahoo.com/p/123', 
                'timestamp':'1234567890', 'repost_count':'12345'})
        query_result.rows.append({'guid':'fooguid', 'pubid':'456', 
                'type':'post', 'caption':'blah', 'content':'blah', 
                'comment':'blah', 'url':'http://meme.yahoo.com/p/456', 
                'timestamp':'1234567890', 'repost_count':'12345'})
        query_result.count = 2
        when(yql_mock).execute(yql_query).thenReturn(query_result)

        repository = PostRepository()
        repository.yql = yql_mock

        posts = repository.postsByUser('foomeme', 2)
        assert len(posts) == 2
        assert posts[0].guid == 'fooguid'
        assert posts[1].guid == 'fooguid'
        
        
    def test_should_get_activity_around_post(self):
        #activity means reposts + comments
        data = {'guid':'123', 'pubid':'456', 
                'type':'post', 'caption':'blah', 'content':'blah', 
                'comment':'blah', 'url':'http://meme.yahoo.com/p/123', 
                'timestamp':'1234567890', 'repost_count':'12345'}                
        post = Post(data)
        
        yql_mock = Mock()
        
        
        activity_result = Mock()
        activity_result.rows = []
        activity_result.rows.append({'guid':'123', 'pubid':'123', 
                'type':'repost', 'caption':'blah', 'content':'blah', 
                'comment':'blah', 'url':'http://meme.yahoo.com/p/123', 
                'timestamp':'1234567890', 'repost_count':'12345'})
        activity_result.rows.append({'guid':'456', 'pubid':'456', 
                'type':'comment', 'caption':'blah', 'content':'blah', 
                'comment':'blah', 'url':'http://meme.yahoo.com/p/456', 
                'timestamp':'1234567890', 'repost_count':'12345'})
        
        yql_query = 'SELECT * FROM meme.post.info(%d) WHERE owner_guid="%s" AND pubid="%s"' % (2, '123', '456')
        
        when(yql_mock).execute(yql_query).thenReturn(activity_result)
        
        repository = PostRepository()
        repository.yql = yql_mock
        
        activity = repository.activity('123', '456', 2)
        assert len(activity) == 2
        
        assert activity[0].type == 'repost'
        assert activity[1].type == 'comment'
        

class MemeTest(unittest.TestCase):
    
    def test_should_get_memes_following_a_meme(self):
        meme_repository_mock = Mock()
        when(meme_repository_mock).following('some_guid', 10).thenReturn(['memes_following'])
        
        meme = Meme()
        meme.meme_repository = meme_repository_mock
        meme.guid = 'some_guid'
        
        assert meme.following(10) == ['memes_following']
        
    def test_should_get_meme_followers(self):
        meme_repository_mock = Mock()
        when(meme_repository_mock).followers('some_guid', 10).thenReturn(['meme_followers'])
        
        meme = Meme()
        meme.meme_repository = meme_repository_mock
        meme.guid = 'some_guid'
        
        assert meme.followers(10) == ['meme_followers']
  

class PostTest(unittest.TestCase):

    def test_should_return_post_activity(self):
        post_repository_mock = Mock()
        when(post_repository_mock).activity('some_guid', 'some_pubid', 10).thenReturn(['post_activity'])
        
        data = {'guid':'some_guid', 'pubid':'some_pubid', 
                'type':'post', 'caption':'blah', 'content':'blah', 
                'comment':'blah', 'url':'http://meme.yahoo.com/p/123', 
                'timestamp':'1234567890', 'repost_count':'12345'}      
        
        post = Post(data)
        post.post_repository = post_repository_mock
        
        assert post.activity(10) == ['post_activity']
    
    def test_should_return_post_without_optional_fields(self):
        """"
        #optional data
        self.content
        self.caption
        self.comment
        self.origin_guid
        self.origin_pubid
        self.via_guid
        self.url
        """
        data = {'guid':'123', 'pubid':'123', 
                'type':'post',
                'timestamp':'1234567890', 'repost_count':'12345'}
        
        post = Post(data)  
        assert post.guid == '123'
        assert post.content == None
        assert post.comment == None
        assert post.origin_guid == None
        assert post.origin_pubid == None
        assert post.via_guid == None
        assert post.url == None
        
    
    def test_should_identify_post_as_original(self):
        #this is an original post
        data = {'guid':'123', 'pubid':'123', 
                'type':'post', 'caption':'blah', 'content':'blah', 
                'comment':'blah', 'url':'http://meme.yahoo.com/p/123', 
                'timestamp':'1234567890', 'repost_count':'12345'}
                
        assert Post(data).is_original == True
    
    def test_should_identify_repost_as_not_original(self):
        #this is a repost
        data = {'guid':'123', 'pubid':'123', 
                'type':'post', 'caption':'blah', 'content':'blah', 
                'comment':'blah', 'url':'http://meme.yahoo.com/p/123', 
                'timestamp':'1234567890', 'repost_count':'12345', 'origin_guid':'666foo'}
        
        assert Post(data).is_original == False
    
    
    
        
