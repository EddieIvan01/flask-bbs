from .. import login_manager
from .. import mongo
from .. import app

from flask_login import UserMixin
import hashlib
from bson.objectid import ObjectId

salt = app.config["SECRET_KEY"]

class BaseUser(UserMixin):
    
    __slots__ = ['id', 'uname', 'passwd', 'passwd_hash', 'email', 'role']
    
    def __init__(self, _id, uname=None, passwd=None, email=None, role="basic"):
        self.id=_id
        self.uname = uname
        self.passwd = passwd
        self.email = email
        self.role = role
        self.passwd_hash = hashlib.sha256(passwd.encode('utf-8')+(hashlib.md5(salt.encode("utf-8")).hexdigest()).encode("utf-8")).hexdigest()
    
    def is_admin(self):
        return self.role=="root"
    
    def __repr__(self, action):
        return "User-{} {}".format(self.uname, action)

    @classmethod
    def query(cls, user_id):
        result = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        return cls(result["_id"], result["uname"], result["passwd"], result["email"], result["role"])
        
    @staticmethod
    def verify_passwd(passwd, _hash):
        return hashlib.sha256(passwd.encode('utf-8')+(hashlib.md5(salt.encode("utf-8")).hexdigest()).encode("utf-8")).hexdigest()==_hash
    
    @staticmethod
    def hash_passwd(passwd, salt):
        return hashlib.sha256(passwd.encode('utf-8')+(hashlib.md5(salt.encode("utf-8")).hexdigest()).encode("utf-8")).hexdigest()
    
@login_manager.user_loader
def load_user(user_id):
    return BaseUser.query(user_id)
