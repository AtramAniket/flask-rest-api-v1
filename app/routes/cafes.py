import json
from random import randint
from app.extensions import db
from app.models.cafe import Cafe
from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, jsonify, request

cafe_blueprint = Blueprint('Cafes', __name__)

@cafe_blueprint.route('/all', methods = ['GET'])
def get_all_cafes():
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


@cafe_blueprint.route('/search', methods = ['POST'])
def get_cafe():
	incoming_params = request.json
	cafe_location = incoming_params["location"]
	print(cafe_location)
	result = db.session.scalar(db.select(Cafe).where(Cafe.location == cafe_location))
	if result:
		return jsonify({
			"status": "success", 
			"message": "Data is available",
			"data": result.to_dict() }), 200
	else:
		return jsonify({
			"status": "Failure", 
			"message": "Sorry no data available", }), 404


@cafe_blueprint.route('/add', methods = ['POST'])
def add_cafe():
	incoming_params = request.json
	name = incoming_params["name"]
	map_url = incoming_params["map_url"]
	img_url = incoming_params["img_url"]
	location = incoming_params["location"]
	can_take_calls = incoming_params["can_take_calls"]
	has_toilet = incoming_params["has_toilet"]
	has_wifi = incoming_params["has_wifi"]
	has_sockets = incoming_params["has_sockets"]
	seats = incoming_params["seats"]
	coffee_price = incoming_params["coffee_price"]

	

	try:
		
		new_cafe = Cafe(name=name,map_url=map_url,img_url=img_url,location=location,can_take_calls=can_take_calls,has_toilet=has_toilet,has_wifi=has_wifi,has_sockets=has_sockets,seats=seats,coffee_price=coffee_price)
		
		db.session.add(new_cafe)
		
		db.session.commit()
		
		return jsonify({
			"status": "Success", 
			"message": "Data added successfully", }), 200
	
	except SQLAlchemyError as e:
		
		db.session.rollback()
		
		return jsonify({
			"status": "Failure",
			"message": "Database eror", 
			"error": str(e) }), 400

	except Exception as e:
		
		db.session.rollback()
		
		return jsonify({
			"status": "Failure", 
			"message": "Unexpected error", 
			"error": str(e) }), 400


@cafe_blueprint.route('/edit/<int:cafe_id>', methods = ['PATCH'])
def edit_cafe(cafe_id):

	cafe_to_edit = Cafe.query.get(cafe_id)

	if not cafe_to_edit:
		return jsonify({
			"status": 404, 
			"message": f"No cafe found for id {cafe_id}",}), 404

	incoming_params = request.json or {}

	valid_columns = Cafe.get_model_columns(Cafe)

	# avoind primary key from being edited
	valid_columns.discard("id")

	try:
		
		for key, value in incoming_params.items():
			setattr(cafe_to_edit, key, value)
		
		db.session.commit()
		
		return jsonify({
			"status": "Success", 
			"message": "Data updated successfully", }), 200
	
	except SQLAlchemyError as e:
		
		db.session.rollback()
		
		return jsonify({
			"status": "Failure",
			"message": "Database eror", 
			"error": str(e) }), 400


@cafe_blueprint.route('/delete/<int:cafe_id>', methods = ['DELETE'])
def delete_cafe(cafe_id):

	cafe_to_delete = Cafe.query.get(cafe_id)

	if not cafe_to_delete:
		return jsonify({
			"status": 404, 
			"message": f"No cafe found for id {cafe_id}",}), 404

	try:
		
		db.session.delete(cafe_to_delete)
		db.session.commit()
		
		return jsonify({
			"status": "Success", 
			"message": "Cafe deleted successfully", }), 200
	
	except SQLAlchemyError as e:
		
		db.session.rollback()
		
		return jsonify({
			"status": "Failure",
			"message": "Database eror", 
			"error": str(e) }), 400
