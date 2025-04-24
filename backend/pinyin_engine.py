import epitran
import pypinyin
from itertools import product
from collections import defaultdict
import re
import json

class PhoneticEngine:
    def __init__(self):
        # 加载资源
        self.epi = epitran.Epitran('eng-Latn')
        self.load_sound_map()
        self.load_negative_lexicon()
        self.load_poetic_terms()
        
    def load_sound_map(self):
        """加载音译映射库"""
        with open('sound_map.json', 'r', encoding='utf-8') as f:
            self.sound_map = json.load(f)
            
        # 声调组合偏好（示例）
        self.tone_preference = {
            ('2', '3'): 8,  # 阳平+上声
            ('1', '4'): 7,  # 阴平+去声
            ('2', '1', '4'): 9  # 三字名优选组合
        }
        
    def load_negative_lexicon(self):
        """加载不雅词汇库"""
        with open('negative_words.txt', 'r', encoding='utf-8') as f:
            self.negative_lexicon = set(line.strip() for line in f)
            
    def load_poetic_terms(self):
        """加载诗词高频词汇""" 
        with open('poetic_terms.json', 'r', encoding='utf-8') as f:
            self.poetic_terms = json.load(f)
    
    def split_english_name(self, name):
        """使用音标拆分英文名到音节"""
        ipa = self.epi.transliterate(name)
        syllables = self._ipa_to_syllables(ipa)
        return syllables
    
    def _ipa_to_syllables(self, ipa):
        """将国际音标分割为近似中文发音的音节（核心算法）"""
        # 实现音标到中文友好音节的转换规则
        vowels = ['a', 'e', 'i', 'o', 'u', 'ɑ', 'ɔ', 'ɛ', 'ɪ', 'ʊ', 'ʌ']
        consonants = ['p', 'b', 't', 'd', 'k', 'g', 'm', 'n', 'ŋ', 'f', 'v', 
                     's', 'z', 'ʃ', 'ʒ', 'h', 'l', 'r', 'j', 'w']
        
        # 音节分割逻辑（示例）
        syllables = []
        current = []
        for c in ipa:
            if c in vowels and len(current) > 0:
                syllables.append(''.join(current))
                current = [c]
            else:
                current.append(c)
        if current:
            syllables.append(''.join(current))
            
        # 音位调整规则（示例）
        adjusted = []
        for syl in syllables:
            syl = re.sub(r'tʃ', 'ch', syl)
            syl = re.sub(r'ʃ', 'sh', syl)
            syl = re.sub(r'ʒ', 'zh', syl)
            adjusted.append(syl)
            
        return adjusted[:3]  # 取前三个有效音节
    
    def generate_candidate_chars(self, syllables):
        """生成候选汉字列表"""
        candidates = []
        for syl in syllables:
            closest = self.find_closest_syllable(syl)
            if closest in self.sound_map:
                candidates.append(self.sound_map[closest])
        return candidates
    
    def find_closest_syllable(self, syllable):
        """寻找最接近的中文发音音节"""
        # 实现音节相似度匹配算法（此处简化）
        mapping = {
            'ka': 'ka', 'der': 'de', 'lex': 'lie'
        }
        return mapping.get(syllable[:2], syllable[:2])
    
    def combine_and_score_names(self, last_name, candidates):
        """生成并评分姓名组合"""
        # 生成所有可能组合
        all_combos = list(product(*candidates))
        scored_names = []
        
        for combo in all_combos:
            full_name = last_name + ''.join(combo)
            if self.is_valid_name(full_name):
                score = self.score_name(full_name)
                scored_names.append((full_name, score))
                
        # 按评分排序并去重
        scored_names.sort(key=lambda x: x[1], reverse=True)
        return scored_names[:10]
    
    def is_valid_name(self, name):
        """基础验证"""
        # 长度检查
        if len(name) < 2 or len(name) > 4:
            return False
        # 不雅词汇检查
        if any(word in name for word in self.negative_lexicon):
            return False
        return True
    
    def score_name(self, name):
        """综合评分模型"""
        score = 0
        
        # 声调分析
        tones = self.get_tones(name)
        score += self.tone_score(tones)
        
        # 韵律检查
        if self.has_rhyme_conflict(name):
            score -= 5
            
        # 诗意评分
        score += self.poetic_score(name)
        
        # 文化偏好
        if len(name) == 3:
            score += 2  # 偏好三字名
            
        return score
    
    def get_tones(self, name):
        """获取每个字的声调"""
        pinyin_list = pypinyin.lazy_pinyin(name, style=pypinyin.TONE3)
        return [p[-1] for p in pinyin_list if p]
    
    def tone_score(self, tones):
        """声调组合评分"""
        for pattern, value in self.tone_preference.items():
            if tuple(tones) == pattern:
                return value
        return 0
    
    def poetic_score(self, name):
        """诗意程度评分"""
        score = 0
        for term in self.poetic_terms:
            if term in name:
                score += self.poetic_terms[term]
        return min(score, 5)
    
    def has_rhyme_conflict(self, name):
        """检查韵母冲突"""
        finals = [pypinyin.lazy_pinyin(c)[0][1:] for c in name]
        return len(set(finals)) < len(finals)//2

# 示例用法
if __name__ == "__main__":
    engine = PhoneticEngine()
    
    # 测试用例
    first_name = "Michael"
    last_name = "Li"
    
    syllables = engine.split_english_name(first_name)
    print(f"音节拆分: {syllables}")
    
    candidates = engine.generate_candidate_chars(syllables)
    print(f"候选汉字: {candidates}")
    
    scored_names = engine.combine_and_score_names(last_name, candidates)
    print("\nTop 3 推荐名字:")
    for name, score in scored_names[:3]:
        print(f"{name} (评分: {score})")
