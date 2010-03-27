from setuptools import setup

setup(
    name = "meme-py",
    version = '0.3.0',
    packages = ["meme"],
    author = "Guilherme Chapiewski and friends",
    author_email = "guilherme.chapiewski@gmail.com",
    description = "Yahoo! Meme (http://meme.yahoo.com) client API.",
    license = "Apache License 2.0",
    keywords = "yahoo meme client api",
    url = "http://github.com/guilhermechapiewski/meme-py/",
    long_description = "Python client API to consume Yahoo! Meme's (http://meme.yahoo.com) webservices on YQL (http://developer.yahoo.com/yql). Please check the documentation on Github: http://github.com/guilhermechapiewski/meme-py/blob/master/README.textile",
    install_requires = ["yql >= 0.3"],
)
