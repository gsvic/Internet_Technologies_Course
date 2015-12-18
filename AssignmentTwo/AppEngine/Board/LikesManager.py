__author__ = 'gsvic'

import webapp2
import logging
import ast

from google.appengine.ext import db
from google.appengine.api import users


"""
This file includes two classes for like handling
1) Post likes
2) Comment likes
"""
class LikesManager(webapp2.RequestHandler):
    def post(self):

        post_key = self.request.get('entity_id')

        username = db.get(post_key).user_mail

        current_user_email = users.get_current_user().email()
        button = self.request.get('like_btn')
        post = db.get(post_key)
        logging.info(post.text)
        self.redirect('/?user='+username)

        if button == 'Unlike':
            logging.info("Unlike")
            for usr in post.liked_by:
                if usr == current_user_email:
                    post.liked_by.remove(usr)
            post.likes = len(post.liked_by)
            post.put()
            return
        else:
            logging.info("Like")
            """Check for like existence"""
            for usr in post.liked_by:
                if usr == current_user_email:
                    return

            post.liked_by.append(current_user_email)
            post.likes = len(post.liked_by)
            post.put()

"""
***Comment Likes Handler***
The likes are saved in a comment dictionary(hashmap).
When a new like happens, the comment dict in string
format is being retrieved and converted into a compilable
python dict. Then, the new like is appended in the likes list.
Finally, the dict is converted into string again and passed
back to the db
"""
class LikeComment(webapp2.RequestHandler):
    def post(self):
        post = db.get(self.request.get("entity_id"))       
        username = post.user_mail    
        current_user_email = users.get_current_user().email()

        comment_id = self.request.get("comment_id")
        button = self.request.get("comment_like")
        if button == "Like":
            self.AddLike(post, int(comment_id))
        else:
            self.RemoveLike(post, int(comment_id))

        self.redirect('/?user='+username)

    """Function for adding likes"""
    def AddLike(self, post, comment_id):
        decoded_comments = ast.literal_eval(post.comments)
        current_comment = decoded_comments[comment_id]
        current_comment['likes'].append(users.get_current_user().email())
        decoded_comments[comment_id] = current_comment
        post.comments = str(decoded_comments)
        post.put()
        logging.info(current_comment)

    """Function for removing likes"""
    def RemoveLike(self, post, comment_id):
        decoded_comments = ast.literal_eval(post.comments)
        current_comment = decoded_comments[comment_id]
        for like in current_comment['likes']:
            if like == users.get_current_user().email():
                current_comment['likes'].remove(like)
        decoded_comments[comment_id] = current_comment
        post.comments = str(decoded_comments)
        post.put()
        logging.info(current_comment)





application = webapp2.WSGIApplication([('/likesmanager', LikesManager),
                                       ('/likecomment', LikeComment)], debug=True)
