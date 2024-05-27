# app.py
import json

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restx import Api
from flask_restx import Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Recipe API', description='A simple Recipe API')

# Mock data for recipes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this in production
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Create a namespace for our API
ns = api.namespace('recipes', description='Recipe operations')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    preparation_steps = db.Column(db.Text, nullable=False)
    cooking_time = db.Column(db.Integer, nullable=False)
    serving_size = db.Column(db.Integer, nullable=False)


class RecipeCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=True)
    recipe_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

# Model for a Registration
recipe_registration_model = api.model('Registration', {
    'username': fields.String(description='username'),
    'email': fields.String(description='email'),
    'password': fields.String(description='password')
})

# Model for a Login
recipe_login_model = api.model('Login', {
    'username': fields.String(description='username'),
    'password': fields.String(description='password')
})


# Define a resource for listing all recipes
@ns.route('/')
class RecipeList(Resource):
    def get(self):
        """List all recipes"""
        recipes = db.Query(Recipe).all()
        result = []
        for recipe in recipes:
            result.append({
                'id': recipe.id,
                'title': recipe.title,
                'description': recipe.description,
                'ingredients': recipe.ingredients,
                'preparation_steps': recipe.preparation_steps,
                'cooking_time': recipe.cooking_time,
                'serving_size': recipe.serving_size,
                'category': recipe.category.name,
                'author': recipe.author.username
            })
        return jsonify(result), 200


# Define a resource for retrieving a specific recipe
@ns.route('/<int:id>')
class Recipes(Resource):
    def get(self, id):
        """Get details of a specific recipe"""
        recipe = db.session.query(Recipe).first()
        if not recipe:
            return {'message': 'Recipe not found'}, 404
        result = {
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'preparation_steps': recipe.preparation_steps,
            'cooking_time': recipe.cooking_time,
            'serving_size': recipe.serving_size,
            'category': recipe.category.name,
            'author': recipe.author.username
        }
        return json.dumps(result)


# Define a resource for validating user
@ns.route('/login')
@ns.expect(recipe_login_model)
class Login(Resource):
    def post(self):
        """ Validating user credentials"""
        data = request.json
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return {'message': 'Invalid username or password'}, 401
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200


@ns.route('/registration')
@ns.expect(recipe_registration_model)
class UserRegistration(Resource):
    def post(self):
        """ User Registration"""
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201


@ns.route('review-rating/<int:id>')
class ReviewRating(Resource):
    def get(self, id):
        recipe = db.session.query(Rating).filter_by(Rating.recipe_id == id).all()
        if not recipe:
            return {'message': 'Recipe not found'}, 404
        result = {
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'preparation_steps': recipe.preparation_steps,
            'cooking_time': recipe.cooking_time,
            'serving_size': recipe.serving_size,
            'category': recipe.category.name,
            'author': recipe.author.username
        }
        return json.dumps(result)


if __name__ == '__main__':
    app.run(debug=True)
