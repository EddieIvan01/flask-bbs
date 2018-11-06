from .escape import flask_real_escape
from .escape import xss_escape
from .. import mongo

import mistune

def get_posts_api(limit=0, skip=0, **kwargs):
    for i in kwargs.keys():
        if type(i) != str or type(i) != int:
            continue
        kwargs[i], _ = flask_real_escape(kwargs[i])  
    _posts = mongo.db.posts.find(kwargs).sort([("date", -1)]).skip(skip).limit(limit)
    posts = list(_posts)
    for i in posts:
        i["content"] = mistune.markdown(i["content"], escape=True, hard_wrap=True)
    return posts

def get_posts_count():
    return mongo.db.posts.find().count()
    