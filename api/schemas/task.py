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
