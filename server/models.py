from config import db

class User(db.Model):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String)
	_password_hash = db.Column(db.String)
	image_url = db.Column(db.String)

	cellar_records = db.relationship('CellarRecord', back_populates='user')

	def __repr__(self):
		return f'<User {self.username}, {self.image_url}>'


class CellarRecord(db.Model):
	__tablename__ = "cellar_records"

	id = db.Column(db.Integer, primary_key=True)
	wine = db.Column(db.String)
	producer = db.Column(db.String)
	country = db.Column(db.String)
	vintage = db.Column(db.Integer)
	quantity = db.Column(db.Integer)
	tasting_notes = db.Column(db.String)

	user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
	user = db.relationship('User', back_populates='cellar_records')