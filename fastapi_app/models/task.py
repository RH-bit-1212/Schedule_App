# fastapi-app/models/task.py

from db import Base
from sqlalchemy import Column, Integer, String, Boolean

class Task(Base):
    __tablename__ = "tasks"  # tasks テーブル定義

    id = Column(Integer, primary_key=True, index=True)   # タスクID（主キー）
    title = Column(String, nullable=False)               # タスク名
    start = Column(String, nullable=False)               # 開始時刻（例: "07:00"）
    end = Column(String, nullable=False)                 # 終了時刻（例: "07:30")
    importance = Column(Integer, nullable=False)         # 重要度（数値）
    memo = Column(String, nullable=True)                 # メモ（任意）
    type = Column(String, nullable=False)                # 種別（"スケジュール" / "習慣"）
    done = Column(Boolean, default=False)                # 完了フラグ
