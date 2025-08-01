#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, CellarRecord, UserSchema, CellarRecordSchema

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
        return {'error': 'User is not logged in'}, 401
    
class Login(Resource):
    def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password']

        user = User.query.filter(User.username == username).first()

        if user and user.authenticate(password):
            session['user_id'] = user.id
            return UserSchema().dump(user), 200

        return {'error': '401 Unauthorized'}, 401

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id'] = None
            return {}, 204
        return {'error': 'User is already logged out'}, 401
    
# CRUD
class CellarRecordIndex(Resource):
    # GET /<resource> – paginated
    def get(self):
        if session.get('user_id'):
            cellar_records = [CellarRecordSchema().dump(cr) for cr in CellarRecord.query.all()]
            return cellar_records, 200    
        return {'error': 'User is already logged out'}, 401  
	
	# POST /<resource>
    def post(self):
        if not session.get('user_id'):
                return {'error': 'User is already logged out'}, 401

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

        except ValueError as error:
            db.session.rollback()  
            return {'error': str(error)}, 422

        except IntegrityError:
            db.session.rollback()
            return {'error': 'Unable to process, invalid data'}, 422     
    
	# PATCH /<resource>/<id>
	
	# DELETE /<resource>/<id>    

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(CellarRecordIndex, '/cellar_records', endpoint='cellar_records')

if __name__ == '__main__':
    app.run(port=5555, debug=True)