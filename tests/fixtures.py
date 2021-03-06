from copy import deepcopy

def get_meme(name):
    return deepcopy(memes[name])

def get_post(pubid):
    return deepcopy(posts[pubid])

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
    'fred': {'guid':'024', 'name':'fred', 
             'title':'Search Fred', 'description':'Meme description', 
             'url':'http://meme.yahoo.com/fred',
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
    'repost_1': {'guid':'123', 'pubid':'123',
                 'type':'repost', 'caption':'blah', 'content':'blah',
                 'comment':'blah', 'url':'http://meme.yahoo.com/p/123',
                 'timestamp':'1234567890', 'repost_count':'12345'},
    'comment_1': {'guid':'456', 'pubid':'456',
                  'type':'comment', 'caption':'blah', 'content':'blah',
                  'comment':'blah', 'url':'http://meme.yahoo.com/p/456',
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
    'filled_post_1': {'guid':'123', 'pubid':'123',
                      'type':'post', 'caption':'blah', 'content':'blah',
                      'comment':'blah', 'url':'http://meme.yahoo.com/p/123',
                      'origin_guid': '456','via_guid': '789',
                      'timestamp':'1234567890', 'repost_count':'12345'},
    }
