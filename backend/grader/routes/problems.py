"""
Defines the problem-related API routes

"""

from flask import jsonify, request
from flask_jwt_extended import jwt_required

from grader import db, application
from grader.models import Problem
from grader.utilities import setattr_not_none
from grader.http_errors import BadContentTypeError
from grader.http_utilities import error_response, check_for_missing_params

@application.route('/api/problem/<int:id>', methods=['GET'])
def get_problem(id):
    problem = Problem.find_by_id(id)
    if not problem:
        return error_response(404, 'The problem does not exist!')

    return  jsonify(status_code=200, id=id, problem=problem.to_json())

@application.route('/api/problem', methods=['POST'])
@jwt_required
def create_problem():
    if not request.is_json:
        raise BadContentTypeError('application/json')

    title = request.json.get('title')
    points = request.json.get('points')
    description = request.json.get('description')
    constraints = request.json.get('constraints')
    input_spec = request.json.get('input_spec')
    output_spec = request.json.get('output_spec')

    check_for_missing_params(title=title, points=points, 
        description=description, constraints=constraints, 
        input_spec=input_spec, output_spec=output_spec)

    problem = Problem(title, points, description, constraints, input_spec, output_spec)

    db.session.add(problem)
    db.session.commit()

    return jsonify(status_code=201, message='Problem was created successfully!', id=problem.id)

@application.route('/api/problem/<int:id>', methods=['PUT'])
@jwt_required
def update_problem(id):
    if not request.is_json:
        raise BadContentTypeError('application/json')

    title = request.json.get('title')
    points = request.json.get('points')
    description = request.json.get('description')
    constraints = request.json.get('constraints')
    input_spec = request.json.get('input_spec')
    output_spec = request.json.get('output_spec')

    problem = Problem.find_by_id(id)
    if not problem:
        return error_response(404, 'The problem does not exist!')

    setattr_not_none(problem, 'title', title)
    setattr_not_none(problem, 'points', points)
    setattr_not_none(problem, 'description', description)
    setattr_not_none(problem, 'constraints', constraints)
    setattr_not_none(problem, 'input_spec', input_spec)
    setattr_not_none(problem, 'output_spec', output_spec)

    db.session.commit()

    return jsonify(status_code=200, message='Problem was updated successfully!', id=id)

@application.route('/api/problem/<int:id>', methods=['DELETE'])
@jwt_required
def delete_problem(id):
    problem = Problem.find_by_id(id)
    if not problem:
        return error_response(404, 'The problem does not exist!')

    db.session.delete(problem)
    db.session.commit()

    return jsonify(status_code=200, message='Problem was deleted successfully!', id=id, problem=problem.to_json())
