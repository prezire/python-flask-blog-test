import os
from flask import Flask, render_template, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.users import Register as UserRegister, User, UserList, Login, Logout
from resources.posts import Post, PostList
from resources.comments import Comment, CommentList, CommentCreate
from datetime import timedelta
from models.dbs import db
from models.tokens import BlackList

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'test')

app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=os.environ.get('JWT_ACCESS_TOKEN_EXPIRES_SECONDS', 4800))
app.config['JWT_SECRET_KEY'] = app.secret_key
app.config['JWT_BLACKLIST_ENABLED'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

api.add_resource(CommentList, '/api/posts/<string:post>/comments')
api.add_resource(CommentCreate, '/api/posts/<string:post>/comments')
api.add_resource(Comment, '/api/posts/<string:post>/comments/<int:comment>')

api.add_resource(PostList, '/api/posts', endpoint='api.posts')
api.add_resource(Post, '/api/posts/<string:post>')

api.add_resource(UserRegister, '/api/register')
api.add_resource(User, '/users/<int:id>')
api.add_resource(UserList, '/users')
api.add_resource(Login, '/api/login')
api.add_resource(Logout, '/api/logout')

api.init_app(app)

jwt = JWTManager(app)
@jwt.user_lookup_loader
def authorize(header, payload):
  return {'header': header, 'payload': payload}
  
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload) -> bool:
  print([j.jti for j in BlackList.all()])
  return jwt_payload['jti'] in [j.jti for j in BlackList.all()]
  
@jwt.revoked_token_loader
def expired_token_callback(jwt_header, jwt_payload):
  return {'message': 'Token has been revoked.'}, 401

db.init_app(app)
@app.before_first_request
def migrate():
  db.create_all()
  
@app.route('/')
def home():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True)