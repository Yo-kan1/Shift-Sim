from typing import Optional
from sqlmodel import Field, SQLModel

# table=True とすることで、このクラスがデータベースのテーブルになります
class Workplace(SQLModel, table=True):
    # id は自動で割り当てられる主キー（Primary Key）
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # バイト先名（例：びっくりドンキー）
    name: str = Field(index=True)
    
    # 基本時給
    base_rate: int
    
    # 交通費（初期値は0円）
    transportation_fee: int = Field(default=0)