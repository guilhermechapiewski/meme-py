import unittest

from mockito import *

from meme.meme import MemeRepository

class MemeRepositoryTest(unittest.TestCase):
    
    def test_should_get_meme_by_name(self):
        query_result = Mock()
        query_result.rows = {'guid':123, 'name':'some_name', 
                'title':'Cool Meme title', 'description':'Meme description', 
                'url':'http://meme.yahoo.com/some_name',
                'avatar_url':'http://img.yahoo.com/avatar/123.jpg', 
                'language':'pt', 'followers':5}
        query_result.count = 1
        
        yql_mock = Mock()
        yql_query = 'SELECT * FROM meme.info WHERE name = "some_name"'
        when(yql_mock).execute(yql_query).thenReturn(query_result)
        
        repository = MemeRepository()
        repository.yql = yql_mock
        
        meme = repository.get('some_name')
        assert meme.name == 'some_name'