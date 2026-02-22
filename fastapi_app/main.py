# fastapi-app/main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db import Base, engine, get_db
from schemas.task import TaskCreate, TaskUpdate, TaskRead
from crud.task import (
    get_tasks,
    get_task,
    create_task,
    update_task,
    delete_task,
)

import models.task  # Base に Task モデルを登録するため必要


# ---------------------------------------
#  DB 初期化（テーブル自動生成）
# ---------------------------------------
Base.metadata.create_all(bind=engine)

app = FastAPI()


# ---------------------------------------
#  CORS 設定（Vue 8080 を許可）
# ---------------------------------------
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------
#  READ 全件
# ---------------------------------------
@app.get("/tasks", response_model=list[TaskRead])
def read_tasks(db: Session = Depends(get_db)):
    return get_tasks(db)


# ---------------------------------------
# READ 1件
# ---------------------------------------
@app.get(
    "/tasks/{task_id}",
    response_model=TaskRead,
    responses={
        404: {"description": "Task not found"},
    },
)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# ---------------------------------------
# CREATE
# ---------------------------------------
@app.post(
    "/tasks",
    response_model=TaskRead,
    responses={
        422: {"description": "Validation error"},
    },
)
def create_task_endpoint(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task)


# ---------------------------------------
# UPDATE
# ---------------------------------------
@app.put(
    "/tasks/{task_id}",
    response_model=TaskRead,
    responses={
        404: {"description": "Task not found"},
        422: {"description": "Validation error"},
    },
)
def update_task_endpoint(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
):
    updated = update_task(db, task_id, task)
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


# ---------------------------------------
# DELETE
# ---------------------------------------
@app.delete(
    "/tasks/{task_id}",
    responses={
        404: {"description": "Task not found"},
    },
)
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    ok = delete_task(db, task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"result": "ok"}