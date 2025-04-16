"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, People, People_favorites, Planets_favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/users', methods=['GET'])
def get_users():
    print("Received a GET request to /users")  # Mensaje de log
    users = User.query.all()
    print("Users found:", users)  # Log de los usuarios encontrados
    users = list(map(lambda x: x.serialize(), users))
    return jsonify(users), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    planets_favorites = Planets_favorites.query.filter_by(user_ID=user_id).all()
    people_favorites = People_favorites.query.filter_by(user_ID=user_id).all()

    favorites_data = {
        "planets": [pf.serialize() for pf in planets_favorites],
        "people": [pf.serialize() for pf in people_favorites]
    }

    return jsonify(favorites_data), 200


@app.route('/people', methods=['GET'])
def get_people():
    print("Received a GET request to /people")  # Mensaje de log
    people = People.query.all()
    print("People found:", people)  # Log de los usuarios encontrados
    people = list(map(lambda x: x.serialize(), people))
    return jsonify(people), 200

@app.route('/people/<int:id>', methods=['GET'])
def get_people_by_id(id):
    people = People.query.get(id)
    if not people:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(people.serialize()), 200


@app.route('/planets', methods=['GET'])
def get_planet():
    print("Received a GET request to /planets")  # Mensaje de log
    planets = Planets.query.all()
    print("Planets found:", planets)  # Log de los usuarios encontrados
    planets = list(map(lambda x: x.serialize(), planets))
    return jsonify(planets), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_planets_by_id(id):
    planets = Planets.query.get(id)
    if not planets:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planets.serialize()), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
