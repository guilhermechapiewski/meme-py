import unittest

from mockito import *

from meme.meme import Meme, Post, MemeRepository, PostRepository, MemeNotFound
import fixtures

class MemeRepositoryTest(unittest.TestCase):
    
    def setUp(self):
        self.single_query_result = Mock()
        self.single_query_result.rows = fixtures.get_meme('john')
        self.single_query_result.count = 1
        
        self.multiple_query_result = Mock()
        self.multiple_query_result.rows = [
            fixtures.get_meme('mike'),
            fixtures.get_meme('danny'),
        ]
        self.multiple_query_result.count = 2

    def test_should_get_meme_by_name(self):
        yql_query = 'SELECT * FROM meme.info WHERE name = "some_name"'
        yql_mock = Mock()
        when(yql_mock).execute(yql_query).thenReturn(self.single_query_result)
        
        meme_repository = MemeRepository()
        meme_repository.yql = yql_mock
        meme = meme_repository.get('some_name')
        assert meme.guid == '123'
    
    def test_should_raise_meme_not_found_error_when_cannot_find_meme_by_name(self):
         yql_query = 'SELECT * FROM meme.info WHERE name = "some_name"'

         query_result = Mock()
         query_result.rows = []
         query_result.count = 0

         yql_mock = Mock()
         when(yql_mock).execute(yql_query).thenReturn(query_result)

         meme_repository = MemeRepository()
         meme_repository.yql = yql_mock

         self.assertRaises(MemeNotFound, meme_repository.get, 'some_name')
    
    def test_should_search_memes(self):
        yql_query = 'SELECT * FROM meme.people(1) WHERE query = "foobar"'

        query_result = Mock()
        query_result.rows = fixtures.get_meme('fred')
        query_result.count = 1

        yql_mock = Mock()
        when(yql_mock).execute(yql_query).thenReturn(query_result)

        meme_repository = MemeRepository()
        meme_repository.yql = yql_mock

        memes = meme_repository.search('foobar', 1)
        assert len(memes) == 1
        assert memes[0].guid == '024'
        assert memes[0].title == 'Search Fred'
        assert memes[0].follower_count == 20
        
    def test_should_raise_meme_not_found_error_when_search_cannot_find_memes(self):
         yql_query = 'SELECT * FROM meme.people(10) WHERE query = "some_name"'

         query_result = Mock()
         query_result.rows = []
         query_result.count = 0

         yql_mock = Mock()
         when(yql_mock).execute(yql_query).thenReturn(query_result)

         meme_repository = MemeRepository()
         meme_repository.yql = yql_mock

         self.assertRaises(MemeNotFound, meme_repository.search, 'some_name', 10)

    def test_should_get_a_meme_following_a_meme(self):
        yql_query = 'SELECT * FROM meme.following(1) WHERE owner_guid = "123"'
        yql_mock = Mock()
        when(yql_mock).execute(yql_query).thenReturn(self.single_query_result)

        meme_repository = MemeRepository()
        meme_repository.yql = yql_mock
        memes = meme_repository.following(123, 1)
    
        assert len(memes) == 1
        assert memes[0].guid == '123'
    
    def test_should_get_two_memes_following_a_meme(self):
        yql_query = 'SELECT * FROM meme.following(2) WHERE owner_guid = "123"'
        yql_mock = Mock()
        when(yql_mock).execute(yql_query).thenReturn(self.multiple_query_result)
        
        meme_repository = MemeRepository()
        meme_repository.yql = yql_mock
        memes = meme_repository.following(123, 2)

        assert len(memes) == 2
        assert memes[0].guid == '456'
        assert memes[1].guid == '789'

    def test_should_get_one_meme_follower(self):
        yql_query =  'SELECT * FROM meme.followers(1) WHERE owner_guid = "123fooGUID"'
        yql_mock = Mock()
        when(yql_mock).execute(yql_query).thenReturn(self.single_query_result)
        
        meme_repository = MemeRepository()
        meme_repository.yql = yql_mock
        meme = meme_repository.followers("123fooGUID", 1)
        assert len(meme) == 1
        assert meme[0].guid == '123'
    
    def test_should_get_meme_followers(self):
        yql_query =  'SELECT * FROM meme.followers(2) WHERE owner_guid = "123fooGUID"'
        yql_mock = Mock()
        when(yql_mock).execute(yql_query).thenReturn(self.multiple_query_result)

        meme_repository = MemeRepository()
        meme_repository.yql = yql_mock
        memes = meme_repository.followers("123fooGUID", 2)
        assert len(memes) == 2
        assert memes[0].guid == '456'
        assert memes[1].guid == '789'

class PostRepositoryTest(unittest.TestCase):

    def setUp(self):
        self.single_query_result = Mock()
        self.single_query_result.rows = fixtures.get_post('complete_post_1')
        self.single_query_result.count = 1
        
        self.multiple_query_result = Mock()
        self.multiple_query_result.rows = [
            fixtures.get_post('complete_post_1'),
            fixtures.get_post('complete_post_2'),
        ]
        self.multiple_query_result.count = 2
    
    def test_should_get_popular_posts_by_language(self):
        yql_query = 'SELECT * FROM meme.popular(2) WHERE locale = "pt"'
        yql_mock = Mock()
        when(yql_mock).execute(yql_query).thenReturn(self.multiple_query_result)

        post_repository = PostRepository()
        post_repository.yql = yql_mock
        posts = post_repository.popular('pt', 2)
        assert len(posts) == 2
        assert posts[0].guid == '123'
        assert posts[1].guid == '456'

    def test_should_search_posts(self):
        yql_query = 'SELECT * FROM meme.search(5) WHERE query = "a sample query"'
        yql_mock = Mock()
        when(yql_mock).execute(yql_query).thenReturn(self.single_query_result)

        post_repository = PostRepository()
        post_repository.yql = yql_mock
        posts = post_repository.search('a sample query', 5)
        assert len(posts) == 1
        assert posts[0].guid == '123'
        
    def test_should_get_meme_posts(self):
        yql_query = 'SELECT * FROM meme.posts(2) WHERE owner_guid = "foo123bar"'
        yql_mock = Mock()
        when(yql_mock).execute(yql_query).thenReturn(self.multiple_query_result)

        post_repository = PostRepository()
        post_repository.yql = yql_mock
        posts = post_repository.get_by_meme('foo123bar', 2)
        assert len(posts) == 2
        assert posts[0].guid == '123'
        assert posts[1].guid == '456'
    
    def test_should_get_only_one_meme_post(self):
        yql_query = 'SELECT * FROM meme.posts(1) WHERE owner_guid = "foo123bar"'
        yql_mock = Mock()
        when(yql_mock).execute(yql_query).thenReturn(self.single_query_result)

        post_repository = PostRepository()
        post_repository.yql = yql_mock
        posts = post_repository.get_by_meme('foo123bar', 1)
        assert len(posts) == 1
        assert posts[0].guid == '123'
    
    def test_should_get_most_reposted_posts_of_a_meme(self):
        yql_query = 'SELECT * FROM meme.search(2) WHERE query = "from:gchapiewski sort:reposts type:text"'
        yql_mock = Mock()
        when(yql_mock).execute(yql_query).thenReturn(self.multiple_query_result)

        post_repository = PostRepository()
        post_repository.yql = yql_mock
        posts = post_repository.get_most_reposted_by_meme('gchapiewski', 'text', 2)
        
        assert len(posts) == 2
        assert posts[0].guid == '123'
        assert posts[1].guid == '456'

class MemeTest(unittest.TestCase):
    
    def test_should_get_memes_following_a_meme(self):
        meme_repository_mock = Mock()
        when(meme_repository_mock).following('some_guid', 10).thenReturn('memes_following')
        
        meme = Meme()
        meme.meme_repository = meme_repository_mock
        meme.guid = 'some_guid'
        
        assert meme.following(10) == 'memes_following'
        
    def test_should_get_meme_followers(self):
        meme_repository_mock = Mock()
        when(meme_repository_mock).followers('some_guid', 10).thenReturn('meme_followers')
        
        meme = Meme()
        meme.meme_repository = meme_repository_mock
        meme.guid = 'some_guid'
        
        assert meme.followers(10) == 'meme_followers'
    
    def test_should_get_meme_posts(self):
        post_repository_mock = Mock()
        when(post_repository_mock).get_by_meme('some_guid', 5).thenReturn('meme_posts')

        meme = Meme()
        meme.post_repository = post_repository_mock
        meme.guid = 'some_guid'

        assert meme.posts(5) == 'meme_posts'

    def test_should_get_meme_most_reposted_posts(self):
        post_repository_mock = Mock()
        when(post_repository_mock).get_most_reposted_by_meme('name', '', 10).thenReturn('meme_posts')

        meme = Meme()
        meme.post_repository = post_repository_mock
        meme.name = 'name'

        assert meme.most_reposted_posts() == 'meme_posts'

    def test_should_get_meme_most_reposted_video_posts(self):
        post_repository_mock = Mock()
        when(post_repository_mock).get_most_reposted_by_meme('name', 'video', 5).thenReturn('meme_posts')

        meme = Meme()
        meme.post_repository = post_repository_mock
        meme.name = 'name'

        assert meme.most_reposted_posts(media='video', count=5) == 'meme_posts'
  
class PostTest(unittest.TestCase):
    
    def test_should_return_post_without_optional_fields(self):
        data = {'guid':'123', 'pubid':'123', 
                'type':'post',
                'timestamp':'1234567890', 'repost_count':'12345'}
        
        post = Post(data)  
        assert post.guid == '123'
        
        # optional data
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
