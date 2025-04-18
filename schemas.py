# schemas.py
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

# 请求体模型：用于 POST /shorten
class URLCreate(BaseModel):
    long_url: HttpUrl # Pydantic 自带的 HttpUrl 类型可以做 URL 校验

# 基础响应模型 (用于读取)
class URLMapBase(BaseModel):
    short_code: str
    long_url: HttpUrl

# 完整的响应模型 (可能包含数据库生成的字段)
class URLMap(URLMapBase):
    id: int
    created_at: datetime
    updated_at: datetime

    # 这个配置让 Pydantic 模型可以从 ORM 对象 (数据库记录) 创建
    class Config:
        from_attributes = True
        # 在 Pydantic V2 中，是 from_attributes = True
        # from pydantic_settings import BaseSettings
        # model_config = SettingsConfigDict(from_attributes=True)