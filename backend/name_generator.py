# backend/name_generator.py
from poetry_db import get_poem_by_tone
from pinyin_engine import approximate_pinyin

def generate_chinese_name(first, last, dob, nationality):
    pinyin_syllables = approximate_pinyin(first + ' ' + last)
    poem = get_poem_by_tone(pinyin_syllables[-1])  # 假设取最后音节押韵的诗句
    name = pinyin_syllables[0] + pinyin_syllables[1]  # 简化音译
    return {
        "name": name,
        "meaning": "名字意为温润如玉，寓意才情横溢",
        "poem": poem
    }
