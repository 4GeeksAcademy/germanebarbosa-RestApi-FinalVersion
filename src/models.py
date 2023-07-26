from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.db.Column(db.db.Integer, primary_key=True)
    email = db.db.Column(db.String(120), unique=True, nullable=False)
    password = db.db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active" : self.is_active
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.db.Column(db.db.Integer, primary_key=True, nullable=True)
    name = db.db.Column(db.String(250), nullable=True)
    population = db.db.Column(db.String(250))

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "planet_name": self.name,
            "population": self.population
        }

class People(db.Model):

    id = db.db.Column(db.db.Integer, primary_key=True, nullable=True)
    full_name = db.db.Column(db.String(250), nullable=True)
    age = db.db.Column(db.String(250))

    def __repr__(self):
        return '<People %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "people name": self.full_name,
            "age": self.age
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'

    id = db.Column(db.Integer, primary_key=True, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship(Planet)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    people = db.relationship(People)

    def __repr__(self):
        return '<Favorite_planets %r>' % self.user_id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id
        }