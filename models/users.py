from .dbs import db
from .timestamp import SqlDateTime, Timestamp

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
    self.password = password
    
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
    
  def json(self):
    d = {'id': self.id, 'name': self.name, 'email': self.email}
    d.update(Timestamp.json(created_on=self.created_on, updated_on=self.updated_on))
    return d