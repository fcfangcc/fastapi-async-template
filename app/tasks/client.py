from typing import Optional, Any

from arq import create_pool
from arq.jobs import Job
from arq.connections import ArqRedis, RedisSettings


class ArqClient:
    pool: Optional[ArqRedis] = None

    async def create_pool(self, dns: str, queue_name: str) -> None:
        self.pool = await create_pool(RedisSettings.from_dsn(dns), default_queue_name=queue_name)

    async def close_pool(self) -> None:
        if self.pool:
            await self.pool.close()

    async def _enqueue_job(self, function_name: str, **kwargs: Any) -> Optional[Job]:
        if self.pool:
            return await self.pool.enqueue_job(function_name, **kwargs)
        raise ValueError("pool is none.please init arq client.")

    async def notify_cron_task(self, task_name: str) -> Optional[Job]:

        return await self._enqueue_job(f'cron:{task_name}')

    async def task_demo(self, input1: str) -> Optional[Job]:
        return await self._enqueue_job('task_demo', input1=input1)


arq_client = ArqClient()
