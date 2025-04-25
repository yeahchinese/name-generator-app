import random
import json
from pinyin_engine import get_initial_letter

with open("backend/sound_map.json", encoding="utf-8") as f:
    sound_map = json.load(f)

def generate_name(first_name, last_name, gender="unisex"):
    initial = get_initial_letter(first_name)
    candidates = sound_map.get(initial.upper(), [])
    filtered = [c for c in candidates if c["gender"] in [gender, "unisex"]]
    if not filtered:
        return {"name": "未知", "meaning": "暂无匹配"}
    selected = random.choices(filtered, weights=[c["weight"] for c in filtered], k=1)[0]
    return {"name": selected["pinyin"], "meaning": selected["meaning"]}
