from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_current_user
from models.items import Item as ItemModel
from authorizations.gates import Delete
from acls.messages import Permission
from flask import abort

class Item(Resource):    
  @staticmethod
  def __req_args():
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float,required=True)
    parser.add_argument('store_id', type=int,required=True)
    return parser.parse_args()
    
  @jwt_required()
  def get(self, name:str):
    item = ItemModel.find_by_name(name)
    if item:
      item = item.json()
    return {'item': item}, 200 if item else 404
  
  @jwt_required()
  def post(self, name:str):
    data = self.__req_args()
    item = ItemModel(name, data['price'], data['store_id']).save()
    return {'item': item.json()}
    
  @jwt_required()
  def delete(self, name:str):
    if not Delete.can():
      return Permission.denied()
    item = ItemModel.find_by_name(name)
    if not item:
      return {'message': 'No items to delete.'}, 404
    return {'deleted': item.delete()}
    
  @jwt_required()
  def put(self, name:str):
    item = ItemModel.find_by_name(name)
    data = self.__req_args()
    price = data['price']
    store_id = data['store_id']
    stat = 'created'
    if item:
      item.price = price
      item.store_id = store_id
      stat = 'updated'
    else:
      item = ItemModel(name, price, store_id)
    item.save()
    return {stat: item.json()}

class ItemList(Resource):
  @jwt_required()
  def get(self):
    if not Delete.can():
      return Permission.denied()
    return {'items': [i.json() for i in ItemModel.all()]}