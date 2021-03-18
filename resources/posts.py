from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Resource, reqparse
from authorizations.gates import Delete
from acls.messages import Permission
from authorizations.gates import Delete
from acls.messages import Permission
from models.posts import Post as PostModel
import os
from flask import request, url_for
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import hashlib

class Parser:
  @staticmethod
  def instance():
    p = reqparse.RequestParser()
    p.add_argument('title', type=str, required=True, help='The title field is required.')
    return p

class File:
  @staticmethod
  def upload(post):
    if 'photo' in request.files:
      photo = request.files['photo']
      if photo:
        photo_original_filename = secure_filename(photo.filename)
        ext = photo_original_filename.split('.')[1]
        photo_system_filename = hashlib.sha224(photo_original_filename.encode('utf-8')).hexdigest() + '.' + ext
        filename = './uploads/posts/' + photo_system_filename
        photo.save(filename)
        post.photo_original_filename = photo_original_filename
        post.photo_system_filename = photo_system_filename
        post.save()

class Post(Resource):
  @staticmethod
  def user_id() -> int:
    return get_jwt()['sub']
    
  def get(self, post:str):
    p = PostModel.find_by_slug(post)
    if p:
      return {'data': p.json()}
    return {'message': 'No query results for post.'}, 404
  
  @jwt_required()
  def patch(self, post:str):
    parser = Parser.instance()
    parser.add_argument('content', type=str, required=True, help='The content field is required.')
    data = parser.parse_args()
    title = data['title']
    p = PostModel.find_by_slug(post)
    if p:
      p.set_title(title)
      File.upload(p)
    else:
      content = data['content']
      p = PostModel(title, content, self.user_id())
    p.save()
    return {'data': p.json()}
  
  @jwt_required()
  def delete(self, post:str):
    p = PostModel.find_by_slug(post)
    if p:
      return {'status': 'record deleted successfully'}
    return {'message': 'No posts to delete.'}, 404

class PostList(Resource):   
  #Guest.
  def get(self):
    a = request.args
    first = 1
    page = int(a['page'] if 'page' in a else first)
    per_page = int(a['per_page'] if 'per_page' in a else 10)
    posts = PostModel.all(True, page, per_page)
    url = lambda page: url_for(endpoint='api.posts', _external=True, page=page)
    data = []
    links = {
      'first': url(first),
      'last': url(posts.total), 
      'prev': url(posts.prev_num), 
      'next': url(posts.next_num)
    }
    meta = {
      'current_page': posts.page, 
      'from': first,
      'to': posts.pages,
      'path': url_for(endpoint='api.posts', _external=True),
      'per_page': posts.per_page, 
      'total': posts.total
    }
    for p in posts.items:
      data.append(p.json())
    return {'data': data, 'links': links, 'meta': meta}
    
  @jwt_required()
  def post(self):
    parser = Parser.instance()
    parser.add_argument('content', type=str, required=True, help='The content field is required.')
    data = parser.parse_args()
    title = data['title']
    content = data['content']
    p = PostModel(title, content, Post.user_id()).save()
    if p:
      File.upload(p)
      return {'post': p.json()}, 201
    return {'message': 'Error creating a new post.'}, 400