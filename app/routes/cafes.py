import json
from random import randint
from app.extensions import db
from app.models.cafe import Cafe
from flask import Blueprint, jsonify

cafe_blueprint = Blueprint('Cafes', __name__)

@cafe_blueprint.route('/', methods = ['GET'])
def home():
	all_cafes = db.session.scalars(db.select(Cafe).order_by(Cafe.id)).all() 
	return jsonify({
		"status": "success", 
		"message": "Data is available",
		"data": [cafe.to_dict() for cafe in all_cafes]
		})


@cafe_blueprint.route('/random', methods = ['GET'])
def get_random_cafe():
	random_id = randint(1, 22)
	random_cafe = Cafe.query.get_or_404(random_id)
	print(random_id)
	print(random_cafe)
	return jsonify({
		"status": "success", 
		"message": "Data is available",
		"data": random_cafe.to_dict()})