__author__ = 'gsvic'

import calendar
from google.appengine.api import users
from google.appengine.ext import db
from datetime import datetime, timedelta
import jinja2
import os
import webapp2
import logging
import models
import ast

template_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.getcwd())
)

"""Posts Handler"""
class Posts(webapp2.RequestHandler):
    def post(self):
        usr = users.get_current_user()
        t = datetime.now()
        key = "%s@%s" % (usr, str(t))
        title = self.request.get('post_title')
        text = self.request.get('post_box')
        post = models.Post(key_name=key)

        """Set attributes for the new post record"""
        post.title = title
        post.text = text
        post.user_mail = usr.email()
        post.user_id = usr.user_id()
        post.post_date = t

        """Insert the new post in db"""
        post.put()
        self.redirect('/')

"""
***Comments Handler***
The comments are saved in a dictionary(hashmap). Then,
the dictionary is passed into the Post entity of the
db as a string. In the case that the comment needs to
be retrieved, the dictionary in string format is
converted again to a dict using ast. This is achieved
using two customized functions for comment handling.
"""
class Comment(webapp2.RequestHandler):
    def post(self):
        text = self.request.get('comment')
        post_key = self.request.get('entity_id')
        username = db.get(post_key).user_mail
        delete_button = self.request.get('comment_delete')
        self.redirect('/?user='+username)

        if delete_button:
            self.RemoveComment(post_key, self.request.get("comment_id"))
        else:
            usr = str(users.get_current_user().email())
            date_time = datetime.now()
            date_time = calendar.timegm(date_time.timetuple())
            new_comment = {
                "user": usr,
                "text": text,
                "datetime": date_time,
                "likes": []}
            self.InsertComment(post_key, new_comment)

    """
    Insert a new comment in the db
    Step 1: Convert the the dict in string format
    in a real dict.
    Step 2: Insert the new comment in the dict
    Stem 3: Convert the dict again to string and put
    it into the db
    """
    def InsertComment(self, post_key, comment):
        post = db.get(post_key)
        if post.comments:
            post_comments = ast.literal_eval(post.comments)
            post_comments[comment['datetime']] = comment
            post.comments = str(post_comments)
        else:
            post.comments = str({comment['datetime']: comment})

        post.put()

    """Function for comment deletion"""
    def RemoveComment(self, post_key, comment_key):
        post = db.get(post_key)
        if post.comments:
            post_comments = ast.literal_eval(post.comments)
            del post_comments[int(comment_key)]
            post.comments = str(post_comments)

        post.put()


"""Class for handling post deletions"""
class Delete(webapp2.RequestHandler):
    def post(self):
        post_key = self.request.get('entity_id')
        print "Post key:", post_key
        p = db.get(post_key)
        p.delete()

        self.redirect('/')

"""Class for handling new posts"""
class NewPost(webapp2.RequestHandler):
    def get(self):
        current_time = datetime.now()
        user = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(self.request.path)

        template = template_env.get_template('Board/newpost.html')
        context = {
            'current_time': current_time,
            'user': user,
            'login_url': login_url,
            'logout_url': logout_url,
        }

        self.response.out.write(template.render(context))


application = webapp2.WSGIApplication([('/store_post', Posts),
                                       ('/delete', Delete),
                                       ('/comment', Comment),
                                       ('/newpost', NewPost)], debug=True)
