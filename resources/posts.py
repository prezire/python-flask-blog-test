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
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, help='The title field is required.')
    return parser

class File:
  @staticmethod
  def upload(post):
    parser = Parser.instance()
    data = parser.parse_args()
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
    
  def get(self, post:int):
    return {'data': PostModel.find(post).json()}
  
  @jwt_required()
  def post(self, post:int):
    pass
    # parser = Parser.instance()
    # parser.add_argument('content', type=str, required=True, help='The content field is required.')
    # data = parser.parse_args()
    # title = data['title']
    # content = data['content']
    # p = PostModel(title, content, self.user_id()).save()
    # if p:
    #   File.upload(p)
    #   return {'post': p.json()}, 201
    # return {'message': 'Error creating a new post.'}, 400
  
  @jwt_required()
  def patch(self, post:int):
    data = Parser.instance().parse_args()
    title = data['title']
    p = PostModel.find(post)
    stat = 'created'
    if p:
      p.title = title
      File.upload(p)
      stat = 'updated'
    else:
      content = data['content']
      p = PostModel(title, content, self.user_id())
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
    #return {'posts': [s.json() for s in PostModel.all()]}
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