
from typing import Any, Mapping
import asyncio
import click
from flask.cli import with_appcontext
from flask_jwt_extended import create_access_token, create_refresh_token

from apps.extensions.logging import make_logger

from .schemas import CreateAdminInput, CreateUserInput, CreateUserOutput, UserSchema
from .use_case import CreateUserUseCase, GetUserByCpfCnpjUseCase
from .repositories import UserMongoRepository, AdminMongoRepository
from .exceptions import UserSchemaValidationErrorException, UserMongoNotUniqueException, UserMongoValidationErrorException

logger = make_logger(debug=True)


class CreateUserCommand:
    @staticmethod
    def save_in_database(payload: Mapping[str, Any], *_, **kwargs: dict[str, Any]):
        try:
            if logger:
                logger.info("create.user.command", message="Save in database operation")

            repo: UserMongoRepository = UserMongoRepository()
            schema = CreateUserInput()
            use_case: CreateUserUseCase = CreateUserUseCase(repo=repo, logger=logger)

            if logger:
                logger.info("create.user.command", message="Execute use case")

            output: CreateUserOutput = use_case.execute(schema_input=schema, input_params=payload)
            return output

        except Exception as exc:
            raise exc

    @staticmethod
    def send_user_to_queue(output):
        try:
            # your code is here
            print(output)
        except Exception as exc:
            raise exc

        if logger:
            logger.info("create.user.command", message="User was sent to queue")

    @staticmethod
    def another_operation(output):
        try:
            # your code is here
            print(output)
            if logger:
                logger.info("create.user.command", message="Another operation")
        except Exception as exc:
            raise exc

    @staticmethod
    def create_access_and_refresh_token(output):
        token = create_access_token(identity=output["email"])
        refresh_token = create_refresh_token(identity=output["email"])

        if logger:
            logger.info("create.user.command", message="Creating jwt tokens")

        return {
            'token': token,
            'refresh': refresh_token
        }

    @staticmethod
    def run(payload: Mapping[str, Any], *args, **kwargs: dict[str, Any]):
        output = CreateUserCommand.save_in_database(payload, *args, **kwargs)

        # use it with async function
        CreateUserCommand.send_user_to_queue(output)
        CreateUserCommand.another_operation(output)

        # gen tokens
        tokens = CreateUserCommand.create_access_and_refresh_token(output)
        output.update(tokens)

        return output


class CreateSuperUserCommand:
    @staticmethod
    def save_in_database(payload: Mapping[str, Any], *_, **kwargs: dict[str, Any]):
        try:
            if logger:
                logger.info("create.admin.user.command", message="Save in database operation")

            repo: AdminMongoRepository = AdminMongoRepository()
            schema = CreateAdminInput()
            use_case: CreateUserUseCase = CreateUserUseCase(repo=repo, logger=logger)
            if kwargs:
                payload.update({'roles': kwargs})

            if logger:
                logger.info("create.admin.user.command", message="Execute use case")

            output: CreateUserOutput = use_case.execute(schema_input=schema, input_params=payload)
            return output

        except Exception as exc:
            raise exc

    @staticmethod
    def run(payload: Mapping[str, Any], *args, **kwargs: dict[str, Any]):
        output = CreateSuperUserCommand.save_in_database(payload, *args, **kwargs)

        return output


# create command function
@click.command(name='createsuperuser')
@click.argument("name")
@click.argument("email")
@click.argument("password")
@with_appcontext
def createsuperuser(name: str, email: str, password: str):
    """
    Create a super user.
    Use: flask create [some-name] [some-email] [some-password]
    """

    payload = {'email': email, 'password': password, 'full_name': name}
    roles = {'superuser': True}

    try:
        output = CreateSuperUserCommand().run(payload=payload, **roles)
        click.echo(f"Superuser {output['email']} created")

    except UserSchemaValidationErrorException:
        click.echo(f"Superuser payload invalid")

    except UserMongoNotUniqueException:
        click.echo(f"Superuser {payload['email']} already exists")

    except UserMongoValidationErrorException:
        click.echo(f"Superuser {payload['email']} some fields are wrong")

    except Exception:
        click.echo(f"An error occurred. Superuser not created")


class GetUserByCpfCnpjCommand:
    @staticmethod
    def get_user_by_cpf_cnpj(current_user, cpf_cnpj, *_, **kwargs: dict[str, Any]):
        try:
            if logger:
                logger.info("users.GetUserByCpfCnpj.command", message="Get the user and check the password")

            repo: AdminMongoRepository = AdminMongoRepository()
            use_case: GetUserByCpfCnpjUseCase = GetUserByCpfCnpjUseCase(repo=repo, logger=logger)

            if logger:
                logger.info("users.GetUserByCpfCnpj.command", message="Execute use case")

            output: UserSchema = use_case.execute(current_user=current_user, cpf_cnpj=cpf_cnpj)
            return output

        except Exception as exc:
            raise exc

    @staticmethod
    def run(current_user, cpf_cnpj, *args, **kwargs: dict[str, Any]):
        output = GetUserByCpfCnpjCommand.get_user_by_cpf_cnpj(current_user=current_user, cpf_cnpj=cpf_cnpj, *args, **kwargs)

        return output
