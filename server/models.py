from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields

from config import db, bcrypt

# Model for wine cellar app users
class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, unique=True, nullable=False)
	_password_hash = db.Column(db.String)
	image_url = db.Column(db.String)

	cellar_records = db.relationship('CellarRecord', back_populates='user')

	@validates('username')
	def nomalize_username(self, key, value):
		return value.strip().lower()

	@hybrid_property
	def password_hash(self):
		raise AttributeError('Password hashes may not be viewed')
    
	@password_hash.setter
	def password_hash(self, password):
		password_hash = bcrypt.generate_password_hash(
			password.encode('utf-8'))
		self._password_hash = password_hash.decode('utf-8')
         
	def authenticate(self, password):
		return bcrypt.check_password_hash(
			self._password_hash, password.encode('utf-8'))

	def __repr__(self):
		return f'<User: {self.username}, {self.image_url}>'

# Model stores wine entries for users
class CellarRecord(db.Model):
	__tablename__ = 'cellar_records'

	id = db.Column(db.Integer, primary_key=True)
	wine = db.Column(db.String, nullable=False)
	grape = db.Column(db.String, nullable=False)
	country = db.Column(db.String, nullable=False)
	vintage = db.Column(db.Integer, nullable=False)
	quantity = db.Column(db.Integer, default=1)
	tasting_notes = db.Column(db.String, nullable=True)

	user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
	user = db.relationship('User', back_populates='cellar_records')

	@validates('vintage')
	def validate_vintage(self, key, vintage):
		if vintage is None:
			raise ValueError("Vintage must be provided.")
		if not isinstance(vintage, int):
			raise ValueError("Vitage must be an integer - YYYY.")
		if vintage < 1800 or vintage > 2026:
			raise ValueError('Vintage year needs to be a valid year between 1800 and current date.')
		return vintage 

	@validates('quantity')
	def validate_quantity(self, key, quantity):
		if quantity is None:
			raise ValueError("Quantity must be provided")
		if not isinstance(quantity, int):
			raise ValueError("Quantity must be an integer.")
		if quantity < 0:
			raise ValueError('Quantity cannot be a negative amount.')
		return quantity

	@validates('tasting_notes')
	def validate_tasting_notes(self, key, tasting_notes):
		if tasting_notes and len(tasting_notes) > 65:
			raise ValueError('Tasting notes cannot be longer than 65 characters.')
		return tasting_notes

	def __repr__(self):
		return f'<Cellar Record: {self.wine}, {self.grape}, {self.country}, {self.vintage}, {self.quantity}, {self.tasting_notes}>'

class UserSchema(Schema):
	id = fields.Integer()
	username = fields.String()
	image_url = fields.String()

	cellar_records = fields.List(fields.Nested(lambda: CellarRecordSchema(exclude=('user',))))

class CellarRecordSchema(Schema):
	id = fields.Integer()
	wine = fields.String()
	grape = fields.String()
	country = fields.String()
	vintage = fields.Integer()
	quantity = fields.Integer()
	tasting_notes = fields.String()

	user = fields.Nested(lambda: UserSchema(exclude=('cellar_records',)))