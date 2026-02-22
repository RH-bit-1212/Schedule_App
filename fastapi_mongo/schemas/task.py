# fastapi_app/schemas/task.py
# -------------------------------------------------
# MongoDB 用 Task スキーマ定義
# -------------------------------------------------

from pydantic import BaseModel, Field
from typing import Optional


# -------------------------------------------------
# 共通フィールド
# -------------------------------------------------
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1)   # タスク名
    start: str                              # 開始時刻（例: "07:00"）
    end: str                                # 終了時刻（例: "07:30"）
    importance: int                         # 重要度
    memo: Optional[str] = None              # メモ（任意）
    type: str                               # "スケジュール" / "習慣"
    done: bool = False                      # 完了フラグ


# -------------------------------------------------
# 新規作成（POST /tasks）
# -------------------------------------------------
class TaskCreate(TaskBase):
    """
    MongoDB 登録用
    ・id / _id は含めない
    """
    pass


# -------------------------------------------------
# 更新（PUT /tasks/{id}）
# -------------------------------------------------
class TaskUpdate(TaskBase):
    """
    MongoDB 更新用
    ・id は URL パラメータで受け取る
    """
    pass


# -------------------------------------------------
# レスポンス（GET 系）
# -------------------------------------------------
class TaskRead(TaskBase):
    """
    MongoDB の _id を文字列として返す
    """
    id: str
