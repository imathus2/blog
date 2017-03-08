import os
import webapp2
import jinja2
from entities import *
from functions import *

from string import letters
from google.appengine.ext import db

# Jinja2 template intialization
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Handler(webapp2.RequestHandler):
    """This class handles the requests using webapp2"""

    def write(self, *a, **kw):
        """Writes the output"""
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """Render output using template"""
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        kw['u'] = self.u
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header('Set-Cookie',
                                         '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.u = uid and User.by_id(int(uid))


class MainPage(Handler):
    """Generates the index/home page of website"""

    def get(self):
        """Renders the home page"""
        like_list = []
        if self.u:
            like_list = Like.list_of_likes(self.u.name)
        posts = Post.all().order('-created')
        self.render("home.html", posts=posts, likes=like_list)


class SignupPage(Handler):
    """Signup page handler"""

    def get(self):
        self.render("signup.html")

    def post(self):
        errors = False
        self.username = self.request.get('username')
        self.email = self.request.get('email')
        self.password = self.request.get('password')
        self.confirm = self.request.get('confirm')
        params = dict(username=self.username,
                      email=self.email)

        # Validate username
        if not validate_username(self.username):
            params['error_username'] = "Username is invalid"
            errors = True
        # Validate Email
        if not validate_email(self.email):
            params['error_email'] = "Email is invalid"
            errors = True
        # Validate Password
        if not validate_password(self.password):
            params['error_password'] = "Password is valid"
            errors = True
        # Compare Password
        if self.password != self.confirm:
            params['error_confirm'] = "Password do not match"
            errors = True

        if errors:
            self.render("signup.html", **params)

        else:
            # Check if username already exsists
            user = User.by_name(self.username)
            if user:
                msg = "User already exsists."
                self.render('signup.html', error_username=msg)
            else:
                # Register user
                user = User.register(self.username, self.password, self.email)
                user.put()
                self.redirect('/')


class Login(Handler):
    """Login page handler"""
    def get(self):
        self.render("login.html")

    def post(self):
        self.username = self.request.get("username")
        self.password = self.request.get("password")
        # Match login credentials
        user = User.login(self.username, self.password)
        if user:
            # Login successful
            self.login(user)
            self.redirect("/")
        else:
            # Login unsuccessful
            msg = "Invalid username or password"
            self.render("login.html", error=msg)


class Logout(Handler):
    """Logout page handler"""
    def get(self):
        self.logout()
        self.redirect('/')


class NewPost(Handler):
    def get(self):
        if self.u:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        if not self.u:
            self.redirect('/login')
        else:
            title = self.request.get('title')
            content = self.request.get('content')

            if title and content:
                p = Post(title=title, content=content, createdby=self.u.name)
                p.put()
                self.redirect('/blog/%s' % str(p.key().id()))
            else:
                msg = "Please provide title and content."
                self.render("newpost.html", error=msg)


class PostPage(Handler):
    def get(self, post_id):
        liked = False
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)
        if not post:
            self.error(404)
            return
        cmt = Comments.all().order('-created')
        cmt.filter("post =", int(post_id))
        if self.u:
            liked = Like.check_like(uname=self.u.name, post=int(post_id))
        self.render("permalink.html", post=post, cmt=cmt, liked=liked)

    def post(self, post_id):
        if not self.u:
            self.redirect('/login')
        else:
            liked = False
            comment = self.request.get("comment")
            if comment:
                c = Comments(comment=comment, by=self.u.name,
                             post=int(post_id))
                c.put()
                key = db.Key.from_path('Post', int(post_id))
                post = db.get(key)
                cmt = Comments.all().order('-created')
                cmt.filter("post =", int(post_id))
                liked = Like.check_like(uname=self.u.name, post=int(post_id))
                self.render("permalink.html", post=post, cmt=cmt, liked=liked)


class EditPost(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)
        if not post:
            self.error(404)
            return
        self.render("editpost.html", post=post)

    def post(self, post_id):
        if not self.u:
            self.redirect('/login')
        else:
            title = self.request.get('title')
            content = self.request.get('content')

            if title and content:
                key = db.Key.from_path('Post', int(post_id))
                p = db.get(key)
                p.title = title
                p.content = content
                p.put()
                self.redirect('/blog/%s' % str(p.key().id()))
            else:
                msg = "Please provide title and content."
                self.render("editpost.html", error=msg)


class DeletePost(Handler):
    def get(self, post_id):
        if self.u:
            key = db.Key.from_path('Post', int(post_id))
            p = db.get(key)
            if p.createdby == self.u.name:
                p.delete()
            self.redirect('/')
        else:
            self.redirect('/login')


class LikePost(Handler):
    def get(self, post_id):
        if self.u:
            key = db.Key.from_path('Post', int(post_id))
            p = db.get(key)
            if not p.createdby == self.u.name:
                liked = Like.check_like(uname=self.u.name, post=int(post_id))
                if not liked:
                    like = Like(user=self.u.name, post=int(post_id))
                    like.put()
                    self.redirect('/blog/' + post_id)
        else:
            self.redirect('/login')


class Dislike(Handler):
    def get(self, post_id):
        if self.u:
            key = db.Key.from_path('Post', int(post_id))
            p = db.get(key)
            if not p.createdby == self.u.name:
                l = Like.all()
                l.filter("user =", self.u.name).filter("post =", int(post_id))
                for like in l:
                    like.delete()
            self.redirect('/blog/' + post_id)
        else:
            self.redirect('/login')


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/signup', SignupPage),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/blog/newpost', NewPost),
                               ('/blog/([0-9]+)', PostPage),
                               ('/edit/([0-9]+)', EditPost),
                               ('/delete/([0-9]+)', DeletePost),
                               ('/like/([0-9]+)', LikePost),
                               ('/dislike/([0-9]+)', Dislike)
                               ], debug=True)
