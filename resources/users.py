from werkzeug.security import safe_str_cmp
from flask import jsonify, json
from flask_restful import Resource, reqparse
from models.users import User as UserModel
from models.timestamp import SqlDateTime
from models.tokens import BlackList
from flask_jwt_extended import (get_jwt,
                                create_access_token,
                                create_refresh_token,
                                jwt_required,
                                get_jwt_identity)
from exceptions.messages import unprocessable_entity as unproc
from datetime import timedelta, datetime

class Parser:
  @staticmethod
  def instance():
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, help='The email field is required.')
    parser.add_argument('password', required=True, help='The password field is required.')
    return parser

class Login(Resource):
  def post(self):
    data = Parser.instance().parse_args()
    email = data['email']
    password = data['password']
    user = UserModel.find_by_email(email)
    if user and safe_str_cmp(password, user.password):
      uid = user.id
      sec = 1800
      exp = timedelta(seconds=sec)
      access_token = create_access_token(identity=uid, fresh=True, expires_delta=exp)
      refresh_token = create_refresh_token(uid)
      exp_on = SqlDateTime.fmt((datetime.now() + exp))
      return {'token': access_token, 'token_type': 'Bearer', 'refresh_token': refresh_token, 'expires_on': exp_on}
    return unproc('The given data was invalid.', credentials='These credentials do not match our records.'), 422
    
class Logout(Resource):
  @jwt_required()
  def post(self):
    return {'success': BlackList(get_jwt()['jti']).save() is not None}
    
class RefreshToken(Resource):
  @jwt_required(refresh=True)
  def post(self):
    refresh_token = create_access_token(identity=get_jwt_identity(), fresh=False)
    return {'token': refresh_token}
  
class Register(Resource):
  def post(self):
    parser = Parser.instance()
    parser.add_argument('name', required=True, help='The name field is required.')
    parser.add_argument('password_confirmation', required=True)
    data = parser.parse_args()
    name = data['name']
    email = data['email']
    password = data['password']
    #TODO: ReqParse err stacking.
    if password != data['password_confirmation']:
      return unproc('The given data was invalid.', password='The password confirmation does not match.'), 422
    if UserModel.find_by_email(email):
      return unproc('The given data was invalid.', email='The email has already been taken.'), 422
    user = UserModel(name, email, password).save()
    return user.json(), 201
    
class UserList(Resource):
  @jwt_required()
  def get(self):
    return jsonify(users=[u.json() for u in UserModel.all()])
    
class User(Resource):
  @staticmethod
  def id() -> int:
    return get_jwt()['sub']
    
  @jwt_required()
  def get(self, id:int):
    user = UserModel.find(id)
    if user:
      return jsonify(user=user.json())
    return jsonify(message='No such user.')
    
  @jwt_required()
  def put(self, id:int):
    parser = Parser.instance()
    parser.add_argument('new_email', required=True)
    parser.add_argument('new_password', required=True)
    data = parser.parse_args()
    email = data['email']
    password = data['password']
    user = UserModel.find(id)
    if user and user.email == email and safe_str_cmp(password, user.password):
      new_email =  data['new_email']
      new_password =  data['new_password']
      user.email = new_email
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