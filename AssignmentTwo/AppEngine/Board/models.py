__author__ = 'gsvic'

from google.appengine.ext import db

class Post(db.Model):
    title = db.TextProperty()
    text = db.TextProperty()
    user_mail = db.TextProperty()
    user_id = db.TextProperty()
    post_date = db.DateTimeProperty()
    likes = db.IntegerProperty(default=0)
    liked_by = db.ListProperty(str)
    comments = db.TextProperty()

class BlogUser(db.Model):
    user = db.UserProperty(auto_current_user=True)
    admin = db.BooleanProperty(default=False)
