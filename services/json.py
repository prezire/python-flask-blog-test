from models.timestamp import SqlDateTime
import datetime

def class_attrs(class_object:object) -> dict:
  attrs = {}
  for k, v in class_object.__dict__.items():
    if not k.startswith('__') and not k.startswith('_'):
      attrs[k] = SqlDateTime.fmt(v) if isinstance(v, datetime.datetime) else v
  return attrs