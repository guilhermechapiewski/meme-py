import unittest

from mockito import *

from meme.meme import Meme, MemeRepository, PostRepository, MemeNotFound

class MemeRepositoryTest(unittest.TestCase):
    
    def test_should_get_meme_by_name(self):
        yql_mock = Mock()
        yql_query = 'SELECT * FROM meme.info WHERE name = "some_name"'
        query_result = Mock()
        query_result.rows = [{'guid':'123', 'name':'some_name', 
                'title':'Cool Meme title', 'description':'Meme description', 
                'url':'http://meme.yahoo.com/some_name',
                'avatar_url':'http://img.yahoo.com/avatar/123.jpg', 
                'language':'pt', 'followers':5}]
        query_result.count = 1
        when(yql_mock).execute(yql_query).thenReturn(query_result)
        
        repository = MemeRepository()
        repository.yql = yql_mock
        
        meme = repository.get('some_name')
        assert meme.guid == '123'
    
    def test_should_get_memes_following_a_meme(self):
        yql_mock = Mock()

        yql_query = 'SELECT * FROM meme.info WHERE name = "some_name"'
        query_result = Mock()
        query_result.rows = [{'guid':'123', 'name':'some_name', 
                'title':'Cool Meme title', 'description':'Meme description', 
                'url':'http://meme.yahoo.com/some_name',
                'avatar_url':'http://img.yahoo.com/avatar/123.jpg', 
                'language':'pt', 'followers':2}]
        query_result.count = 1
        when(yql_mock).execute(yql_query).thenReturn(query_result)
        
        yql_query_following = 'SELECT * FROM meme.following(2) WHERE owner_guid = "123"'
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
        
        memes = repository.following('some_name', 2)
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
        yql_query = 'SELECT * FROM meme.popular WHERE locale="pt"'
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

        posts = repository.popular('pt')
        assert len(posts) == 2

    def test_should_search_posts(self):
        yql_mock = Mock()
        yql_query = 'SELECT * FROM meme.search WHERE query="a sample query"'
        query_result = Mock()
        query_result.rows = [{'guid':'123', 'pubid':'123', 
                'type':'post', 'caption':'blah', 'content':'blah', 
                'comment':'blah', 'url':'http://meme.yahoo.com/p/123', 
                'timestamp':'1234567890', 'repost_count':'12345'}]
        query_result.count = 1
        when(yql_mock).execute(yql_query).thenReturn(query_result)

        repository = PostRepository()
        repository.yql = yql_mock

        posts = repository.search('a sample query')
        assert len(posts) == 1
        assert posts[0].guid == '123'

class MemeTest(unittest.TestCase):
    
    def test_should_get_memes_following_a_meme(self):
        meme_repository_mock = Mock()
        when(meme_repository_mock).following('some_name', 10).thenReturn(['memes_following'])
        
        meme = Meme()
        meme.meme_repository = meme_repository_mock
        meme.name = 'some_name'
        
        assert meme.following() == ['memes_following']
        

