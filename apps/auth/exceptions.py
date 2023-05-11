class LoginSchemaValidationErrorException(Exception):

    def __init__(self, errors=None):
        self.msg = f"The input data is wrong"
        self.errors = errors

    def __str__(self):
        return self.msg
