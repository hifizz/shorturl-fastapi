from sqlalchemy.orm import Session
import models
import random
import string

def generate_short_code(length: int = 6) -> str:
  characters = string.ascii_letters + string.digits
  return ''.join(random.choice(characters) for _ in range(length))

# 根据短码获取 URL 映射记录
def get_url_map_by_short_code(db: Session, short_code: str):
    # db.query(models.URLMap) 开始一个查询
    # .filter(models.URLMap.short_code == short_code) 添加过滤条件
    # .first() 返回第一个匹配的记录，如果没有则返回 None
    return db.query(models.URLMap).filter(models.URLMap.short_code == short_code).first()

# 根据长 URL 获取 URL 映射记录 (防止重复创建)
def get_url_map_by_long_url(db: Session, long_url: str):
    return db.query(models.URLMap).filter(models.URLMap.long_url == long_url).first()

# 创建新的 URL 映射记录
def create_url_map(db: Session, long_url: str):
    # TODO： 待优化
    # 循环生成短码，直到找到一个数据库里不存在的
    while True:
        short_code = generate_short_code()
        db_url_map = get_url_map_by_short_code(db, short_code)
        if not db_url_map:
            break # 找到未使用的短码

    # 创建模型实例
    db_url_map = models.URLMap(short_code=short_code, long_url=long_url)
    # 添加到会话
    db.add(db_url_map)
    # 提交事务到数据库
    db.commit()
    # 刷新实例，获取数据库生成的值 (比如 id, created_at)
    db.refresh(db_url_map)
    return db_url_map


def get_all_url_maps(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.URLMap).offset(skip).limit(limit).all()
