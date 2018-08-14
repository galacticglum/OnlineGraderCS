def user_identity_kwargs_to_list(identity_kwargs):
    """
    Maps a set of keyword arguments that identify a user to
    a list of strings in the format "'key' (value='dict[key]')".

    :param identity_kwargs:
        a dictionary representing the keyword arguments to map.
    :returns:
        A list of strings in the format "'key' (value='dict[key]')".

    :usage:: 
        >>> user_identity_kwargs_to_list({'name':'bob', 'id':2})
        ["'name' (value='bob')", "'id' (value='2')"]

    """

    return [f'\'{key}\' (value=\'{identity_kwargs[key]}\')' for key in identity_kwargs if identity_kwargs[key] != None]

class BadContentTypeError(Exception):
    """
    Raised when an HTTP request sends an invalid content type.
    """

    def __init__(self, expected_content_type):
        self.expected_content_type = expected_content_type

class MissingParametersError(Exception):
    """
    Raised when an HTTP request is missing required parameters.
    """

    def __init__(self, empty_params):
        self.empty_params = empty_params

class MissingHeaderError(Exception):
    """
    Raised when an HTTP request is missing a required header.
    """

    def __init__(self, header):
        self.header = header
    
class MissingUserError(Exception):
    """
    Raised when the server cannot find the user given some identifier information.
    """

    def __init__(self, **identity_kwargs):
        self.identity_info = user_identity_kwargs_to_list(identity_kwargs)

class InvalidUserCredentials(Exception):
    """
    Raised when the provided user credentials are invalid.
    """

    def __init__(self, **identity_kwargs):
        self.identity_info = user_identity_kwargs_to_list(identity_kwargs)
