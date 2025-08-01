#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, CellarRecord, UserSchema, CellarRecordSchema

# GET /<resource> – paginated
# POST /<resource>
# PATCH /<resource>/<id>
# DELETE /<resource>/<id>

class Signup(Resource):
    def post(self):
        data = request.get_json()
        
        username = data.get('username')

if __name__ == '__main__':
    app.run(port=5555, debug=True)