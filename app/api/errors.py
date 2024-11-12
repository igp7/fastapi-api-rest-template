from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class UserExistsException(Exception):
    pass


class UsernameExistsException(Exception):
    pass


class UserNotExistsException(Exception):
    pass


class InactiveUserException(Exception):
    pass


class EmailExistsException(Exception):
    pass


class EmailNotExistsException(Exception):
    pass


class UnauthorizedException(Exception):
    pass


class NotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name


class PasswordErrorException(Exception):
    pass


class SamePasswordException(Exception):
    pass


class LoginErrorException(Exception):
    pass


class InvalidTokenException(Exception):
    pass


def register_error_handlers(app: FastAPI):
    @app.exception_handler(UserExistsException)
    def user_exists_exception_handler(request: Request, exc: UserExistsException):
        return JSONResponse(
            status_code=409,
            content={"message": "The user with this data already exists in the system."},
        )

    @app.exception_handler(UsernameExistsException)
    def user_exists_exception_handler(request: Request, exc: UsernameExistsException):
        return JSONResponse(
            status_code=409,
            content={"message": "The user with this username already exists in the system."},
        )


    @app.exception_handler(UserNotExistsException)
    def user_not_exists_exception_handler(request: Request, exc: UserNotExistsException):
        return JSONResponse(
            status_code=404,
            content={"message": "User not found."},
        )


    @app.exception_handler(InactiveUserException)
    def inactive_user_exception_handler(request: Request, exc: InactiveUserException):
        return JSONResponse(
            status_code=403,
            content={"message": "The user with this username is inactive in the system."},
        )


    @app.exception_handler(EmailExistsException)
    def email_exists_exception_handler(request: Request, exc: EmailExistsException):
        return JSONResponse(
            status_code=409,
            content={"message": "User with this email already exists."},
        )


    @app.exception_handler(EmailNotExistsException)
    def email_not_exists_exception_handler(request: Request, exc: EmailNotExistsException):
        return JSONResponse(
            status_code=409,
            content={"message": "User with this email not exists."},
        )


    @app.exception_handler(PasswordErrorException)
    def password_error_exception_handler(request: Request, exc: PasswordErrorException):
        return JSONResponse(
            status_code=401,
            content={"message": "Incorrect password."},
        )


    @app.exception_handler(SamePasswordException)
    def same_password_error_exception_handler(request: Request, exc: SamePasswordException):
        return JSONResponse(
            status_code=409,
            content={"message": "New password cannot be the same as the current one"},
        )


    @app.exception_handler(UnauthorizedException)
    def user_not_authorized_exception_handler(request: Request, exc: UnauthorizedException):
        return JSONResponse(
            status_code=403,
            content={"message": "The user doesn't have enough privileges"},
        )


    @app.exception_handler(LoginErrorException)
    def login_error_exception_handler(request: Request, exc: LoginErrorException):
        return JSONResponse(
            status_code=400,
            content={"message": "Incorrect username or password"},
        )


    @app.exception_handler(InvalidTokenException)
    def invalid_token_exception_handler(request: Request, exc: InvalidTokenException):
        return JSONResponse(
            status_code=400,
            content={"message": "Invalid token"},
        )


    @app.exception_handler(NotFoundException)
    def not_found_exception_handler(request: Request, exc: NotFoundException):
        return JSONResponse(
            status_code=404,
            content={"message": f"{exc.name} not found in the system."},
        )
