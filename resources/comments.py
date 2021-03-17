from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.comments import Comment as CommentModel
from resources.users import User
from authorizations.gates import Delete
from acls.messages import Permission
from flask import abort, request

class Parser:
  @staticmethod
  def instance():
    parser = reqparse.RequestParser()
    parser.add_argument('body', type=str, required=True, help='The body field is required.')
    return parser

class CommentCreate(Resource):
  @jwt_required()
  def post(self, post:int):
    comment = CommentModel(Parser.instance().parse_args()['body'], post, User().id()).save()
    return {'data': comment.json()}

class Comment(Resource):    
  @jwt_required()
  def delete(self, post:int, comment:int):
    if not Delete.can():
      return Permission.denied()
    comment = CommentModel.find(comment)
    if not comment:
      return {'message': 'No comments to delete.'}, 404
    return {'deleted': comment.delete()}
    
  @jwt_required()
  def patch(self, post:int, comment:int):
    comment = CommentModel.find(comment)
    data = _parser.parse_args()
    stat = 'created'
    if comment:
      comment.body = body
      stat = 'updated'
    else:
      comment = CommentModel(body)
    parent_id = request.parent_id
    if parent_id:
      comment.parent_id = parent_id
    comment.save()
    return {stat: comment.json()}

class CommentList(Resource):
  #Guest.
  def get(self, post:int):
    return {'data': [i.json() for i in CommentModel.all()]}