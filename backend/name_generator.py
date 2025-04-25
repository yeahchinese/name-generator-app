# backend/name_generator.py
import json
import re
from difflib import SequenceMatcher
from pypinyin import lazy_pinyin, Style
from typing import List, Tuple

class SurnameTranslator:
    """智能姓氏音译系统"""
    
    def __init__(self):
        # 加载多层级姓氏数据库
        self.exact_mapping = self._load_exact_mapping()
        self.common_surnames = self._load_common_surnames()
        self.semantic_db = self._load_semantic_db()
        
        # 权重配置（可动态调整）
        self.weights = {
            'initial': 0.4,    # 声母匹配
            'final': 0.3,      # 韵母匹配
            'length': 0.1,     # 长度相似度
            'semantic': 0.2    # 语义评分
        }

    def _load_exact_mapping(self) -> dict:
        """加载精确映射表（支持多语言）"""
        with open('resources/surnames/exact_mappings.json') as f:
            data = json.load(f)
            return {k.lower(): v for lang in data.values() for k, v in lang.items()}

    def _load_common_surnames(self) -> List[str]:
        """加载现代常见中文姓氏"""
        with open('resources/surnames/common_surnames.txt', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]

    def _load_semantic_db(self) -> dict:
        """加载姓氏语义数据库"""
        with open('resources/surnames/semantic_scores.json') as f:
            return json.load(f)

    def translate(self, surname: str, lang_hint: str = 'en') -> str:
        """
        智能姓氏翻译主逻辑
        :param surname: 原始姓氏
        :param lang_hint: 语言提示（en/jp/kr等）
        :return: 最佳匹配中文姓氏
        """
        # 清洗输入
        clean_surname = self._normalize_surname(surname, lang_hint)
        
        # 优先精确匹配
        if matched := self._exact_match(clean_surname):
            return matched
        
        # 生成候选列表
        candidates = self._generate_candidates(clean_surname)
        
        # 综合评分
        scored_candidates = [
            (surname, self._score_surname(clean_surname, surname))
            for surname in candidates
        ]
        
        # 返回最高分项
        return max(scored_candidates, key=lambda x: x[1])[0]

    def _normalize_surname(self, surname: str, lang_hint: str) -> str:
        """姓氏预处理"""
        # 统一转小写并移除特殊字符
        surname = re.sub(r'[^a-zA-Z\u4e00-\u9fff]', '', surname).lower()
        
        # 语言特定处理
        if lang_hint == 'jp':
            surname = surname.replace(' ', '')  # 处理日语空格
        elif lang_hint == 'kr':
            surname = surname[:3]  # 韩语姓氏通常较短
            
        return surname

    def _exact_match(self, surname: str) -> str:
        """精确匹配逻辑"""
        return self.exact_mapping.get(surname, None)

    def _generate_candidates(self, surname: str) -> List[str]:
        """生成音译候选"""
        # 第一步：首字母匹配
        initial_char = surname[0].upper()
        initial_matches = [s for s in self.common_surnames if s.startswith(initial_char)]
        
        # 第二步：发音近似匹配
        pinyin = self._get_pinyin_features(surname)
        sound_matches = [
            s for s in self.common_surnames
            if self._pinyin_similarity(pinyin, s) > 0.6
        ]
        
        return list(set(initial_matches + sound_matches))[:20]  # 限制候选数量

    def _get_pinyin_features(self, surname: str) -> dict:
        """获取拼音特征"""
        return {
            'initials': lazy_pinyin(surname, style=Style.INITIALS),
            'finals': lazy_pinyin(surname, style=Style.FINALS_TONE3),
            'normal': lazy_pinyin(surname, style=Style.NORMAL)
        }

    def _pinyin_similarity(self, source: dict, target: str) -> float:
        """拼音相似度计算"""
        target_pinyin = lazy_pinyin(target, style=Style.FINALS_TONE3)
        
        # 声母匹配
        initial_score = sum(
            1 for s, t in zip(source['initials'], target_pinyin)
            if s and t and s[0] == t[0]
        ) / len(source['initials'])
        
        # 韵母匹配
        final_score = SequenceMatcher(
            None, ''.join(source['finals']), ''.join(target_pinyin)
        ).ratio()
        
        return initial_score * 0.6 + final_score * 0.4

    def _score_surname(self, source: str, candidate: str) -> float:
        """综合评分模型"""
        # 长度相似度
        length_score = 1 - abs(len(source) - len(candidate)) * 0.1
        
        # 拼音特征
        pinyin_source = self._get_pinyin_features(source)
        pinyin_score = self._pinyin_similarity(pinyin_source, candidate)
        
        # 语义评分
        semantic_score = self.semantic_db.get(candidate, 0.5)
        
        # 综合计算
        return (
            self.weights['initial'] * pinyin_score +
            self.weights['final'] * length_score +
            self.weights['semantic'] * semantic_score
        )

class NameGenerator:
    """整合音译系统的改进版生成器"""
    
    def __init__(self):
        self.translator = SurnameTranslator()
        self.poetry_db = self._load_poetry_db()
        
    def generate_names(self, first_name: str, last_name: str, **kwargs) -> List[dict]:
        """主生成逻辑"""
        chinese_surname = self.translator.translate(
            last_name, 
            lang_hint=kwargs.get('nationality', 'en')
        )
        
        # 生成候选名逻辑（需根据实际需求扩展）
        # ...
        
        return [{
            "name": chinese_surname + "晓明",
            "pinyin": "Xiao Ming",
            "meaning": "破晓之光，明智聪慧",
            "poetry": ["《晨兴》'晓光初透玉窗纱，起理新妆对镜花'"]
        }]

# 关键数据文件结构
"""
resources/
  surnames/
    exact_mappings.json  # 多语言精确映射
    common_surnames.txt  # 常见中文姓氏
    semantic_scores.json # 姓氏语义评分
    /
      en.json  # 英语姓氏扩展映射
      jp.json  # 日语姓氏扩展映射
      kr.json  # 韩语姓氏扩展映射
"""

# exact_mappings.json 示例
{
  "en": {
    "smith": "史",
    "johnson": "江",
    "watanabe": "渡边"
  },
  "jp": {
    "satō": "佐藤",
    "suzuki": "铃木"
  },
  "kr": {
    "kim": "金", 
    "lee": "李"
  }
}
