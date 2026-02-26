from flask import Blueprint
from app.extensions import db

cafe_blueprint = Blueprint('Cafes', __name__)

@cafe_blueprint.route('/')
def home():
	return '<p>Hello from cafe api</p>'