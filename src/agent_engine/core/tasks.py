import time
from typing import Any

from agent_engine.core.celery_app import celery_app


@celery_app.task(name="tasks.long_running_analysis")  # type: ignore[misc]
def long_running_analysis(session_id: str, data: dict[str, Any]) -> str:
    # simulate a heavy process (like reading 100 pages of PDF)
    time.sleep(10)
    return f"Analysis completed for session {session_id}. Ready for RAG!"


@celery_app.task  # type: ignore[misc]
def long_research_task(query: str) -> str:
    # here we will put the heavy logic that takes time
    time.sleep(5)
    return f"Deep research finished for: {query}"
