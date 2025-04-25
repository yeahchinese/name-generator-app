import json
import random

with open('sound_map.json', 'r', encoding='utf-8') as f:
    sound_map = json.load(f)

def generate_name(gender="unisex", length=2):
    # 过滤符合性别的音节
    candidates = [
        entry for entry in sound_map.values()
        if entry["gender"] == gender or entry["gender"] == "unisex"
    ]
    if not candidates:
        return "无可用名字"

    weights = [entry["weight"] for entry in candidates]
    selected = random.choices(candidates, weights=weights, k=length)
    return ''.join([s["char"] for s in selected])

# 示例调用
if __name__ == "__main__":
    print(generate_name(gender="female"))
