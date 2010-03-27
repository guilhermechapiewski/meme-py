from meme import MemeRepository, PostRepository

class Meme(object):
    meme_repository = MemeRepository()
    
    @staticmethod
    def get(name=None):
        '''Gets a Meme by it's name/user, e.g.: "gchapiewski".'''
        return Meme.meme_repository.get(name)

    @staticmethod
    def search(query, count=10):
        '''Searches for Memes that have the title similar to the search string.'''
        return Meme.meme_repository.search(query, count)
    
    class Posts(object):
        post_repository = PostRepository()

        @staticmethod
        def popular(locale='en', count=10):
            '''Gets the popular posts.'''
            return Meme.Posts.post_repository.popular(locale, count)
        
        @staticmethod
        def search(query, count=10):
            '''Searches for Posts that contains the specified word(s).'''
            return Meme.Posts.post_repository.search(query, count)
        
        @staticmethod
        def activity(guid, pubid, count=10):
            '''Shows the activity of a Post.'''
            return Meme.Posts.post_repository.activity(guid, pubid, count)