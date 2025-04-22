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
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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

    planets_favorites = Planets_favorites.query.filter_by(
        user_ID=user_id).all()
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

# Post para crear personas favoritas
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def create_favorite_people(people_id):
    request_body = request.get_json()

    current_user_id = 1

    new_favorite_people = People_favorites(
        user_ID=current_user_id, people_ID=people_id)
    # Verificar si el favorito ya existe
    existing_favorite = People_favorites.query.filter_by(
        user_ID=current_user_id, people_ID=people_id).first()
    if existing_favorite:
        return jsonify({"error": "Este personaje ya es un favorito"}), 400
    # Si no existe, agregar el nuevo favorito
    db.session.add(new_favorite_people)
    db.session.commit()
    return jsonify(new_favorite_people.serialize()), 201

# Post para crear un planeta favorito


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def create_favorite_planet(planet_id):
    request_body = request.get_json()

    current_user_id = 1

    new_favorite_planet = Planets_favorites(
        user_ID=current_user_id,
        planets_ID=planet_id
    )
    # Verificar si el favorito ya existe
    existing_favorite = Planets_favorites.query.filter_by(
        user_ID=current_user_id, planet_ID=planet_id).first()
    if existing_favorite:
        return jsonify({"error": "Este planeta ya es un favorito"}), 400
    # Si no existe, agregar el nuevo favorito
    db.session.add(new_favorite_planet)
    db.session.commit()

    return jsonify(new_favorite_planet.serialize()), 201

# DELETE para eliminar una persona favorita del usuario actual
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):

    current_user_id = 1 

    favorite_people = People_favorites.query.filter_by(
        user_ID=current_user_id,
        people_ID=people_id
    ).first()

    if favorite_people is None:
        return jsonify({"error": "Favorito no encontrado"}), 404

    db.session.delete(favorite_people)
    db.session.commit()

    return jsonify({"error": "Persona favorita eliminada"}), 200

# DELETE para eliminar un planeta favorito del usuario actual
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):

    current_user_id = 1 

    favorite_planet = Planets_favorites.query.filter_by(
        user_ID=current_user_id,
        planets_ID=planet_id
    ).first()

    if favorite_planet is None:
        return jsonify({"error": "Favorito no encontrado"}), 404

    db.session.delete(favorite_planet)
    db.session.commit()

    return jsonify({"error": "Planeta favorito eliminado"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
