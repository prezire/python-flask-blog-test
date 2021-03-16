from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_current_user
from models.comments import Comment as CommentModel
from authorizations.gates import Delete
from acls.messages import Permission
from flask import abort, request

parser = reqparse.RequestParser()
parser.add_argument('body', type=str, required=True, help='The body field is required.')

class Comment(Resource):    
  @jwt_required()
  def post(self, post:int):
    comment = CommentModel(_parser.parse_args()['body']).save()
    parent_id = request.parent_id
    if parent_id:
      comment.parent_id = parent_id
      comment.save()
    return {'comment': comment.json()}
    
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
  def get(self, post:int, comment:int):
    return {'comments': [i.json() for i in CommentModel.all()]}