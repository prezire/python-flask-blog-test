from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.comments import Comment as CommentModel
from models.posts import Post as PostModel
from resources.users import User

class Parser:
  @staticmethod
  def instance():
    p = reqparse.RequestParser()
    p.add_argument('body', type=str, required=True, help='The body field is required.')
    return p

class CommentCreate(Resource):
  @jwt_required()
  def post(self, post:int):
    c = CommentModel(Parser.instance().parse_args()['body'], post, User().id()).save()
    return {'data': c.json()}

class Comment(Resource):    
  @jwt_required()
  def delete(self, post:int, comment:int):
    c = PostModel.find_comment(post, comment)
    if not c:
      return {'message': 'No comments to delete.'}, 404
    return {'deleted': c.delete()}
    
  @jwt_required()
  def patch(self, post:int, comment:int):
    c = PostModel.find_comment(post, comment)
    parser = Parser.instance()
    parser.add_argument('title', type=str, required=False)
    parser.add_argument('parent_id', type=int, required=False)
    data = parser.parse_args()
    stat = 'created'
    if c:
      c.body = data['body']
      stat = 'updated'
    else:
      c = CommentModel(body, post_id, User().id())
    if 'title' in data and data['title']:
      c.title = data['title']
    if 'parent_id' in data and data['parent_id']:
      c.parent_id = data['parent_id']
    c.save()
    return {stat: c.json(True)}

class CommentList(Resource):
  #Guest.
  def get(self, post:int):
    return {'data': [i.json(True) for i in CommentModel.all()]}