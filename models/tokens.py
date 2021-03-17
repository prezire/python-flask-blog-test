from .dbs import db

class BlackList(db.Model):
  __tablename__ = 'blacklisted_jwt_ids'
  id = db.Column(db.Integer, primary_key=True)
  
  #JWT ID.
  jti = db.Column(db.String(500))
  
  now = db.func.now()
  created_on = db.Column(db.DateTime, server_default=now)
  updated_on = db.Column(db.DateTime, server_default=now, server_onupdate=now)

  def __init__(self, jti:str):
    self.jti = jti
    
  def save(self):
    db.session.add(self)
    db.session.commit()
    return BlackList.find(self.id)
    
  @staticmethod
  def find(id:int):
    return BlackList.query.filter_by(id=id).first()
    
  @staticmethod
  def all():
    return BlackList.query.all()