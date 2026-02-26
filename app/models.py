from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class Workplace(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    
    # 基本情報
    base_rate: int
    transportation_fee: int = Field(default=0)
    daily_allowance: int = Field(default=0) # 日当（新規追加）
    
    # --- 時間帯割増情報（timeRate） ---
    # 例: start="22:00", end="06:00", rate=1637
    time_rate_start: Optional[str] = Field(default=None)
    time_rate_end: Optional[str] = Field(default=None)
    time_rate_rate: Optional[int] = Field(default=None)

    # --- 休日設定（holidayRate） ---
    holiday_rate: Optional[int] = Field(default=None)
    holiday_time_rate_start: Optional[str] = Field(default=None)
    holiday_time_rate_end: Optional[str] = Field(default=None)
    holiday_time_rate_rate: Optional[int] = Field(default=None)


class Shift(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    workplace_id: int = Field(foreign_key="workplace.id")
    start_datetime: datetime
    end_datetime: datetime
    is_actual: bool = Field(default=False)