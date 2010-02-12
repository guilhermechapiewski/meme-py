from setuptools import setup

import meme

setup(
    name = "meme-py",
    version = meme.VERSION,
    packages = ["meme"],
    author = "Guilherme Chapiewski",
    author_email = "guilherme.chapiewski@gmail.com",
    description = "Yahoo! Meme client API.",
    license = "Apache License 2.0",
    keywords = "yahoo meme client api",
    url = "http://github.com/guilhermechapiewski/meme-py/",
    long_description = "Client API to consume Yahoo! Meme's (http://meme.yahoo.com) webservices on YQL (http://developer.yahoo.com/yql).",
)
