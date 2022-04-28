import pathlib
import logging
from logging import Logger, StreamHandler, Handler
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta

from jose import jwt

from app.core.config import settings
from app.commons.constant import ALGORITHM


def setup_logger(
    name: str,
    level: int = logging.INFO,
    debug: bool = False,
    path: str = "./logs/app.log",
    max_bytes: int = 25 * 1024 * 1024,
    backup_count: int = 5
) -> Logger:
    if debug:
        level = logging.DEBUG
    logger = logging.getLogger(name)
    logger.setLevel(level)

    DEFAULT_FORMAT = (
        "%(asctime)s.%(msecs)03d [%(threadName)s] %(levelname)s "
        "%(pathname)s(%(funcName)s:%(lineno)d) - %(message)s"
    )
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(DEFAULT_FORMAT, datefmt=DATE_FORMAT)
    pathlib.Path(path).absolute().parent.mkdir(parents=True, exist_ok=True)
    handlers: list[Handler] = [StreamHandler(), RotatingFileHandler(path, maxBytes=max_bytes, backupCount=backup_count)]
    for handler in handlers:
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {
            "exp": exp, "nbf": now, "sub": email
        },
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt
