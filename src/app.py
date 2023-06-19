"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from pickle import GET
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite
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

# -----GET------
@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all() #devuelve una lista[] del modelo a devolver, es decir el modelo.
    result = list(map(lambda item: item.serialize(), all_users))
    return jsonify(result), 200

@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()
    result = list(map(lambda item: item.serialize(), all_people))
    return jsonify(result), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):

    people = People.query.filter_by(id = people_id).first()
    result = list(map(lambda item: item.serialize(), people))
       
    return jsonify(result), 200

@app.route('/planet', methods=['GET'])
def get_planet():
    all_planet = Planet.query.all()
    result = list(map(lambda item: item.serialize(), all_planet))
    return jsonify(result), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):

    planet = Planet.query.filter_by(id = planet_id).first()
    result = list(map(lambda item: item.serialize(), planet))
       
    return jsonify(result), 200

@app.route('/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):

    user_favorites = Favorite.query.filter_by(id = user_id).all()
    if not user_favorites:
        return {"No favorite"}
    
    serialized_favorites = [{
        "planet_id" : favorite.planet.id,
        "planet_name": Planet.query.get(favorite.planet_id).name,
        "people_id" : favorite.people_id,
        "people_name": People.query.get(favorite.planet_id).name
    } for favorite in user_favorites]
       
    return jsonify(serialized_favorites), 200

# -----POST------

@app.route('/<int:user_id>/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(user_id, people_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "El usuario no existe"}, 404
    
    people = People.query.get(people_id)
    if not people:
        return {"error": "El personaje no existe"}, 404
    
    new_fav_people = Favorite(user_id=user_id,people_id=people_id)
    db.session.add(new_fav_people)
    db.session.commit()
    response_body = {
        "msg": "Favorite people added correctly"
    }
    
    return jsonify(response_body),200

@app.route('/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):

    user = User.query.get(user_id)
    if not user:
        return {"error": "El usuario no existe"}, 404
    
    planet = Planet.query.get(planet_id)
    if not planet:
        return {"error": "El planeta no existe"}, 404
    
    new_fav_planet = Favorite(user_id=user_id,planet_id=planet_id)
    db.session.add(new_fav_planet)
    db.session.commit()
    response_body = {
        "msg": "Favorite planet added correctly"
    }
    
    return jsonify(response_body),200

@app.route('/people', methods=['POST'])
def add_people():
    body = request.get_json()
    people = People(
        name=body['name'],
        age=body['age']
    )
    db.session.add(people)
    db.session.commit()
    response_body = {
    "msg": "People added correctly"
    }
    return jsonify(response_body),200


@app.route('/planets', methods=['POST'])
def planetsPost():
    body = request.get_json()
    planets = Planet(
        name=body['name'],
        population=body['population']
    )
    db.session.add(planets)
    db.session.commit()
    response_body = {
        "msg": "Planets added correctly"
    }
    return jsonify(response_body),200

# -----DELETE------

@app.route('/<int:user_id>/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(user_id, people_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "The user does not exist"}, 404
    
    people = People.query.get(people_id)
    if not people:
        return {"error": "The people does not exist"}, 404
    
    delete_fav_people = Favorite(user_id=user_id,people_id=people_id)
    
    db.session.delete(delete_fav_people)
    db.session.commit()

    return jsonify("The person has been successfully deleted"), 200

@app.route('/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "The user does not exist"}, 404
    
    planet = Planet.query.get(planet_id)
    if not planet:
        return {"error": "The planet does not exist"}, 404
    
    delete_fav_planet = Favorite(user_id=user_id,planet_id=planet_id)
    
    db.session.delete(delete_fav_planet)
    db.session.commit()

    return jsonify("The planet has been successfully deleted"), 200

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):

    people = People.query.filter_by(id = people_id).first()
    db.session.delete(people)
    db.session.commit()

    return jsonify("The people has been successfully deleted"), 200

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):

    planet = Planet.query.filter_by(id = planet_id).first()
    db.session.delete(planet)
    db.session.commit()

    return jsonify("The planet has been successfully deleted"), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

