from .dbs import db

class Timestamp:
  @staticmethod
  def json(**dates):
    d = {'created_on': SqlDateTime.fmt(dates['created_on']), 'updated_on': SqlDateTime.fmt(dates['updated_on'])}
    if 'deleted_on' in dates and dates['deleted_on']:
      d.update(SqlDateTime.fmt(dates['deleted_on']))
    return d
    
  
class SqlDateTime:  
  @staticmethod
  def fmt(datetime:db.DateTime) -> str:
    return datetime.strftime('%Y-%m-%d %H:%M:%S')