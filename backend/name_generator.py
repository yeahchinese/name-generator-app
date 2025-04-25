from pinyin_engine import english_to_pinyin
import random
import json

with open("poem_db.json", "r", encoding="utf-8") as f:
    poems = json.load(f)

def generate_chinese_name(first_name, last_name, birthdate, nationality):
    full_name = f"{first_name} {last_name}"
    pinyin_list = english_to_pinyin(full_name)
    chinese_name = ''.join(random.choice(p) for p in pinyin_list if isinstance(p, list))
    poem_entry = random.choice(poems)
    return {
        "name": chinese_name,
        "poem": poem_entry["line"],
        "source": poem_entry["source"],
        "meaning": poem_entry["meaning"]
    }