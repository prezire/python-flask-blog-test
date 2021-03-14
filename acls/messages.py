class Permission:
  @staticmethod
  def denied():
    return {'message': 'Permission denied.'}, 401