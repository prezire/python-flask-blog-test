from .dbs import db

class Comment(db.Model):
  __tablename__ = 'comments'
  
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100))
  body = db.Column(db.Text())
  
  #OP.
  creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  creator = db.relationship('User')
  
  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
  post = db.relationship('Post')
  
  #Self-ref parent.
  parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
  parent = db.relationship('Comment')
  
  #Comment replies.
  comments = db.relationship('Comment')
  
  def __init__(self, title:str, body:str, parent_id:int):
    self.title = title
    self.body = body
    self.parent_id = parent_id
    
  def save(self):
    db.session.add(self)
    db.session.commit()
    return self.find(self.id)
    
  @staticmethod
  def find(int:id):
    return Comment.query.filter_by(id=id).first()
    
  def delete(self):
    db.session.delete(self)
    db.session.commit()
    return True
    
  @staticmethod
  def all(cls):
    return Comment.query.all()
  
  def json(self, comments=False):
    return {'id': self.id, 'title': self.title, 'body': self.body}