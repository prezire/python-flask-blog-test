from .dbs import db
from services.json import class_attrs

class Comment(db.Model):
  __tablename__ = 'comments'
  
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=True)
  body = db.Column(db.Text(), nullable=False)
  
  #OP.
  creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  creator = db.relationship('User')
  
  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
  post = db.relationship('Post')
  
  #Self-ref parent.
  parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
  
  replies = db.relationship('Comment', backref=db.backref('parent', remote_side='Comment.id'))
  
  now = db.func.now()
  created_on = db.Column(db.DateTime, server_default=now)
  updated_on = db.Column(db.DateTime, server_default=now, server_onupdate=now)
  
  def __init__(self, body:str, post_id:int, creator_id:int):
    self.body = body
    self.post_id = post_id
    self.creator_id = creator_id
    
  def save(self):
    db.session.add(self)
    db.session.commit()
    return self.find(self.id)
    
  @staticmethod
  def find(id:int):
    return Comment.query.filter_by(id=id).first()
    
  def delete(self):
    db.session.delete(self)
    db.session.commit()
    return True
    
  @staticmethod
  def all():
    return Comment.query.all()
  
  def json(self, replies=False):
    d = class_attrs(self)
    reps = self.replies
    if replies and reps:
      d.update({'replies': [{'id': rep.id, 'title': rep.title, 'body': rep.body} for rep in reps]})
    return d
