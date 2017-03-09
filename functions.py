import hashlib
import random
import re
import hmac
from string import letters


# Validates username
def validate_username(username):
    USERNAME_RE = re.compile(r"^[a-zA-Z0-9_-]{5,15}$")
    return username and USERNAME_RE.match(username)


# Validates password
def validate_password(password):
    PASSWORD_RE = re.compile(r"^.{5,15}$")
    return password and PASSWORD_RE.match(password)


# Validates email
def validate_email(email):
    EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
    return not email or EMAIL_RE.match(email)


# Cookie hashing
secret = "alpha"


def make_secure_val(val):
    """Generate secure cookie token"""
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())


def check_secure_val(secure_val):
    """Validate cookie token"""
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


def make_salt(length=5):
    """Generate a 5 letter token"""
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pwd_hash(name, pwd, salt=None):
    """Generate hash of password"""
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pwd + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pwd(name, password, h):
    """Validate the password hash"""
    salt = h.split(',')[0]
    return h == make_pwd_hash(name, password, salt)
