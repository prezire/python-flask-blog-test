from flask_jwt_extended import get_current_user

class Delete:
  @staticmethod
  def can():
    return get_current_user()['payload']['sub'] == 1