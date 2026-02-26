from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException # HTTPExceptionを追加
from sqlmodel import SQLModel, Session, select
from .database import engine, get_session
from .models import Workplace, Shift
from . import services # 🌟 先ほど作った計算ファイルを読み込む
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

# ⑤ 特定のシフトの給与を計算するAPI (GET)
@app.get("/shifts/{shift_id}/calculate")
def calculate_salary(shift_id: int, session: Session = Depends(get_session)):
    # 1. DBからシフト情報を探す
    shift = session.get(Shift, shift_id)
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
        
    # 2. DBから紐づくバイト先情報を探す
    workplace = session.get(Workplace, shift.workplace_id)
    if not workplace:
        raise HTTPException(status_code=404, detail="Workplace not found")
        
    # 3. 給与計算ロジックを実行！
    result = services.calculate_shift_salary(shift, workplace)
    return result