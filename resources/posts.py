from flask_jwt_extended import jwt_required, get_current_user#, current_identity
from flask_restful import Resource, reqparse
from authorizations.gates import Delete
from acls.messages import Permission
from authorizations.gates import Delete
from acls.messages import Permission
from models.posts import Post as PostModel

class Post(Resource):
  def __uid(self) -> int:
    return get_current_user()['payload']['sub']
  
  @staticmethod
  def __name_arg():
    p = reqparse.RequestParser()
    p.add_argument('name', required=True)
    return p.parse_args()['name']
  
  @jwt_required()
  def get(self):
    post = PostModel.find_by_name(self.__name_arg())
    if post:
      post = post.json()
    return {'post': post}, 200 if post else 404
  
  @jwt_required()
  def post(self):
    return {'post': PostModel(self.__name_arg(), self.__uid()).save().json()}
  
  @jwt_required()
  def put(self):
    p = reqparse.RequestParser()
    p.add_argument('old_name', required=True)
    p.add_argument('new_name', required=True)
    args = p.parse_args()
    old_name = args['old_name']
    new_name = args['new_name']
    post = PostModel.find_by_name(old_name)
    stat = 'created'
    if post:
      post.name = new_name
      stat = 'updated'
    else:
      post = PostModel(old_name, self.__uid())
    post.save()
    return {stat: post.json()}
  
  @jwt_required()
  def delete(self):
    if not Delete.can():
      return Permission.denied()
    post = PostModel.find_by_name(self.__name_arg())
    if post:
      return {'deleted': post.delete()}
    return {'message': 'No posts to delete.'}, 404

class PostList(Resource):
  @jwt_required()
  def get(self):
    return {'posts': [s.json() for s in PostModel.all()]}