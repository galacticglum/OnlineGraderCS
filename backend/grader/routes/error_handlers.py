from grader import application
from grader.utilities import list_join
from grader.http_utilities import MissingParametersError, error_response

__param_required_message = 'This parameter is required.'

@application.errorhandler(MissingParametersError)
def handle_missing_params_error(error):
    field_errors = {empty_param:__param_required_message for empty_param in error.empty_params}
    
    is_plural = len(error.empty_params) > 1
    conjunction_word = 'are' if is_plural  else 'is'
    s_ending = 's' if is_plural else ''

    missing_param_left = list_join(error.empty_params, 'and', lambda x: f'\'{x}\'')
    error_message = f'Parameter error: {missing_param_left} parameter{s_ending} {conjunction_word} missing.'
    return error_response(400, error_message, parameter_info=field_errors)