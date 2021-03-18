from .dbs import db 
  
class SqlDateTime:  
  @staticmethod
  def fmt(datetime:db.DateTime) -> str:
    return datetime.strftime('%Y-%m-%d %H:%M:%S')