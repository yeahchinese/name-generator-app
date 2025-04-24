# name_generator.py

from pinyin_engine import simple_pinyin_translator
import random

# 示例诗词数据库（可接入真实 DB 或 JSON 文件）
POEM_DATABASE = [
    {
        "name": "可可",
        "meaning": "温润如玉，甜美可亲",
        "poem": "桃之夭夭，灼灼其华"
    },
    {
        "name": "若琳",
        "meaning": "如兰之气，清新雅致",
        "poem": "采兰赠芍，言念君子"
    },
    {
        "name": "语嫣",
        "meaning": "言辞动人，如花似玉",
        "poem": "嫣然一笑，倾国倾城"
    },
    {
        "name": "天一",
        "meaning": "天之骄子，独一无二",
        "poem": "天行健，君子以自强不息"
    }
]

def generate_chinese_name(first_name: str, last_name: str, birthdate: str, nationality: str) -> dict:
    """
    根据用户输入生成中文名字及其解释
    """
    base_pinyin = simple_pinyin_translator(first_name)
    
    # 从诗词数据库中随机选取一个名字
    selected = random.choice(POEM_DATABASE)

    # 示例姓氏映射（可扩展支持英文姓氏音译）
    surname_mapping = {
        'Smith': '史',
        'Johnson': '江',
        'Brown': '布',
        'Lee': '李',
        'Taylor': '陶',
        'Miller': '米',
        'Davis': '戴',
        'Wilson': '魏',
        'Anderson': '安',
        'Thomas': '唐'
    }
    
    chinese_surname = surname_mapping.get(last_name, '叶')

    full_name = chinese_surname + selected['name']
    
    return {
        "chinese_name": full_name,
        "meaning": selected["meaning"],
        "poem": selected["poem"],
        "lunar_date": fake_lunar_date(birthdate)  # 模拟农历日期
    }

def fake_lunar_date(gregorian: str) -> str:
    # 示例转换（应替换为真实农历 API 调用）
    return "农历乙巳年七月初七"
