from logging import Logger

from marshmallow import ValidationError
from bcrypt import checkpw


from apps.users.repositories import UserMongoRepository, AdminMongoRepository
from apps.users.schemas import UserSchema
from .exceptions import LoginSchemaValidationErrorException


class AuthUserUseCase:
    """
    Classe para autenticar um usuario
    """

    def __init__(self, repo: UserMongoRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def __validate(self, schema_input, input_params):
        try:
            data = schema_input.load(input_params)
            return data

        except ValidationError as err:
            raise LoginSchemaValidationErrorException(err.messages) from err

    def __to_output(self, user):
        # Realizo um dump dos dados de acordo com o modelo salvo
        schema = UserSchema()
        result = schema.dump(user)
        if self.logger:
            self.logger.info("auth.user.usecase", message="Render user output")
        return result

    def validate(self, schema_input, input_params):
        # Desserialização os dados postados ou melhor meu payload
        try:
            data = self.__validate(schema_input=schema_input, input_params=input_params)

            # supress password and confirm password before loggin payload
            # By according LGPD the cpf is a sensitive data too. So is necessary to be supressed
            if self.logger:
                self.logger.info("auth.user.usecase", message="Validate initial Payload")

            return data

        except ValidationError as err:
            if self.logger:
                self.logger.info("auth.user.usecase", message="Schema validation failed", errors=err.messages)

            raise err

    def get_user(self, data):
        # Buscamos nosso usuário pelo email
        return self.repo.get_user_by_email(data.get('email'))

    def check_user_is_active(self, user):
        if not user.is_active():
            raise Exception('Not allowed User')

    def check_password(self, user, data):
        if not checkpw(data.get('password').encode('utf-8'), user.password.encode('utf-8')):
            raise Exception('Password did not match')

    def execute(self, schema_input, input_params):
        data = self.validate(schema_input=schema_input, input_params=input_params)
        user = self.get_user(data=data)
        self.check_user_is_active(user=user)
        self.check_password(user=user, data=data)
        return self.__to_output(user=user)



class AdminAuthUserUseCase:
    """
    Classe para autenticar um admin
    """

    def __init__(self, repo: AdminMongoRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def __validate(self, schema_input, input_params):
        try:
            data = schema_input.load(input_params)
            return data

        except ValidationError as err:
            raise LoginSchemaValidationErrorException(err.messages) from err

    def __to_output(self, user):
        # Realizo um dump dos dados de acordo com o modelo salvo
        schema = UserSchema()
        result = schema.dump(user)
        if self.logger:
            self.logger.info("auth.admin.user.usecase", message="Render user output")
        return result

    def validate(self, schema_input, input_params):
        # Desserialização os dados postados ou melhor meu payload
        try:
            data = self.__validate(schema_input=schema_input, input_params=input_params)

            # supress password and confirm password before loggin payload
            # By according LGPD the cpf is a sensitive data too. So is necessary to be supressed
            if self.logger:
                self.logger.info("auth.admin.user.usecase", message="Validate initial Payload")

            return data

        except ValidationError as err:
            if self.logger:
                self.logger.info("auth.admin.user.usecase", message="Schema validation failed", errors=err.messages)

            raise err

    def get_admin(self, data):
        # Buscamos nosso usuário pelo email
        return self.repo.get_admin_by_email(data.get('email'))

    def check_admin_is_active(self, admin):
        if not admin.is_active():
            raise Exception('Not allowed Admin')

    def check_password(self, admin, data):
        if not checkpw(data.get('password').encode('utf-8'), admin.password.encode('utf-8')):
            raise Exception('Password did not match')

    def execute(self, schema_input, input_params):
        data = self.validate(schema_input=schema_input, input_params=input_params)
        admin = self.get_admin(data=data)
        self.check_admin_is_active(admin=admin)
        self.check_password(admin=admin, data=data)
        return self.__to_output(user=admin)
