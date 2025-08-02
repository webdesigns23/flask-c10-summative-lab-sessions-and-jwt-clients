#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, CellarRecord, UserSchema, CellarRecordSchema

# Protected Routes
@app.before_request
def check_if_logged_in():
    open_access_list = ['signup', 'check_session','login']
    
    if request.endpoint not in open_access_list and not session.get('user_id'):
        return {'error': 'Unauthorized Access'}, 401

# User Account
class Signup(Resource):
    def post(self):
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')
        image_url = data.get('image_url')
        
        user = User(username = username, image_url = image_url)
        user.password_hash = password
        
        try:
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return UserSchema().dump(user), 201
        except IntegrityError:
            return {'error': 'Unprocessable Entity'}, 422
        
class CheckSession(Resource):
    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id == session['user_id']).first()
            return UserSchema().dump(user), 200
        return {'error': 'User is Not Logged In'}, 401
    
class Login(Resource):
    def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password']

        user = User.query.filter(User.username == username).first()

        if user and user.authenticate(password):
            session['user_id'] = user.id
            return UserSchema().dump(user), 200

        return {'error': 'Unauthorized'}, 401

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session.pop('user_id', None)
            return {}, 204
        return {'error': 'User is Already Logged Out'}, 401
    
# Create, Read, Add Pagination
class CellarRecordIndex(Resource):
    # GET /<resource> – paginated
    def get(self):
        if not session.get('user_id'):
            return {'error': 'User is Logged Out'}, 401
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        pagination = CellarRecord.query.paginate(page=page, per_page=per_page, error_out=False)
        cellar_records = pagination.items
        return {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'total_pages': pagination.pages,
            'items': [CellarRecordSchema().dump(cr) for cr in cellar_records]
		}, 200
	
	# POST /<resource>
    def post(self):
        if not session.get('user_id'):
            return {'error': 'User is Logged Out'}, 401

        data = request.get_json()

        try:
            cellar_record = CellarRecord(
                wine = data.get('wine'),
				grape = data.get('grape'),
				country = data.get('country'),
				vintage = data.get('vintage'),
				quantity = data.get('quantity'),
				tasting_notes = data.get('tasting_notes'),
                user_id=session['user_id']
            )
            db.session.add(cellar_record)
            db.session.commit()
            return CellarRecordSchema().dump(cellar_record), 201

        except ValueError:
            db.session.rollback()  
            return {'error': 'Unable to Process, Incorrect Value'}, 422

        except IntegrityError:
            db.session.rollback()
            return {'error': 'Unable to Process, Data Invalid'}, 422     

# Update, Delete by Id
class CellarRecordId(Resource):
    # PATCH /<resource>/<id>
    def patch(self, id):
        if not session.get('user_id'):
            return {'error': 'User is Logged Out'}, 401
        
        data = request.get_json()
        cellar_record = CellarRecord.query.filter(CellarRecord.id == id).first()
        
        if not cellar_record or cellar_record.user_id != session['user_id']:
            return {'error': 'Forbidden, Unable to Update'}, 403
        
		# Update values
        if 'quantity' in data:
            cellar_record.quantity = data['quantity']
        if 'tasting_notes' in data:
            cellar_record.tasting_notes = data['tasting_notes']
            
        db.session.commit()
        return CellarRecordSchema().dump(cellar_record), 200
	
	# DELETE /<resource>/<id>
    def delete(self, id):
        if not session.get('user_id'):
            return {'error': 'User is Logged Out'}, 401
        
        cellar_record = CellarRecord.query.filter(CellarRecord.id == id).first()
        
        if not cellar_record or cellar_record.user_id != session['user_id']:
            return {'error': 'Forbidden, Unable to Delete'}, 403
        else:
            db.session.delete(cellar_record)
            db.session.commit()
            return {}, 204
	
      

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(CellarRecordIndex, '/cellar_records', endpoint='cellar_records')
api.add_resource(CellarRecordId, '/cellar_record/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)