def unprocessable_entity(message, **errs):
  return {'message': message, 'errors': {**errs}}