"""
Defines the user-related API routes

"""

from flask import jsonify, url_for, g, request
from flask_jwt_extended import create_access_token, create_refresh_token, \
    jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt

from grader import db, application
from grader.models import User
from grader.http_errors import BadContentTypeError, MissingUserError, InvalidUserCredentials
from grader.http_utilities import check_for_missing_params, error_response

@application.route('/api/users/register', methods=['POST'])
def register():
    if not request.is_json:
        raise BadContentTypeError('application/json')

    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    
    check_for_missing_params(username=username, password=password, email=email)
    
    if User.find_by_username(username) or User.find_by_email(email):
        return error_response(400, 'The user already exists!')

    user = User(username, password, email)

    db.session.add(user)
    db.session.commit() 

    user_json = user.to_json()
    access_token = create_access_token(identity=user_json)
    refresh_token = create_refresh_token(identity=user_json)

    return jsonify(status_code=201, message='User was created successfully!',  \
        access_token=access_token, refresh_token=refresh_token)

@application.route('/api/users/authenticate')
def authenticate():
    if request.authorization == None:
        raise MissingHeaderError('Authorization: Basic')

    username = request.authorization['username']
    password = request.authorization['password']

    user = User.find_by_username(username)
    if not user:
        raise MissingUserError(**user.to_api_safe_json())

    if not User.verify_hash(password, user.password_hash):
        raise InvalidUserCredentials(**user.to_api_safe_json())

    user_json = user.to_json()
    access_token = create_access_token(identity=user_json)
    refresh_token = create_refresh_token(identity=user_json)

    return jsonify(status_code=201, message='User was authenticated successfully!',  \
        access_token=access_token, refresh_token=refresh_token)

@application.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        return error_response(400, f'No user exists with username \'{username}\'')

    return jsonify(user.to_dict())

@application.route('/api/users/authenticate/refresh')
@jwt_refresh_token_required
def refresh_token():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    
    return jsonify(status_code=201, message='Successfully refreshed access token!', access_token=access_token)

@application.route('/api/test')
@jwt_required
def user_test():
    current_user_identity = get_jwt_identity()
    user = User.find_by_id(current_user_identity['id'])
    return jsonify(data=f'Hello, {user.username}')