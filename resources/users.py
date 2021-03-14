from werkzeug.security import safe_str_cmp
from flask import jsonify
from flask_restful import Resource, reqparse
from models.users import User as UserModel
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

_parser = reqparse.RequestParser()
_parser.add_argument('username', required=True)
_parser.add_argument('password', required=True)

class Login(Resource):
  def post(self):
    data = _parser.parse_args()
    username = data['username']
    password = data['password']
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(password, user.password):
      uid = user.id
      access_token = create_access_token(identity=uid, fresh=True)
      refresh_token = create_refresh_token(uid)
      return jsonify(access_token=access_token, refresh_token=refresh_token)
    return {'message': 'Invalid credentials.'}, 401
    
class Logout(Resource):
  @jwt_required()
  def post(self):
    #TODO: Expired tokens.
    pass
    
class Register(Resource):
  def post(self):
    data = _parser.parse_args()
    username = data['username']
    if UserModel.find_by_username(username):
      return {'message': 'User already exists'}, 400
    user = UserModel(username, data['password']).save()
    return {'success': True, 'user': user.json()}
    
class UserList(Resource):
  @jwt_required()
  def get(self):
    return jsonify(users=[u.json() for u in UserModel.all()])
    
class User(Resource):
  @jwt_required()
  def get(self, id:int):
    user = UserModel.find(id)
    if user:
      return jsonify(user=user.json())
    return jsonify(message='No such user.')
    
  @jwt_required()
  def put(self, id:int):
    _parser.add_argument('new_username', required=True)
    _parser.add_argument('new_password', required=True)
    data = _parser.parse_args()
    username = data['username']
    password = data['password']
    user = UserModel.find(id)
    if user and user.username == username and safe_str_cmp(password, user.password):
      new_username =  data['new_username']
      new_password =  data['new_password']
      user.username = new_username
      user.password = new_password
      user.save()
      return jsonify(message='User was updated.')
    return {'message': 'The user does not exist.'}, 404
  
  @jwt_required()
  def delete(self, id:int):
    user = UserModel.find(id)
    b = False
    if user:
      b = user.delete()
    return jsonify(success=b)