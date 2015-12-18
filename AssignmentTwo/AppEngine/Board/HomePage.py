# -*- coding: utf-8 -*-
__author__ = 'gsvic'

import webapp2
import jinja2
import os

import models
import logging
from ast import literal_eval
from datetime import datetime
from google.appengine.api import users, datastore
from google.appengine.ext import db

template_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.getcwd())
)

"""
Parsing python functions to jinja to use them
inside html code
"""
template_env.filters['literal_eval'] = literal_eval
template_env.filters['OrderByDate'] = sorted
template_env.filters['fromtimestamp'] = datetime.fromtimestamp


"""
Home page request handler
"""
class HomePage(webapp2.RequestHandler):
    """
    Getting all registered users from db
    """
    registered_users = models.BlogUser

    def get(self):
        user = users.get_current_user()
        template = template_env.get_template("/Board/home.html")
        q = db.GqlQuery('select * from Post order by post_date desc').fetch(limit=1000)
        admin = False

        """
        The first user who logs in is
        the administrator by default
        """
        if user:
            count = self.registered_users.all().count()
            if count == 0:
                new_user = models.BlogUser(key_name=user.email())
                new_user.admin = True
                new_user.user = user
                new_user.put()
            else:
                if not self.UserExists(user, self.registered_users):
                    new_user = models.BlogUser(key_name=user.email())
                    new_user.admin = False
                    new_user.user = user
                    new_user.put()
            """Checking if current user is admin"""
            admin = self.IsAdmin()

        """Getting page's user"""
        nav_user = self.request.get('user')
        if not nav_user:
            if user:
                nav_user = user.email()
        """
        In the context are defined the variables
        which are visible in the embedded Jinja code
        in the html
        """
        context = {
            'user': users.get_current_user(),
            'log_in': users.create_login_url(self.request.path),
            'log_out': users.create_logout_url(self.request.path),
            'db_posts': q,
            'nav_user': nav_user,
            'registered_users': self.registered_users.all().fetch(limit=1000),
            'admin': admin
        }
        self.response.out.write(template.render(context))

    """Checks if the current user exists in the db"""
    def UserExists(self, new_user, database):
        users = database.all().fetch(limit=1000)
        for usr in users:
            if usr.user.email() == new_user.email():
                return True
        return False

    """"Checks if the current user is an administrator"""
    def IsAdmin(self):
        current_user = users.get_current_user().email()
        is_admin = self.registered_users.get_by_key_name(current_user).admin

        logging.info("\n\n\nCURRENT USER %s, IS_ADMIN %s\n\n\n" % (current_user, is_admin) )
        return is_admin

application = webapp2.WSGIApplication([('/', HomePage)], debug=True)