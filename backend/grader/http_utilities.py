from grader import application
from grader.utilities import check_none, list_join

from flask import jsonify

def error_response(status_code, error_message, **kwargs):
    response = jsonify(status_code=status_code, error=error_message, **kwargs)
    response.status_code = status_code
    return response

class MissingParametersError(Exception):
    def __init__(self, empty_params):
        self.empty_params = empty_params

def check_for_missing_params(**kwargs):
    empty_params = check_none(**kwargs)
    if len(empty_params) == 0: return
    raise MissingParametersError(empty_params)