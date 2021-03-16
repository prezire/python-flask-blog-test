from flask_jwt_extended import jwt_required, get_current_user
from flask_restful import Resource, reqparse
from authorizations.gates import Delete
from acls.messages import Permission
from authorizations.gates import Delete
from acls.messages import Permission
from models.posts import Post as PostModel
import os
from flask import request
from werkzeug.utils import secure_filename
from werkzeug import FileStorage
import hashlib

_parser = reqparse.RequestParser()
_parser.add_argument('title', type=str, required=True, help='The title field is required.')
_parser.add_argument('content', type=str, required=True, help='The content field is required.')

class File:
  @staticmethod
  def upload(post):
    _parser.add_argument('photo', type=FileStorage, location='files')
    data = _parser.parse_args()
    photo = data['photo']
    if photo:
      photo_original_filename = secure_filename(photo.filename)
      ext = photo_original_filename.filename.split('.')[0]
      photo_system_filename = hashlib.sha224(photo_original_filename).hexdigest() + '.' + ext
      uploaded_file.save('./uploads/posts/' + photo_system_filename)
      post.photo_original_filename = photo_original_filename
      post.photo_system_filename = photo_system_filename
      post.save()

class Post(Resource):
  def __user_id(self) -> int:
    return get_current_user()['payload']['sub']
  
  @jwt_required()
  def post(self):
    data = _parser.parse_args()
    title = data['title']
    content = data['content']
    p = PostModel(title, content, self.__user_id()).save()
    if p:
      File.upload(p)
      return {'post': p.json()}
    return {'message': 'Error creating a new post.'}, 400
  
  @jwt_required()
  def patch(self, post:int):
    data = _parser.parse_args()
    title = data['title']
    content = data['content']
    p = PostModel.find(post)
    stat = 'created'
    if p:
      p.title = title
      p.content = content
      File.upload(p)
      stat = 'updated'
    else:
      p = PostModel(title, content, self.__user_id())
    p.save()
    return {stat: p.json()}
  
  @jwt_required()
  def delete(self, post:int):
    if not Delete.can():
      return Permission.denied()
    p = PostModel.find(post)
    if p:
      return {'deleted': p.delete()}
    return {'message': 'No posts to delete.'}, 404

class PostList(Resource):
  @staticmethod
  def all():
    return {'posts': [s.json() for s in PostModel.all()]}
    
  #Guest.
  def get(self):
    return PostList.all()
    
  @jwt_required()
  def post(self):
    return PostList.all()