from .dbs import db

class Timestamp:
  now = db.func.now()
  created_on = db.Column(db.DateTime, server_default=now)
  updated_on = db.Column(db.DateTime, server_default=now, server_onupdate=now)
  
class SqlDateTime:  
  @staticmethod
  def fmt(datetime:db.DateTime) -> str:
    return datetime.strftime('%Y-%m-%d %H:%M:%S')