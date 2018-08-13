class BadContentTypeError(Exception):
    def __init__(self, expected_content_type):
        self.expected_content_type = expected_content_type

class MissingParametersError(Exception):
    def __init__(self, empty_params):
        self.empty_params = empty_params