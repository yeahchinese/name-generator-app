# lunar/lunar_converter.py
from lunardate import LunarDate
from datetime import datetime

def convert_to_lunar(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    lunar = LunarDate.fromSolarDate(date.year, date.month, date.day)
    return {
        "year": lunar.year,
        "month": lunar.month,
        "day": lunar.day,
        "is_leap": lunar.isleap()
    }
