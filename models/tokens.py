from .dbs import db

class BlackList(db.Model):
  __tablename__ = 'blacklisted_tokens'
  id = db.Column(db.Integer, primary_key=True)
  token = db.Column(db.String(500))
  
  now = db.func.now()
  created_on = db.Column(db.DateTime, server_default=now)
  updated_on = db.Column(db.DateTime, server_default=now, server_onupdate=now)

  def __init__(self, token:str):
    self.token = token
    
  def save(self):
    db.session.add(self)
    db.session.commit()
    return True