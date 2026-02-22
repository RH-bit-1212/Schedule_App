# fastapi-mongo/main.py
# -------------------------------------------------
# MongoDB 版 FastAPI（/tasks API に統一）
# -------------------------------------------------

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId

from schemas.task import TaskCreate, TaskRead, TaskUpdate


app = FastAPI()

# ---------------------------------------
# CORS 設定（Vue 8080 を許可）
# ---------------------------------------
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------
# MongoDB 接続
# ---------------------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["syspro10"]     # DB 名
col = db["tasks"]          # コレクション名


# ---------------------------------------
# Mongo → JSON 変換
# ---------------------------------------
def serialize(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "title": doc.get("title"),
        "start": doc.get("start"),
        "end": doc.get("end"),
        "importance": doc.get("importance"),
        "memo": doc.get("memo"),
        "type": doc.get("type"),
        "done": doc.get("done", False),
    }


# ---------------------------------------
# READ 全件（GET /tasks）
# ---------------------------------------
@app.get("/tasks", response_model=list[TaskRead])
def read_tasks():
    docs = col.find().sort("_id", -1)
    return [serialize(d) for d in docs]


# ---------------------------------------
# READ 1件（GET /tasks/{id}）
# ---------------------------------------
@app.get("/tasks/{task_id}", response_model=TaskRead)
def read_task(task_id: str):
    doc = col.find_one({"_id": ObjectId(task_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Task not found")
    return serialize(doc)


# ---------------------------------------
# CREATE（POST /tasks）
# ---------------------------------------
@app.post("/tasks", response_model=TaskRead)
def create_task(task: TaskCreate):
    doc = task.model_dump()
    result = col.insert_one(doc)
    new_doc = col.find_one({"_id": result.inserted_id})
    return serialize(new_doc)


# ---------------------------------------
# UPDATE（PUT /tasks/{id}）
# ---------------------------------------
@app.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: str, task: TaskUpdate):
    result = col.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": task.model_dump()}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    updated = col.find_one({"_id": ObjectId(task_id)})
    return serialize(updated)


# ---------------------------------------
# DELETE（DELETE /tasks/{id}）
# ---------------------------------------
@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    result = col.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"result": "ok"}
