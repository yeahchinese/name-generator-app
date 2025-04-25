from sound_map import sound_map

def english_to_pinyin(name):
    result = []
    name = name.lower()
    for ch in name:
        if ch in sound_map:
            result.append(sound_map[ch])
        else:
            result.append(["•"])
    return result