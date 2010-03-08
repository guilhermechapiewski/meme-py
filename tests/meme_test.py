import unittest

from mockito import *

from meme.meme import MemeRepository

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
        assert meme.name == 'some_name'
    
    def test_should_get_memes_following_a_meme(self):
        yql_mock = Mock()

        yql_query = 'SELECT * FROM meme.info WHERE name = "some_name"'
        query_result = Mock()
        query_result.rows = {'guid':'123', 'name':'some_name', 
                'title':'Cool Meme title', 'description':'Meme description', 
                'url':'http://meme.yahoo.com/some_name',
                'avatar_url':'http://img.yahoo.com/avatar/123.jpg', 
                'language':'pt', 'followers':2}
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
