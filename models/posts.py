from .dbs import db

class Post(db.Model):
  __tablename__ = 'posts'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  description = db.Column(db.Text(80))
  
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User')
  
  comments = db.relationship('Comment', lazy='dynamic')
  
  def __init__(self, name:str, description:str=None, user_id:int):
    self.name = name
    self.user_id = user_id
    self.description = description
    
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
  
  def json(self, owner:bool=False, comments:bool=False):
    u = self.user
    user = {'id': u.id, 'username': u.username}
    return {'id': self.id, 'name': self.name, 'owner': user}