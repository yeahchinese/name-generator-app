# backend/name_generator.py
from datetime import datetime
from pinyin_engine import PhoneticEngine
from poetry_db import PoetryDatabase
from lunar_converter import LunarCalendar
from cultural_filters import check_taboos

class NameGenerator:
    def __init__(self):
        # 初始化核心组件
        self.engine = PhoneticEngine()
        self.poetry_db = PoetryDatabase()
        self.lunar_conv = LunarCalendar()
        
        # 加载文化偏好配置
        self._load_cultural_preferences()
    
    def _load_cultural_preferences(self):
        """加载国家/地区文化偏好"""
        with open('resources/cultural_prefs.json') as f:
            self.cultural_prefs = json.load(f)
    
    def generate_names(self, first_name, last_name, birthdate, nationality, gender=None):
        """
        主生成逻辑
        :param first_name: 英文名
        :param last_name: 英文姓
        :param birthdate: 生日字符串 (YYYY-MM-DD)
        :param nationality: ISO国家代码
        :param gender: 可选性别参数
        :return: 排序后的候选名字列表
        """
        # 参数校验
        self._validate_input(first_name, last_name, birthdate)
        
        # 文化参数处理
        lunar_date = self.lunar_conv.convert(birthdate)
        country_prefs = self.cultural_prefs.get(nationality, {})
        
        # 音韵生成
        name_candidates = self._generate_candidates(
            first_name, last_name, 
            lunar_date=lunar_date,
            country_prefs=country_prefs
        )
        
        # 综合评分
        scored_names = self._score_names(
            name_candidates,
            lunar_date=lunar_date,
            gender=gender
        )
        
        return sorted(scored_names, key=lambda x: x['score'], reverse=True)[:3]

    def _validate_input(self, first, last, dob):
        """输入验证"""
        if len(first) < 2 or len(last) < 2:
            raise ValueError("姓名长度需大于2字符")
        try:
            datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            raise ValueError("生日格式错误，应为YYYY-MM-DD")

    def _generate_candidates(self, first, last, **context):
        """生成候选名字"""
        # 音译处理
        syllables = self.engine.split_english_name(first + ' ' + last)
        
        # 姓氏本地化
        localized_surname = self._localize_surname(
            last, 
            context['country_prefs']
        )
        
        # 候选组合
        base_names = self.engine.combine_syllables(
            localized_surname, 
            syllables,
            max_length=3  # 最多三字名
        )
        
        # 文化过滤
        return [name for name in base_names if not check_taboos(name)]

    def _localize_surname(self, surname, prefs):
        """本地化姓氏处理"""
        # 优先使用常见本地化姓氏
        if prefs.get('common_surnames'):
            return prefs['common_surnames'][0]
        
        # 音译回退方案
        return self.engine.transliterate(surname)[0]

    def _score_names(self, candidates, **context):
        """综合评分模型"""
        scored = []
        for name in candidates:
            # 基础评分
            score = self.engine.base_score(name)
            
            # 生肖加成
            score += self._zodiac_bonus(name, context['lunar_date'])
            
            # 性别适配
            if context.get('gender'):
                score *= self._gender_factor(name, context['gender'])
                
            # 诗词引用加成
            poetry_refs = self.poetry_db.match_poetry(name)
            score += len(poetry_refs) * 0.5
            
            scored.append({
                "name": name,
                "score": round(score, 1),
                "pinyin": self.engine.to_pinyin(name),
                "poetry": poetry_refs[:2],  # 取前两个引用
                "cultural_origin": self._detect_origin(name, poetry_refs)
            })
        return scored

    def _zodiac_bonus(self, name, lunar_date):
        """生肖匹配加成"""
        zodiac = lunar_date['zodiac']
        # 根据生肖字典检查宜用字
        return sum(1 for char in name if char in self.zodiac_words[zodiac]) * 0.3

    def _gender_factor(self, name, gender):
        """性别适配系数"""
        fem_words = self.cultural_prefs['gender']['female']
        masc_words = self.cultural_prefs['gender']['male']
        
        fem_score = sum(1 for char in name if char in fem_words)
        masc_score = sum(1 for char in name if char in masc_words)
        
        if gender == 'female':
            return 1 + fem_score * 0.1 - masc_score * 0.05
        elif gender == 'male':
            return 1 + masc_score * 0.1 - fem_score * 0.05
        return 1  # 中性情况

    def _detect_origin(self, name, poetry_refs):
        """判断名字文化来源"""
        if poetry_refs:
            return 'classic_poetry'
        if any(char in self.cultural_prefs['common_words'] for char in name):
            return 'modern_trend'
        return 'phonetic_creative'
