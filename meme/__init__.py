from meme import MemeRepository, PostRepository

class Meme(object):
    meme_repository = MemeRepository()
    
    @staticmethod
    def get(name=None):
        return Meme.meme_repository.get(name)
    
    class Posts(object):
        post_repository = PostRepository()

        @staticmethod
        def popular(locale='en'):
            return Meme.Posts.post_repository.popular(locale)
        
        @staticmethod
        def search(query):
            return Meme.Posts.post_repository.search(query)
