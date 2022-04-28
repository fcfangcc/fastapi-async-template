import logging
from arq import cron
from arq.connections import RedisSettings

from app.main import create_app
from app.core.config import settings
from app.utils import setup_logger

logger = logging.getLogger(__name__)


async def startup(ctx: dict) -> None:
    create_app()
    setup_logger("arq")
    logger.info("arq starting...")


async def shutdown(ctx: dict) -> None:
    logger.info("arq shutdown...")


async def task_demo(ctx: dict, input1: str) -> None:
    print(f"task_demo {ctx['job_id'] } input1={input1}")


async def cron_demo(ctx: dict) -> None:
    print(f"cron_demo {ctx['job_id']}")


class WorkerSettings:
    redis_settings = RedisSettings.from_dsn(settings.ARQ_REDIS_DSN)
    max_tries = 10
    queue_name = settings.ARQ_QUEUE_NAME

    functions = [task_demo]

    on_startup = startup

    on_shutdown = shutdown

    cron_jobs = [
        cron(cron_demo, second=10, run_at_startup=True),  # type: ignore
    ]
