from typing import Any

from fastapi import APIRouter, Body

from app.tasks.client import arq_client

router = APIRouter()


@router.post("/tasks/cron")
async def notify_cron(task_name: str = Body(..., embed=True)) -> Any:
    job = await arq_client.notify_cron_task(task_name)
    return job.job_id if job else None


@router.post("/tasks/task")
async def notify_task(input1: str = Body(..., embed=True)) -> Any:
    job = await arq_client.task_demo(input1)
    return job.job_id if job else None