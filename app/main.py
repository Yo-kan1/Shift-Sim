from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel

# 先ほど作ったファイルを読み込む
from .database import engine
from . import models 

# アプリ起動時にデータベースのテーブルを作成する設定
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

# FastAPIのアプリ本体を作成 (lifespanを登録)
app = FastAPI(title="Shift-Sim API", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Shift-Sim API is running with Database!"}