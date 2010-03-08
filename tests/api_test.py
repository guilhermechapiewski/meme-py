import unittest

from mockito import *

from meme import Meme

class MemeApiTest(unittest.TestCase):
    
    def test_should_get_meme_by_name(self):
        meme_reporitory_mock = Mock()
        when(meme_reporitory_mock).get('some_name').thenReturn('ok')
        
        Meme.meme_repository = meme_reporitory_mock
        
        assert Meme.get('some_name') == 'ok'

class MemePostsApiTest(unittest.TestCase):
    
    def test_should_get_popular_posts(self):
        post_repository_mock = Mock()
        when(post_repository_mock).popular('en').thenReturn('popular_posts')
        
        Meme.Posts.post_repository = post_repository_mock
        
        assert Meme.Posts.popular() == 'popular_posts'
        
    def test_should_get_popular_posts_by_language(self):
        post_repository_mock = Mock()
        when(post_repository_mock).popular('pt').thenReturn('popular_posts_from_pt')

        Meme.Posts.post_repository = post_repository_mock

        assert Meme.Posts.popular(locale='pt') == 'popular_posts_from_pt'
        
    def test_should_search_posts(self):
        post_repository_mock = Mock()
        when(post_repository_mock).search('a query').thenReturn('search_result')

        Meme.Posts.post_repository = post_repository_mock

        assert Meme.Posts.search('a query') == 'search_result'