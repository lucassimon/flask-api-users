
from typing import Any, Mapping
import asyncio
import click
from flask.cli import with_appcontext
from flask_jwt_extended import create_access_token, create_refresh_token

from apps.extensions.logging import make_logger
from apps.users.repositories import UserMongoRepository, AdminMongoRepository
from apps.users.schemas import UserSchema
from .schemas import LoginSchema
from .use_case import AuthUserUseCase, AdminAuthUserUseCase

logger = make_logger(debug=True)


class AuthAdminUsersCommand:
    @staticmethod
    def get_user_and_check_password(payload: Mapping[str, Any], *_, **kwargs: dict[str, Any]):
        try:
            if logger:
                logger.info("auth.admin.user.command", message="Get the user and check the password")

            repo: AdminMongoRepository = AdminMongoRepository()
            schema = LoginSchema()
            use_case: AdminAuthUserUseCase = AdminAuthUserUseCase(repo=repo, logger=logger)
            if kwargs:
                payload.update({'roles': kwargs})

            if logger:
                logger.info("auth.admin.user.command", message="Execute use case")

            output: UserSchema = use_case.execute(schema_input=schema, input_params=payload)
            return output

        except Exception as exc:
            raise exc

    @staticmethod
    def create_access_and_refresh_token(output):
        token = create_access_token(identity=output["email"])
        refresh_token = create_refresh_token(identity=output["email"])

        if logger:
            logger.info("auth.admin.user.command", message="Creating jwt tokens")

        return {
            'token': token,
            'refresh': refresh_token
        }

    @staticmethod
    def run(payload: Mapping[str, Any], *args, **kwargs: dict[str, Any]):
        output = AuthAdminUsersCommand.get_user_and_check_password(payload, *args, **kwargs)
        # gen tokens
        tokens = AuthAdminUsersCommand.create_access_and_refresh_token(output)
        output.update(tokens)

        return output



class AuthUsersCommand:
    @staticmethod
    def get_user_and_check_password(payload: Mapping[str, Any], *_, **kwargs: dict[str, Any]):
        try:
            if logger:
                logger.info("auth.user.command", message="Get the user and check the password")

            repo: UserMongoRepository = UserMongoRepository()
            schema = LoginSchema()
            use_case: AuthUserUseCase = AuthUserUseCase(repo=repo, logger=logger)
            if kwargs:
                payload.update({'roles': kwargs})

            if logger:
                logger.info("auth.user.command", message="Execute use case")

            output: AuthUserUseCase = use_case.execute(schema_input=schema, input_params=payload)
            return output

        except Exception as exc:
            raise exc

    @staticmethod
    def create_access_and_refresh_token(output):
        token = create_access_token(identity=output["email"])
        refresh_token = create_refresh_token(identity=output["email"])

        if logger:
            logger.info("auth.user.command", message="Creating jwt tokens")

        return {
            'token': token,
            'refresh': refresh_token
        }

    @staticmethod
    def run(payload: Mapping[str, Any], *args, **kwargs: dict[str, Any]):
        output = AuthUsersCommand.get_user_and_check_password(payload, *args, **kwargs)
        # gen tokens
        tokens = AuthUsersCommand.create_access_and_refresh_token(output)
        output.update(tokens)

        return output
