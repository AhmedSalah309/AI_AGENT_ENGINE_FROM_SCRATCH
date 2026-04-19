import os

from celery import Celery

# define the Celery and link it to Redis that we created in Docker
celery_app = Celery(
    "agent_tasks",
    broker=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://redis:6379/0"),
)

celery_app.conf.task_routes = {
    "agent_engine.tasks.*": {"queue": "agent_queue"},
}
