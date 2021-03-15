from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_current_user
from models.comments import Comment as CommentModel
from authorizations.gates import Delete
from acls.messages import Permission
from flask import abort

class Comment(Resource):    
  @staticmethod
  def __req_args():
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float,required=True)
    parser.add_argument('store_id', type=int,required=True)
    return parser.parse_args()
    
  @jwt_required()
  def get(self, name:str):
    comment = CommentModel.find_by_name(name)
    if comment:
      comment = comment.json()
    return {'comment': comment}, 200 if comment else 404
  
  @jwt_required()
  def post(self, name:str):
    data = self.__req_args()
    comment = CommentModel(name, data['price'], data['store_id']).save()
    return {'comment': comment.json()}
    
  @jwt_required()
  def delete(self, name:str):
    if not Delete.can():
      return Permission.denied()
    comment = CommentModel.find_by_name(name)
    if not comment:
      return {'message': 'No comments to delete.'}, 404
    return {'deleted': comment.delete()}
    
  @jwt_required()
  def put(self, name:str):
    comment = CommentModel.find_by_name(name)
    data = self.__req_args()
    price = data['price']
    store_id = data['store_id']
    stat = 'created'
    if comment:
      comment.price = price
      comment.store_id = store_id
      stat = 'updated'
    else:
      comment = CommentModel(name, price, store_id)
    comment.save()
    return {stat: comment.json()}

class CommentList(Resource):
  @jwt_required()
  def get(self):
    if not Delete.can():
      return Permission.denied()
    return {'comments': [i.json() for i in CommentModel.all()]}