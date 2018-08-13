from grader import application

from grader.http_errors import MissingParametersError
from grader.utilities import check_none, list_join

from flask import jsonify

def error_response(status_code, error_message, **kwargs):
    response = jsonify(status_code=status_code, error=error_message, **kwargs)
    response.status_code = status_code
    return response

def check_for_missing_params(**kwargs):
    empty_params = check_none(**kwargs)
    if len(empty_params) == 0: return
    raise MissingParametersError(empty_params)