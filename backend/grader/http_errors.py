def user_identity_kwargs_to_list(identity_kwargs):
    return [f'\'{key}\' ({identity_kwargs[key]})' for key in identity_kwargs if identity_kwargs[key] != None]

class BadContentTypeError(Exception):
    def __init__(self, expected_content_type):
        self.expected_content_type = expected_content_type

class MissingParametersError(Exception):
    def __init__(self, empty_params):
        self.empty_params = empty_params

class MissingHeaderError(Exception):
    def __init__(self, header):
        self.header = header
    
class MissingUserError(Exception):
    def __init__(self, **identity_kwargs):
        self.identity_info = user_identity_kwargs_to_list(identity_kwargs)

class InvalidUserCredentials(Exception):
    def __init__(self, **identity_kwargs):
        self.identity_info = user_identity_kwargs_to_list(identity_kwargs)
