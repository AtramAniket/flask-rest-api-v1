from app.extensions import db
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class Cafe(db.Model):
	
	id: Mapped[int] = mapped_column(Integer, primary_key=True)

	name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

	map_url: Mapped[str] = mapped_column(String(500), nullable=False)

	img_url: Mapped[str] = mapped_column(String(500), nullable=False)

	location: Mapped[str] = mapped_column(String(500), nullable=False)

	can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
	
	has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)

	has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)

	has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)

	seats: Mapped[str] = mapped_column(String(255), nullable=False)
	
	coffee_price: Mapped[str] = mapped_column(String, nullable=False)

	def __repr__(self):
		return f"<Cafe {self.name}>"


	def to_dict(self):
		return {column.name: getattr(self, column.name) for column in self.__table__.columns}

	
	def get_model_columns(model):
		return {column.name for column in model.__table__.columns}