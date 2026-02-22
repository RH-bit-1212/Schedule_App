# fastapi_app/schemas/task.py

from pydantic import BaseModel
from typing import Optional


# -------------------------------------------------
#  共通のフィールド
# -------------------------------------------------
class TaskBase(BaseModel):
    title: str
    start: str        # "07:00"
    end: str          # "07:30"
    importance: int   # 1〜3
    memo: Optional[str] = None    # メモ（任意）
    type: str         # "スケジュール" or "習慣"
    done: bool = False    # 完了フラグ


# -------------------------------------------------
#  新規登録（クライアント→サーバ）
# -------------------------------------------------
class TaskCreate(TaskBase):
    """POST /tasks 用（id は不要）"""
    pass


# -------------------------------------------------
#  更新（クライアント→サーバ）
# -------------------------------------------------
class TaskUpdate(TaskBase):
    """PUT /tasks/{id} 用（id は不要）"""
    pass


# -------------------------------------------------
#  レスポンス（サーバ→クライアント）
# -------------------------------------------------
class TaskRead(TaskBase):
    id: int   # DB から返すので必須

    class Config:
        orm_mode = True  # ← SQLAlchemy と連携するため必須
