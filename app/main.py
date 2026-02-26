from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session, select

# 🌟 models.py から Shift も読み込むように変更
from .database import engine, get_session
from .models import Workplace, Shift 

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Shift-Sim API", lifespan=lifespan)

# ① バイト先を登録するAPI (POST)
@app.post("/workplaces/", response_model=Workplace)
def create_workplace(workplace: Workplace, session: Session = Depends(get_session)):
    session.add(workplace)
    session.commit()
    session.refresh(workplace)
    return workplace

# ② 登録されているバイト先の一覧を取得するAPI (GET)
@app.get("/workplaces/", response_model=list[Workplace])
def read_workplaces(session: Session = Depends(get_session)):
    workplaces = session.exec(select(Workplace)).all()
    return workplaces

# --- 🌟ここから下を追加 ---

# ③ シフトを登録するAPI (POST)
@app.post("/shifts/", response_model=Shift)
def create_shift(shift: Shift, session: Session = Depends(get_session)):
    session.add(shift)
    session.commit()
    session.refresh(shift)
    return shift

# ④ 登録されているシフトの一覧を取得するAPI (GET)
@app.get("/shifts/", response_model=list[Shift])
def read_shifts(session: Session = Depends(get_session)):
    shifts = session.exec(select(Shift)).all()
    return shifts