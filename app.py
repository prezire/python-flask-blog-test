import os
from flask import Flask, render_template, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.users import Register as UserRegister, User, UserList, Login, Logout
from resources.items import Item, ItemList
from resources.posts import Post, PostList
from resources.comments import Comment, CommentList
from datetime import timedelta
from models.dbs import db

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'test')

app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = os.environ.get('JWT_ACCESS_TOKEN_EXPIRES_SECONDS', timedelta(seconds=1800))
app.config['JWT_SECRET_KEY'] = app.secret_key

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
api.add_resource(CommentList, '/comments')
api.add_resource(Comment, '/comment/<int:id>')

api.add_resource(Post, '/post')
api.add_resource(PostList, '/posts')
api.add_resource(Post, '/post/<int:id>')

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:id>')
api.add_resource(UserList, '/users')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

api.init_app(app)

jwt = JWTManager(app)
@jwt.user_lookup_loader
def authorize(header, payload):
  return {'header': header, 'payload': payload}

db.init_app(app)

@app.before_first_request
def migrate():
  db.create_all()
  
@app.route('/')
def home():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True)