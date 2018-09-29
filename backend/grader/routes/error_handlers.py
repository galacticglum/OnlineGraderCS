from grader import application
from grader.utilities import list_join

from grader.http_errors import MissingParametersError, BadContentTypeError, \
    MissingHeaderError, MissingUserError, InvalidUserCredentials

from grader.http_utilities import error_response

@application.errorhandler(BadContentTypeError)
def __handle_bad_content_type_error(error):
    return error_response(415, 'Expected \'Content-Type: {0}\''.format(error.expected_content_type))

@application.errorhandler(MissingHeaderError)
def __handle_missing_header_error(error):
    return error_response(400, '\'{0} header is required by this request!\'' .format(error.header))

@application.errorhandler(MissingUserError)
def __handle_missing_user_error(error):
    invalid_identity_info = list_join(error.identity_info, 'and')
    return error_response(400, f'No user exists with {invalid_identity_info}!')

@application.errorhandler(InvalidUserCredentials)
def __handle_invalid_user_credentials(error):
    invalid_identity_info = list_join(error.identity_info, 'and')
    return error_response(400, f'Could not authenticate user with {invalid_identity_info}!')

@application.errorhandler(MissingParametersError)
def __handle_missing_params_error(error):
    PARAM_REQUIRED_MESSAGE = 'This field is required.'

    field_errors = {empty_param: PARAM_REQUIRED_MESSAGE for empty_param in error.empty_params}
    
    is_plural = len(error.empty_params) > 1
    conjunction_word = 'are' if is_plural  else 'is'
    s_ending = 's' if is_plural else ''

    missing_param_left = list_join(error.empty_params, 'and', lambda x: f'\'{x}\'')
    error_message = f'Parameter error: {missing_param_left} parameter{s_ending} {conjunction_word} missing.'
    return error_response(400, error_message, parameter_info=field_errors)