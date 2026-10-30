import os
import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI()

task_service_url = os.getenv(
    "TASK_SERVICE_URL",
    "http://127.0.0.1:8000"
)

@app.get("/statistics")
def get_statistics():

    try:
        response = httpx.get(
            f"{task_service_url}/tasks",
            timeout=5.0
        )
        response.raise_for_status()

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Task Service is unavailable"
        )
    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=502,
            detail="Task Service returned an error"
        )

    tasks = response.json()

    total = len(tasks)
    comp_task = 0

    for task in tasks:
        if task["completed"]:
            comp_task += 1

    pending = total - comp_task

    return {
        "total": total,
        "completed": comp_task,
        "pending": pending
    }