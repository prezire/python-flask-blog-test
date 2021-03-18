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
  def post(self, post:str):
    p = PostModel.find_by_slug(post)
    if p:
      c = CommentModel(Parser.instance().parse_args()['body'], p.id, User().id()).save()
      return {'data': c.json()}
    else:
      return {'message': 'No query results for such post.'}

class Comment(Resource):    
  @jwt_required()
  def delete(self, post:str, comment:int):
    c = PostModel.find_comment_by_slug(post, comment)
    if not c:
      return {'message': 'No comments to delete.'}, 404
    return {'status': 'Record deleted successfully.'}
    
  @jwt_required()
  def patch(self, post:str, comment:int):
    parser = Parser.instance()
    parser.add_argument('title', type=str, required=False)
    parser.add_argument('parent_id', type=int, required=False)
    data = parser.parse_args()
    body = data['body']
    c = PostModel.find_comment_by_slug(post, comment)
    if c:
      c.body = body
    else:
      c = CommentModel(body, post, User().id())
    if 'title' in data and data['title']:
      c.title = data['title']
    if 'parent_id' in data and data['parent_id']:
      c.parent_id = data['parent_id']
    c.save()
    return {'data': c.json(True)}

class CommentList(Resource):
  #Guest.
  def get(self, post:str):
    p = PostModel.find_by_slug(post)
    if p:
      return {'data': [i.json(True) for i in p.comments]}
    return {'data': []}