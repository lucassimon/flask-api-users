class UserMongoNotUniqueException(Exception):
    pass


class UserMongoValidationErrorException(Exception):
    pass


class UserMongoFieldsDoesNotExistException(Exception):
    pass


class UserMongoDoesNotExistException(Exception):
    pass


class UserMongoMultipleObjectsReturnedException(Exception):
    pass


class UserSchemaValidationErrorException(Exception):

    def __init__(self, errors=None):
        self.msg = f"The input data is wrong"
        self.errors = errors

    def __str__(self):
        return self.msg
