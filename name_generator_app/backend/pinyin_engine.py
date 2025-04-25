from pypinyin import lazy_pinyin

def get_initial_letter(name):
    pinyin = lazy_pinyin(name)
    return pinyin[0][0] if pinyin else ""
