from flask import Flask
from .routes.cafes import cafe_blueprint
from .extensions import db

def create_app():

	app = Flask(__name__)

	app.config.from_object('config.Config')

	db.init_app(app)

	app.register_blueprint(cafe_blueprint)

	return app