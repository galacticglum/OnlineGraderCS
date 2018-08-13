from flask import jsonify, url_for, g, request
from grader import db, application, token_auth, basic_auth, auth

from grader.models import User
from grader.http_errors import BadContentTypeError
from grader.http_utilities import check_for_missing_params, error_response

@token_auth.verify_token
def __verify_token(token):
    user = User.verify_auth_token(token)
    if not user:
        return False

    g.user = user
    return True

@basic_auth.verify_password
def __verify_basic_auth(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False

    g.user = user
    return True

@application.route('/api/users/register', methods=['POST'])
def register():
    if not request.is_json:
        raise BadContentTypeError('application/json')

    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    
    check_for_missing_params(username=username, password=password, email=email)
    
    if User.query.filter_by(username=username).first() is not None or \
        User.query.filter_by(email=email).first() is not None:
        return error_response(400, 'The user already exists!')

    user = User(username, password, email)
    db.session.add(user)
    db.session.commit()

    user_location = url_for('get_user', id=user.id, _external=True)
    return jsonify(username=user.username, status_code=201, Location=user_location)

@application.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        return error_response(400, 'The user already exists!')

    return jsonify(user.to_dict())

@application.route('/api/users/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify(token=token.decode('ascii'))

@application.route('/api/test')
@auth.login_required
def user_test():
    return jsonify(data=f'Hello, {g.user.username}')