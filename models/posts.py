from .dbs import db
from .timestamp import SqlDateTime, Timestamp

class Post(db.Model):
  __tablename__ = 'posts'
  
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(80))
  content = db.Column(db.Text(80))
  
  now = db.func.now()
  created_on = db.Column(db.DateTime, server_default=now)
  updated_on = db.Column(db.DateTime, server_default=now, server_onupdate=now)
  deleted_on = db.Column(db.DateTime)
  
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User')
  
  comments = db.relationship('Comment', lazy='dynamic')
  
  def __init__(self, title:str, user_id:int, content:str=None):
    self.title = title
    self.user_id = user_id
    self.content = content
    
  @staticmethod
  def all(cls):
    return Post.query.all()
    
  def save(self):
    db.session.add(self)
    db.session.commit()
    return Store.find(self.id)
    
  def delete(self):
    db.session.delete(self)
    db.session.commit()
    return True
    
  @staticmethod
  def find(id:int):
    return Post.query.filter_by(id=id).first()
  
  def json(self):
    slug = self.title.lower().replace(' ', '-')
    d = {'id': self.id, 'title': self.title, 'slug': slug, 'content': self.content}
    d.update(Timestamp.json(created_on=self.created_on, updated_on=self.updated_on, deleted_on=self.deleted_on))
    return d