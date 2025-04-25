# backend/name_generator.py
import os
import json
import random
from datetime import datetime
from pypinyin import lazy_pinyin, Style
from lunar_converter import LunarDate

class NameGenerator:
    def __init__(self):
        # 加载诗词数据库
        self.poetry_db = self._load_poetry_data()
        self.surname_map = self._load_surname_mapping()
        self.common_surnames = self._load_common_surnames()
        
        # 音译配置
        self.surname_weights = {
            'sound': 0.6,
            'meaning': 0.4
        }

    def _load_poetry_data(self):
        """加载开源诗词数据库"""
        poetry_data = []
        data_dir = os.path.join(os.path.dirname(__file__), 'data/poetry')
        
        for filename in os.listdir(data_dir):
            if filename.endswith('.json'):
                with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as f:
                    poetry_data.extend(json.load(f))
        return poetry_data

    def _load_surname_mapping(self):
        """加载姓氏音译映射表"""
        with open('data/surnames/surname_mapping.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_common_surnames(self):
        """加载现代常见姓氏"""
        with open('data/surnames/common_surnames.txt', 'r', encoding='utf-8') as f:
            return [line.strip() for line in f]

    def _translate_surname(self, last_name: str) -> str:
        """
        智能姓氏音译
        算法步骤：
        1. 优先匹配已知映射
        2. 音译+常见姓氏筛选
        3. 语义优先回退
        """
        # 精确匹配
        if last_name.lower() in self.surname_map:
            return self.surname_map[last_name.lower()]
        
        # 音译候选
        pinyin = ''.join(lazy_pinyin(last_name, style=Style.NORMAL))
        candidates = [
            (surname, self._similarity_score(pinyin, surname))
            for surname in self.common_surnames
        ]
        
        # 加权排序
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0]

    def _similarity_score(self, source: str, target: str) -> float:
        """音形相似度评分"""
        # 声母匹配
        initial_score = 1.0 if lazy_pinyin(target, style=Style.INITIALS)[0][0] == source[0] else 0.0
        
        # 长度匹配
        length_score = 1 - abs(len(source) - len(target)) * 0.1
        
        return self.surname_weights['sound'] * (initial_score + length_score) + \
               self.surname_weights['meaning'] * self._semantic_score(target)

    def _semantic_score(self, surname: str) -> float:
        """姓氏语义评分"""
        # 从Unihan数据库获取语义评分（示例）
        semantic_db = {
            '李': 0.9, '王': 0.9, '张': 0.85,
            '布': 0.6, '戴': 0.7, '安': 0.8
        }
        return semantic_db.get(surname, 0.5)

    def _match_poetry(self, pinyin: str, birthdate: datetime) -> dict:
        """
        根据音韵和生日匹配诗词
        算法策略：
        - 押韵匹配（尾字韵母）
        - 季节关联（生日所在季节）
        - 高频美字优先
        """
        lunar_date = LunarDate.from_datetime(birthdate)
        
        # 生成候选特征
        features = {
            'rhyme': lazy_pinyin(pinyin[-1], style=Style.FINALS_TONE3),
            'season': self._get_season(lunar_date.month),
            'zodiac': lunar_date.zodiac
        }
        
        # 筛选并排序
        candidates = []
        for poem in self.poetry_db:
            score = 0
            if poem.get('rhyme') == features['rhyme']:
                score += 3
            if poem.get('season') == features['season']:
                score += 2
            if poem.get('zodiac'):
                score += 1
            candidates.append((poem, score))
        
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0] if candidates else None

    def _get_season(self, month: int) -> str:
        """农历月份转季节"""
        if month in [1, 2, 3]:
            return '春'
        elif month in [4, 5, 6]:
            return '夏'
        elif month in [7, 8, 9]:
            return '秋'
        else:
            return '冬'

    def generate_chinese_name(self, first_name: str, last_name: str, 
                             birthdate: str, nationality: str) -> dict:
        # 参数处理
        birth_date = datetime.strptime(birthdate, "%Y-%m-%d")
        
        # 姓氏音译
        chinese_surname = self._translate_surname(last_name)
        
        # 生成候选名
        base_pinyin = ''.join(lazy_pinyin(first_name))
        matched_poem = self._match_poetry(base_pinyin, birth_date)
        
        # 构建结果
        return {
            "chinese_name": chinese_surname + matched_poem['name'],
            "meaning": matched_poem['meaning'],
            "poem": matched_poem['content'],
            "pinyin": ' '.join(lazy_pinyin(chinese_surname + matched_poem['name'])),
            "lunar_date": str(LunarDate.from_datetime(birth_date)),
            "cultural_origin": "诗词典籍" if matched_poem else "创意组合"
        }

# 数据目录结构
"""
backend/
├── data/
│   ├── poetry/
│   │   ├── tang_poetry.json
│   │   ├── song_poetry.json
│   │   └── ...
│   ├── surnames/
│   │   ├── surname_mapping.json
│   │   └── common_surnames.txt
"""

# 诗词JSON格式示例
"""
{
  "title": "静夜思",
  "author": "李白",
  "content": "床前明月光，疑是地上霜。",
  "rhyme": "uang",
  "season": ["秋"],
  "zodiac": ["兔", "龙"],
  "name_candidates": ["明光", "月霜"]
}
"""

# 使用示例
if __name__ == "__main__":
    generator = NameGenerator()
    print(generator.generate_chinese_name(
        first_name="Michael",
        last_name="Johnson",
        birthdate="1990-05-15",
        nationality="US"
    ))
