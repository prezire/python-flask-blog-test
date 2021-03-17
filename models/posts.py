from .dbs import db
from .timestamp import SqlDateTime, Timestamp
from datetime import datetime

class Post(db.Model):
  __tablename__ = 'posts'
  
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(80))
  content = db.Column(db.Text())
  photo_original_filename = db.Column(db.String(500))
  photo_system_filename = db.Column(db.String(500))
  
  now = db.func.now()
  created_on = db.Column(db.DateTime, server_default=now)
  updated_on = db.Column(db.DateTime, server_default=now, server_onupdate=now)
  deleted_on = db.Column(db.DateTime)
  
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User')
  
  comments = db.relationship('Comment', lazy=True)
  
  def __init__(self, title:str, content:str, user_id:int):
    self.title = title
    self.user_id = user_id
    self.content = content
    
  @staticmethod
  def all(paginate=False, page:int=1, per_page:int=2):
    if paginate:
      return Post.query.paginate(page=page, per_page=per_page)
    return Post.query.all()
    
  def slug(self) -> str:
    return self.title.lower().replace(' ', '-')
    
  def save(self):
    db.session.add(self)
    db.session.commit()
    return Post.find(self.id)
    
  def delete(self):
    self.deleted_on = datetime.now()
    db.session.commit()
    return True
    
  @staticmethod
  def find(id:int):
    return Post.query.filter_by(id=id).first()
  
  def json(self):
    d = {'id': self.id, 'title': self.title, 'slug': self.slug(), 'content': self.content, 'user_id': self.user_id}
    d.update(Timestamp.json(created_on=self.created_on, updated_on=self.updated_on, deleted_on=self.deleted_on))
    return d