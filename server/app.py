#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# ✅ CREATE TABLES FOR TESTS
with app.app_context():
    db.create_all()
    
    # Seed data if no earthquakes exist
    if Earthquake.query.count() == 0:
        db.session.add(Earthquake(magnitude=9.5, location="Chile", year=1960))
        db.session.add(Earthquake(magnitude=9.2, location="Alaska", year=1964))
        db.session.add(Earthquake(magnitude=8.6, location="Alaska", year=1946))
        db.session.add(Earthquake(magnitude=8.5, location="Banda Sea", year=1934))
        db.session.add(Earthquake(magnitude=8.4, location="Chile", year=1922))
        db.session.commit()


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)


# ✅ GET /earthquakes/<id>
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    earthquake = db.session.get(Earthquake, id)

    if earthquake:
        return jsonify(earthquake.to_dict()), 200
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404


# ✅ GET /earthquakes/magnitude/<magnitude>
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(
        Earthquake.magnitude >= magnitude
    ).all()

    return jsonify({
        "count": len(earthquakes),
        "quakes": [quake.to_dict() for quake in earthquakes]
    }), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
