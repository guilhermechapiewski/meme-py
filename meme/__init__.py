from meme import MemeRepository

class MemeApi(object):
    meme_repository = MemeRepository()

    @staticmethod
    def popular(locale='en'):
        return MemeApi.meme_repository.popular(locale)