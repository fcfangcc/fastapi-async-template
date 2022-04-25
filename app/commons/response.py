from fastapi import HTTPException

LOGIN_ERROR = "LOGIN_ERROR"
NOT_FOUND = "NOT_FOUND"
NOT_PERMITTED = "NOT_PERMITTED"
DUPLICATED = 'DUPLICATED'


class ApiException(HTTPException):
    error_code = ""

    def __init__(self, status_code: int, message: str, error_code: str):
        super().__init__(status_code, message)
        self.error_code = error_code


class LoginException(ApiException):
    def __init__(self, message: str):
        super().__init__(400, message, LOGIN_ERROR)


class NotFoundException(ApiException):
    def __init__(self, message: str):
        super().__init__(400, message, NOT_FOUND)


class NotPermittedError(ApiException):
    def __init__(self, message: str):
        super().__init__(400, message, NOT_PERMITTED)


class DuplicatedError(ApiException):
    def __init__(self, message: str):
        super().__init__(400, message, DUPLICATED)
