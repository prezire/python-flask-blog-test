from .dbs import db
from datetime import datetime
from slugify import slugify
from services.json import class_attrs

class Post(db.Model):
  __tablename__ = 'posts'
  
  id = db.Column(db.Integer, primary_key=True)
  
  title = db.Column(db.String(200))
  slug = db.Column(db.String(200), nullable=False)
  
  content = db.Column(db.Text())
  photo_original_filename = db.Column(db.String(500))
  photo_system_filename = db.Column(db.String(500))
  
  now = db.func.now()
  created_on = db.Column(db.DateTime, server_default=now)
  updated_on = db.Column(db.DateTime, server_default=now, server_onupdate=now)
  deleted_on = db.Column(db.DateTime)
  
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User')
  
  comments = db.relationship('Comment', lazy='dynamic')
  
  def __init__(self, title:str, content:str, user_id:int):
    self.set_title(title)
    self.user_id = user_id
    self.content = content
    
  def set_title(self, title:str):
    self.title = title
    self.slug = slugify(title)
    
  @staticmethod
  def all(paginate=False, page:int=1, per_page:int=2):
    if paginate:
      return Post.query.paginate(page=page, per_page=per_page)
    return Post.query.all()
    
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
    
  @staticmethod
  def find_by_slug(slug:str):
    return Post.query.filter_by(slug=slug).first()
    
  @staticmethod
  def find_comment_by_slug(slug:str, comment_id:int):
    p = Post.query.filter_by(slug=slug).first()
    if p:
      return p.comments.filter_by(id=comment_id).first()
  
  def json(self):
    return class_attrs(self)