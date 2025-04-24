# pinyin_engine.py

import re

def simple_pinyin_translator(name: str) -> str:
    """
    将英文名简化音译为近似拼音
    注意：此为简化版，仅用于演示。
    """
    name = name.lower().strip()
    mapping = {
        'a': '阿', 'b': '贝', 'c': '西', 'd': '迪', 'e': '伊',
        'f': '艾夫', 'g': '吉', 'h': '艾尺', 'i': '艾', 'j': '杰',
        'k': '凯', 'l': '艾勒', 'm': '艾姆', 'n': '恩', 'o': '欧',
        'p': '皮', 'q': '丘', 'r': '艾儿', 's': '艾丝', 't': '提',
        'u': '优', 'v': '维', 'w': '达布流', 'x': '艾克斯', 'y': '吾艾', 'z': '贼德'
    }
    pinyin = ''.join([mapping.get(ch, '') for ch in name if ch in mapping])
    return pinyin
