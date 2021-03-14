from flask_jwt_extended import jwt_required, get_current_user#, current_identity
from flask_restful import Resource, reqparse
from models.stores import Store as StoreModel
from authorizations.gates import Delete
from acls.messages import Permission
from authorizations.gates import Delete
from acls.messages import Permission

class Store(Resource):
  
  def __uid(self) -> int:
    return get_current_user()['payload']['sub']
  
  @staticmethod
  def __name_arg():
    p = reqparse.RequestParser()
    p.add_argument('name', required=True)
    return p.parse_args()['name']
  
  @jwt_required()
  def get(self):
    store = StoreModel.find_by_name(self.__name_arg())
    if store:
      store = store.json()
    return {'store': store}, 200 if store else 404
  
  @jwt_required()
  def post(self):
    return {'store': StoreModel(self.__name_arg(), self.__uid()).save().json()}
  
  @jwt_required()
  def put(self):
    p = reqparse.RequestParser()
    p.add_argument('old_name', required=True)
    p.add_argument('new_name', required=True)
    args = p.parse_args()
    old_name = args['old_name']
    new_name = args['new_name']
    store = StoreModel.find_by_name(old_name)
    stat = 'created'
    if store:
      store.name = new_name
      stat = 'updated'
    else:
      store = StoreModel(old_name, self.__uid())
    store.save()
    return {stat: store.json()}
  
  @jwt_required()
  def delete(self):
    if not Delete.can():
      return Permission.denied()
    store = StoreModel.find_by_name(self.__name_arg())
    if store:
      return {'deleted': store.delete()}
    return {'message': 'No stores to delete.'}, 404

class StoreList(Resource):
  @jwt_required()
  def get(self):
    return {'stores': [s.json() for s in StoreModel.all()]}