from meme import MemeRepository, PostRepository

class Meme(object):
    meme_repository = MemeRepository()
    
    @staticmethod
    def get(name=None):
        return Meme.meme_repository.get(name)
    
    @staticmethod
    def recommended(locale='en', count=10):
        return Meme.meme_repository.recommended(locale, count)
    
    class Posts(object):
        post_repository = PostRepository()

        @staticmethod
        def popular(locale='en', count=10):
            return Meme.Posts.post_repository.popular(locale, count)
        
        @staticmethod
        def search(query, count=10):
            return Meme.Posts.post_repository.search(query, count)
