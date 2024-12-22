# FastAPIの基本的な使い方

# 参考資料

- [FastAPI入門](https://zenn.dev/sh0nk/books/537bb028709ab9)
  - 直接の参考元
- [FastAPI](https://fastapi.tiangolo.com)
  - ドキュメント

# 環境構築

## 導入方法

```powershell
pip install "fastapi[standard]"
```

## 起動方法

```powershell
fastapi dev main.py
```

## URLについて

- http://127.0.0.1:8000/
  - 基本的なURL
- http://127.0.0.1:8000/docs
  - openAPIドキュメント

# 型アノテーション

## 簡易説明

```python
# 型アノテーション
num:int=1
num="string" # 実行はできるがエラーを出せる
```

# 基本記法

## 最小起動

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello") # /helloのエンドポイントで動作
async def hello():
    return {"message": "hello world!"}
```

## ファイル分割後

### ディレクトリ

```
📦api
 ┣ 📂routers
 ┃ ┣ 📜done.py
 ┃ ┗ 📜task.py
 ┗ 📜main.py
```

### main.py

```python
from fastapi import FastAPI
from api.routers import task, done

app = FastAPI()

@app.get("/hello")
async def hello():
    return {"message": "hello world!"}

app.include_router(task.router)
app.include_router(done.router)
```

### routers/done.py

```python
from fastapi import APIRouter

router = APIRouter()

@router.put("/tasks/{task_id}/done")
async def mark_task_as_done():
    pass

@router.delete("/tasks/{task_id}/done")
async def unmark_task_as_done():
    pass
```

### routers/task.py

```python
from fastapi import APIRouter
from typing import List
import api.schemas.task as task_schema

router = APIRouter()

@router.get("/tasks")
async def list_tasks():
    pass

@router.post("/tasks")
async def create_task():
    pass

@router.put("/tasks/{task_id}")
async def update_task():
    pass

@router.delete("/tasks/{task_id}")
async def delete_task():
    pass

```

# 型アノテーションを使ったAPIの型定義

## ディレクトリ

```
📦api
 ┣ 📂routers
 ┃ ┣ 📜done.py
 ┃ ┗ 📜task.py
 ┣ 📂schemas
 ┃ ┗ 📜task.py
 ┗ 📜main.py
```

## schemas/task.py

```python
from typing import Optional
from pydantic import BaseModel, Field

class TaskBase(BaseModel):
    title: Optional[str] = Field(
        default=None,
        json_schema_extra={"example": "クリーニングを取りに行く"} # JSON Schema の拡張情報。Swagger UI に表示される
    )

class Task(TaskBase): # クラスの継承
    id: int # 必須の整数型のフィールド
    done: bool = Field( # 必須の真偽値型のフィールド
        default=False, # デフォルト値
        description="完了フラグ" # ドキュメントの説明。Swagger UI に表示される
    )

    class Config: # DBとの接続に使用する設定
        from_attributes = True

class TaskCreate(TaskBase): # クラスの継承
    pass

class TaskCreateResponse(TaskCreate):
    id: int

    class Config:
        from_attributes = True
```

## routers/tasks.py

```python
from fastapi import APIRouter
from typing import List
import api.schemas.task as task_schema

router = APIRouter()

@router.get("/tasks", response_model=List[task_schema.Task])
async def list_tasks():
    return [task_schema.Task(id=1, title="1つ目のTODOタスク")]

@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(task_body: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=1, **task_body.model_dump()) # task_bodyにidを追加して返す

@router.put("/tasks/{task_id}")
async def update_task(task_id: int, task_body: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=task_id, **task_body.model_dump())

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    return

```

## routers/done.py

```python
from fastapi import APIRouter

router = APIRouter()

@router.put("/tasks/{task_id}/done", response_model=None)
async def mark_task_as_done(task_id: int):
    return

@router.delete("/tasks/{task_id}/done", response_model=None)
async def unmark_task_as_done(task_id: int):
    return
```

