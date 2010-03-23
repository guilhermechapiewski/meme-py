from meme import MemeRepository, PostRepository

class Meme(object):
    meme_repository = MemeRepository()
    
    @staticmethod
    def get(name=None):
        return Meme.meme_repository.get(name)
    
    class Posts(object):
        post_repository = PostRepository()

        @staticmethod
        def popular(locale='en', count=10):
            return Meme.Posts.post_repository.popular(locale, count)
        
        @staticmethod
        def search(query, count=10):
            return Meme.Posts.post_repository.search(query, count)
        
        @staticmethod
        def posts(guid, count=10):
            return Meme.Posts.post_repository.posts(guid, count)
        
        @staticmethod
        def activity(guid, pubid, count=10):
            return Meme.Posts.post_repository.activity(guid, pubid, count)
