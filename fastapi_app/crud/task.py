# fastapi_app/crud/task.py

from sqlalchemy.orm import Session
from models.task import Task
from schemas.task import TaskCreate, TaskUpdate


# ---------------------------------------------------------
# 一覧取得
# ---------------------------------------------------------
def get_tasks(db: Session):
    return db.query(Task).all()


# ---------------------------------------------------------
# 1件取得
# ---------------------------------------------------------
def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


# ---------------------------------------------------------
# 新規作成
# ---------------------------------------------------------
def create_task(db: Session, task: TaskCreate):
    db_task = Task(
        title=task.title,
        start=task.start,
        end=task.end,
        importance=task.importance,
        memo=task.memo,
        type=task.type,
        done=task.done,
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


# ---------------------------------------------------------
# 更新
# ---------------------------------------------------------
def update_task(db: Session, task_id: int, task: TaskUpdate):
    db_task = get_task(db, task_id)
    if db_task is None:
        return None

    db_task.title = task.title
    db_task.start = task.start
    db_task.end = task.end
    db_task.importance = task.importance
    db_task.memo = task.memo
    db_task.type = task.type
    db_task.done = task.done

    db.commit()
    db.refresh(db_task)

    return db_task


# ---------------------------------------------------------
# 削除
# ---------------------------------------------------------
def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task is None:
        return None

    db.delete(db_task)
    db.commit()

    return True
