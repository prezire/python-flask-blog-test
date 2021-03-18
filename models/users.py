from .dbs import db
#from .timestamp import Timestamp
from passlib.hash import sha256_crypt
from services.json import class_attrs

class User(db.Model):
  __tablename__ = 'users'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  email = db.Column(db.String(100))
  password = db.Column(db.String(100))
  
  now = db.func.now()
  created_on = db.Column(db.DateTime, server_default=now)
  updated_on = db.Column(db.DateTime, server_default=now, server_onupdate=now)
  
  posts = db.relationship('Post', lazy=True)
  comments = db.relationship('Comment', lazy=True)
  
  def __init__(self, name:str, email:str, password:str):
    self.name = name
    self.email = email
    self.password = sha256_crypt.encrypt(password)
    
  def save(self):
    db.session.add(self)
    db.session.commit()
    return self.find(self.id)
    
  def delete(self):
    db.session.delete(self)
    db.session.commit()
    return True
    
  @staticmethod
  def find_by_email(email:str):
    return User.query.filter_by(email=email).first()
    
  @classmethod
  def find_post_by_id(cls, post_id:str):
    return cls.posts.query.filter_by(id=post_id).first()
    
  @staticmethod
  def all():
    return User.query.all()
    
  @staticmethod
  def find(id:int):
    return User.query.filter_by(id=id).first()
    
  def verify_password(self, password:str) -> bool:
    return sha256_crypt.verify(password, self.password)
    
  def json(self):
    d = class_attrs(self)
    del d['password']
    return d