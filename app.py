# server/app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plant_store.db'  # Use SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db = SQLAlchemy(app)

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Index Route: Get all plants
@app.route('/plants', methods=['GET'])
def get_all_plants():
    plants = Plant.query.all()
    return jsonify([plant.serialize() for plant in plants])

# Show Route: Get a specific plant by ID
@app.route('/plants/<int:id>', methods=['GET'])
def get_plant_by_id(id):
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({'message': 'Plant not found'}), 404
    return jsonify(plant.serialize())

# Create Route: Create a new plant
@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json()
    new_plant = Plant(
        name=data['name'],
        image=data['image'],
        price=data['price']
    )
    db.session.add(new_plant)
    db.session.commit()
    return jsonify(new_plant.serialize()), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)
