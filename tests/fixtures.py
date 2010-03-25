from copy import deepcopy

memes = {
    'john': {'guid':'123', 'name':'john',
             'title':'Cool Meme title', 'description':'Meme description', 
             'url':'http://meme.yahoo.com/john',
             'avatar_url':'http://img.yahoo.com/avatar/123.jpg', 
             'language':'pt', 'followers':5},
    'mike': {'guid':'456', 'name':'mike', 
             'title':'Cool Meme title', 'description':'Meme description', 
             'url':'http://meme.yahoo.com/mike',
             'avatar_url':'http://img.yahoo.com/avatar/123.jpg', 
             'language':'pt', 'followers':10},
    'danny': {'guid':'789', 'name':'danny', 
              'title':'Cool Meme title', 'description':'Meme description', 
              'url':'http://meme.yahoo.com/danny',
              'avatar_url':'http://img.yahoo.com/avatar/123.jpg', 
              'language':'pt', 'followers':20},
    }

posts = {
    'complete_post_1': {'guid':'123', 'pubid':'123',
                        'type':'post', 'caption':'blah', 'content':'blah',
                        'comment':'blah', 'url':'http://meme.yahoo.com/p/123',
                        'timestamp':'1234567890', 'repost_count':'12345'},
    'complete_post_2': {'guid':'456', 'pubid':'456',
                        'type':'post', 'caption':'blah', 'content':'blah',
                        'comment':'blah', 'url':'http://meme.yahoo.com/p/456',
                        'timestamp':'1234567890', 'repost_count':'12345'},
    'simple_post_1': {'guid':'123', 'pubid':'123',
                      'type':'post',
                      'timestamp':'1234567890', 'repost_count':'12345'},
    'post_for_activity_1': {'guid':'some_guid', 'pubid':'some_pubid',
                            'type':'post', 'caption':'blah', 'content':'blah',
                            'comment':'blah', 'url':'http://meme.yahoo.com/p/123',
                            'timestamp':'1234567890', 'repost_count':'12345'},
    'post_is_original_1': {'guid':'123', 'pubid':'123',
                           'type':'post', 'caption':'blah', 'content':'blah',
                           'comment':'blah', 'url':'http://meme.yahoo.com/p/123',
                           'timestamp':'1234567890', 'repost_count':'12345'},
    'post_is_not_original_1': {'guid':'123', 'pubid':'123',
                               'type':'post', 'caption':'blah', 'content':'blah',
                               'comment':'blah', 'url':'http://meme.yahoo.com/p/123',
                               'timestamp':'1234567890', 'repost_count':'12345', 'origin_guid':'666foo'},
    }

def get_meme(name):
    return deepcopy(memes[name])

def get_post(pubid):
    return deepcopy(posts[pubid])
