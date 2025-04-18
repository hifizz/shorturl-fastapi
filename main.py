# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, HTMLResponse # 导入 HTMLResponse
from fastapi.staticfiles import StaticFiles # 导入 StaticFiles
from sqlalchemy.orm import Session
import models, schemas, crud # 导入相关模块
from database import engine, SessionLocal, get_db # 导入 get_db

# 在应用启动时创建数据库表
# 注意：这里需要确保 models.py 中的 Base 被正确关联
# 更稳妥的方式是在 database.py 中导入并绑定 models.Base
# 或者直接在这里调用 models.Base.metadata.create_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 挂载静态文件目录
# "/static" 是 URL 路径, directory="static" 是本地目录名
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.post("/shorten")
def create_short_url(url_in: schemas.URLCreate, db: Session = Depends(get_db)):
  db_url= crud.get_url_map_by_long_url(db, str(url_in.long_url))
  if db_url:
    return db_url

  new_url_map = crud.create_url_map(db, long_url=str(url_in.long_url));
  return new_url_map;

@app.get("/{short_code}")
def redirect_to_long_url(short_code: str, db: Session = Depends(get_db)):
  db_url = crud.get_url_map_by_short_code(db, short_code)
  if db_url is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")

  return RedirectResponse(url=str(db_url.long_url), status_code=status.HTTP_301_MOVED_PERMANENTLY)

if __name__ == "__main__":
  print("要运行 FastAPI 应用, 请使用 uvicorn 命令:")
  print("uvicorn main:app --reload")
