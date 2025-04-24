import os
import json
import re
from itertools import product
import epitran
import pypinyin

class PhoneticEngine:
    def __init__(self):
        self.resources_path = os.path.join(os.path.dirname(__file__), 'resources')
        self.epi = epitran.Epitran('eng-Latn')
        
        # 初始化资源
        self.sound_map = self._load_json_resource('sound_map.json')
        self.negative_lexicon = self._load_text_resource('negative_words.txt')
        self.poetic_terms = self._load_json_resource('poetic_terms.json')
        self.poetry_db = self._load_json_resource('poetry_db.json')
        
        # 声调偏好配置
        self.tone_rules = {
            'preferred_patterns': {
                ('2', '3'): 8,  # 阳平+上声
                ('1', '4'): 7,  # 阴平+去声
                ('2', '1', '4'): 9  # 三字名优选
            },
            'forbidden_combos': ['444', '111']  # 避免三连仄/平
        }

    def _load_json_resource(self, filename):
        """加载JSON格式资源文件"""
        path = os.path.join(self.resources_path, filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"无法加载资源文件 {filename}: {str(e)}")

    def _load_text_resource(self, filename):
        """加载文本格式资源文件""" 
        path = os.path.join(self.resources_path, filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return set(line.strip() for line in f if line.strip())
        except FileNotFoundError as e:
            raise RuntimeError(f"无法加载资源文件 {filename}: {str(e)}")

    # 保留之前的核心方法，更新资源引用路径...
    # [保留之前实现的 split_english_name, generate_candidate_chars 等方法]
    
    def _get_poetry_reference(self, name):
        """从诗词数据库获取引用"""
        references = []
        for char in name:
            if char in self.poetry_db:
                references.extend(self.poetry_db[char][:2])  # 取前两个引用
        return references[:3]  # 最多返回三个

    def generate_chinese_name(self, first_name, last_name, gender=None):
        """完整生成流程"""
        syllables = self.split_english_name(first_name)
        candidates = self.generate_candidate_chars(syllables)
        scored_names = self.combine_and_score_names(last_name, candidates)
        
        # 添加诗词引用
        final_names = []
        for name, score in scored_names:
            poetry_refs = self._get_poetry_reference(name)
            final_names.append({
                'name': name,
                'score': score,
                'poetry': poetry_refs,
                'gender_suit': self._check_gender_suit(name, gender)
            })
            
        return sorted(final_names, key=lambda x: x['score'], reverse=True)[:3]

# 保留其他辅助方法...

if __name__ == "__main__":
    # 测试用例
    engine = PhoneticEngine()
    
    test_cases = [
        ("Michael", "Li"),
        ("Sophia", "Wang"),
        ("James", "Zhang")
    ]
    
    for first, last in test_cases:
        print(f"\n生成 {first} {last} 的中文名:")
        results = engine.generate_chinese_name(first, last)
        for res in results:
            print(f"{res['name']} | 评分: {res['score']}")
            print("诗词引用: " + " | ".join(res['poetry'][:2]))
