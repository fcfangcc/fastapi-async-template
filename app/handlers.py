from typing import Any, Optional

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from app.commons.response import ApiException


VALIDATION_ERROR = "VALIDATION_ERROR"


def json_error(err_code: str, msg: Optional[str] = None, status_code: int = 400, **kwargs: Any) -> JSONResponse:
    detial = {"code": err_code, "message": msg} | kwargs
    error = {'ok': False, "detail": detial}
    return JSONResponse(content=error, status_code=status_code)


def init_error_handles(app: FastAPI) -> None:
    @app.exception_handler(ApiException)
    async def api_exception_handler(_: Request, exc: ApiException) -> JSONResponse:
        return json_error(exc.error_code, exc.detail, exc.status_code)

    @app.exception_handler(RequestValidationError)
    async def valid_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        try:
            params: Any = {}
            for i in exc.errors():
                params[i.get('loc')[-1]] = i.get('msg', None)
        except Exception:  # pragma: no cover
            params = {"error": exc.errors()}
        return json_error(VALIDATION_ERROR, "params error", 400, params=params)
