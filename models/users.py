from .dbs import db

class User(db.Model):
  __tablename__ = 'users'
  
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100))
  password = db.Column(db.String(100))
  posts = db.relationship('Post', lazy=True)
  comments = db.relationship('Comment', lazy=True)
  
  def __init__(self, username:str, password:str):
    self.username = username
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
  def find_by_username(username:str):
    return User.query.filter_by(username=username).first()
    
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
    return {'id': self.id, 'username': self.username}