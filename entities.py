from functions import *
from google.appengine.ext import db


class User(db.Model):
    """This class stores the information about users

    Attributes
    name -- Name of user
    password -- Hashed password
    email -- Email address of user"""

    name = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        """Retrieve user by its id"""
        return User.get_by_id(uid)

    @classmethod
    def by_name(cls, name):
        user = User.all().filter('name =', name).get()
        return user

    @classmethod
    def register(cls, name, pwd, email=None):
        pwd_hash = make_pwd_hash(name, pwd)
        return User(name=name,
                    password=pwd_hash,
                    email=email)

    @classmethod
    def login(cls, name, pwd):
        user = cls.by_name(name)
        if user and valid_pwd(name, pwd, user.password):
            return user


class Post(db.Model):
    """This class stores the information about blog posts

    Attributes
    title -- Title of post
    content -- Content of post
    created -- Creation date and time of post
    last_modified -- Last modification date and time
    createdby -- Username of created of blog post"""

    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    createdby = db.StringProperty(required=True)


class Comments(db.Model):
    """This class stores the comments on blog posts

    Attributes
    comment -- The comment
    by -- Username who commented
    created -- Date and time of comment
    post -- Id of post on which commented"""

    comment = db.TextProperty(required=True)
    by = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    post = db.IntegerProperty(required=True)


class Like(db.Model):
    """This class stores the likes on blog post

    Attributes
    user -- Username of user who liked
    post -- Id of the post which is liked
    liked -- Date and time of like"""

    user = db.StringProperty(required=True)
    post = db.IntegerProperty(required=True)
    liked = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def list_of_likes(cls, uname):
        """Retrieves the list of likes by user"""
        likes_list = []
        likes = Like.all()
        likes.filter("user =", uname)
        for like in likes:
            likes_list.append(like.post)
        return likes_list
    
    @classmethod
    def check_like(cls, uname, post):
        """Check if post is liked by user"""
        l = Like.all()
        l.filter("user =", uname).filter("post =", post)
        for like in l:
            if like:
                return True
