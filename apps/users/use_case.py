from logging import Logger

from marshmallow import ValidationError

from .exceptions import (
    UserMongoNotUniqueException, UserMongoValidationErrorException,
    UserSchemaValidationErrorException
)
from .repositories import UserMongoRepository, AdminMongoRepository
from .schemas import UserSchema
from .utils import generate_password


class CreateUserUseCase:
    """
    Classe para criar um usuario
    """

    def __init__(self, repo: UserMongoRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def __validate(self, schema_input, input_params):
        try:
            data = schema_input.load(input_params)
            return data

        except ValidationError as err:
            raise UserSchemaValidationErrorException(err.messages) from err

    def __to_output(self, user):
        # Realizo um dump dos dados de acordo com o modelo salvo
        schema = UserSchema()
        result = schema.dump(user)
        if self.logger:
            self.logger.info("create.user.usecase", message="Render user output")
        return result

    def __hashed_password(self, data):
        # Crio um hash da minha senha
        return generate_password(data['password'])

    def validate(self, schema_input, input_params):
        # Desserialização os dados postados ou melhor meu payload
        try:
            data = self.__validate(schema_input=schema_input, input_params=input_params)

            # supress password and confirm password before loggin payload
            # By according LGPD the cpf is a sensitive data too. So is necessary to be supressed
            if self.logger:
                self.logger.info("create.user.usecase", message="Validate initial Payload")

            return data

        except ValidationError as err:
            if self.logger:
                self.logger.info("create.user.usecase", message="Schema validation failed", errors=err.messages)

            raise err

    def encrypted_password(self, data):
        # encriptar a senha
        try:
            data['password'] = self.__hashed_password(data)
            if self.logger:
                self.logger.info("create.user.usecase", message="Encrypted password")
            return data

        except Exception as err:
            if self.logger:
                self.logger.info("create.user.usecase", message="Hashed password failed")
            raise err

    def save(self, data):
        try:
            model = self.repo.insert(data)
            if self.logger:
                self.logger.info("create.user.usecase", message="User saved")

            return model

        except UserMongoNotUniqueException as err:
            if self.logger:
                self.logger.info("create.user.usecase", message="User already saved")
            raise err

        except UserMongoValidationErrorException as err:
            if self.logger:
                self.logger.info("create.user.usecase", message="User fields and model are not equal",)
            raise err

        except Exception as err:
            if self.logger:
                self.logger.info("create.user.usecase", message="User not saved. Strange error")
            raise err

    def execute(self, schema_input, input_params):
        data = self.validate(schema_input=schema_input, input_params=input_params)
        data = self.encrypted_password(data=data)
        model = self.save(data=data)

        return self.__to_output(user=model)


class GetUserByCpfCnpjUseCase:
    def __init__(self, repo: AdminMongoRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def get_admin(self, email):
        # Buscamos nosso usuário pelo email
        if self.logger:
            self.logger.info("users.GetUserByCpfCnpjUseCase.usecase", message="Get admin current user")

        return self.repo.get_admin_by_email(email)

    def check_admin_is_active(self, admin):
        if self.logger:
            self.logger.info("users.GetUserByCpfCnpjUseCase.usecase", message="Check admin is active")

        if not admin.is_active():
            if self.logger:
                self.logger.info("users.GetUserByCpfCnpjUseCase.usecase", message="The admin is not activate")

            raise Exception('Not allowed Admin')

    def get_user_by_cpf_cnpj(self, cpf_cnpj):
        # Buscamos nosso usuário pelo email
        if self.logger:
            self.logger.info("users.GetUserByCpfCnpjUseCase.usecase", message="Get the user by cpf and cnpj")

        return self.repo.get_user_by_cpf_cnpj(cpf_cnpj=cpf_cnpj)

    def __to_output(self, user):
        # Realizo um dump dos dados de acordo com o modelo salvo
        schema = UserSchema()
        result = schema.dump(user)

        if self.logger:
            self.logger.info("users.GetUserByCpfCnpjUseCase.usecase", message="Render user output")

        return result

    def execute(self, current_user, cpf_cnpj, *args, **kargs):
        admin = self.get_admin(email=current_user)
        self.check_admin_is_active(admin=admin)
        user = self.get_user_by_cpf_cnpj(cpf_cnpj=cpf_cnpj)
        return self.__to_output(user=user)
