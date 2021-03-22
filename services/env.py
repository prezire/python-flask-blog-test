import os
def env(key:str, default_value=''):
  s = os.environ.get(key, default_value)
  if s == '':
    if default_value == '':
      raise ValueError(f'Both environment key {key} and default_value param are empty or have no values in them.')
    return default_value
  return s