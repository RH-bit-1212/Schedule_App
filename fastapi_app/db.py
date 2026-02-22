# fastapi_app/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -----------------------------------
# DB 接続 URL（SQLite を使用）
# -----------------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

# -----------------------------------
# エンジン作成（SQLite 用の設定）
# -----------------------------------
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite のおまじない
)

# -----------------------------------
# SessionLocal（DB セッション）
# -----------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -----------------------------------
# ORM モデルの基底クラス
# -----------------------------------
Base = declarative_base()

# -----------------------------------
# FastAPI に inject する DB セッション依存関係
# -----------------------------------
def get_db():
    """FastAPI の Depends が使用する DB セッション生成"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
