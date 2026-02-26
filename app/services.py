from datetime import datetime
from .models import Workplace, Shift

def calculate_shift_salary(shift: Shift, workplace: Workplace) -> dict:
    """
    シフトとバイト先の情報から、予想給与を計算する関数
    """
    # 1. 勤務時間（時間）の算出
    duration = shift.end_datetime - shift.start_datetime
    total_hours = duration.total_seconds() / 3600.0  # 秒を時間に変換

    # 2. 基本給の計算（※一旦、休日設定は除外して基本時給で計算）
    base_salary = int(workplace.base_rate * total_hours)

    # 3. 交通費と日当の加算
    total_salary = base_salary + workplace.transportation_fee + workplace.daily_allowance

    # --- 今後ここに「深夜割増（22:00〜06:00）」の計算を追加します ---

    return {
        "workplace_name": workplace.name,
        "total_hours": round(total_hours, 2),
        "base_salary": base_salary,
        "transportation_fee": workplace.transportation_fee,
        "daily_allowance": workplace.daily_allowance,
        "total_salary": total_salary
    }