# prosody.py
import re

SHORT_HARAKAT = ['َ', 'ُ', 'ِ']
TANWEEN = {'ً': 'َنْ', 'ٌ': 'ُنْ', 'ٍ': 'ِنْ'}
SUN_LETTERS = ['ت', 'ث', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ل', 'ن']

SPECIAL_WORDS = {
    'الله': 'اللَاه',
    'الإله': 'الإِلَاه',
    'إله': 'إِلَاه',
    'الرحمن': 'الرَحْمَان',
    'هذا': 'هَذَا',
    'هذه': 'هَذِهِ',
    'هذان': 'هَذَانِ',
    'هؤلاء': 'هَؤُلَاءِ',
    'ذلك': 'ذَالِكَ',
    'طه': 'طَاهَا',
    'لكن': 'لَكِنْ'
}

def process_prosodic_rules(text, is_end_of_verse=True):
    words = text.split()
    processed_words = []
    for w in words:
        clean_w = re.sub(r'[ًٌٍَُِّْ]', '', w)
        if clean_w in SPECIAL_WORDS:
            w = SPECIAL_WORDS[clean_w]
        processed_words.append(w)
    text = " ".join(processed_words)

    text = re.sub(r'وا(\s|$)', r'و\1', text)

    for sun in SUN_LETTERS:
        text = re.sub(rf'(^|\s)ال([{sun}])', rf'\1\2َّ', text)
        text = re.sub(rf'(^|\s)َال([{sun}])', rf'\1\2َّ', text)
        
    text = re.sub(r'([^\s])\s*ال', r'\1لْ', text)
    text = re.sub(r'([^\s])\s*ٱ', r'\1', text)

    res = []
    i, n = 0, len(text)

    while i < n:
        char = text[i]
        if char == 'ّ' and res:
            prev_char = res.pop()
            if res and res[-1] in SHORT_HARAKAT:
                res.pop()
            next_haraka = 'َ'
            if i + 1 < n and text[i+1] in SHORT_HARAKAT:
                next_haraka = text[i+1]
                i += 1
            res.extend([prev_char, 'ْ', prev_char, next_haraka])
        elif char in TANWEEN:
            res.append('َا' if is_end_of_verse and i == n - 1 and char == 'ً' else TANWEEN[char])
        elif char == 'ة':
            res.append('هْ' if is_end_of_verse and (i == n - 1 or (i < n - 1 and text[i+1] in SHORT_HARAKAT and i+2 == n)) else 'ت')
        else:
            res.append(char)
        i += 1

    prosodic = "".join(res)
    prosodic = re.sub(r'([اىىَ])\s*([ْلْأإآتثجحخدذرزسشصضطظلعغفقكلمنهوي])ْ', r'\2ْ', prosodic)
    prosodic = re.sub(r'[اىى]\s*لْ', r'لْ', prosodic)
    prosodic = re.sub(r'ي\s*لْ', r'لْ', prosodic)
    prosodic = re.sub(r'ِي\s*([ْلْأإآتثجحخدذرزسشصضطظلعغفقكلمنهوي])ْ', r'\1ْ', prosodic)
    prosodic = re.sub(r'و\s*لْ', r'لْ', prosodic)
    prosodic = re.sub(r'ُو\s*([ْلْأإآتثجحخدذرزسشصضطظلعغفقكلمنهوي])ْ', r'\1ْ', prosodic)

    if is_end_of_verse and prosodic:
        if prosodic[-1] == 'َ': prosodic = prosodic[:-1] + 'َا'
        elif prosodic[-1] == 'ُ': prosodic = prosodic[:-1] + 'ُو'
        elif prosodic[-1] == 'ِ': prosodic = prosodic[:-1] + 'ِي'

    return prosodic

def get_aligned_prosody(prosodic_text):
    aligned = []
    text = re.sub(r'\s+', '', prosodic_text)
    i, n = 0, len(text)

    while i < n:
        char = text[i]
        if char in SHORT_HARAKAT:
            i += 1
            continue
        next_char = text[i+1] if i + 1 < n else ''

        if next_char == 'ْ':
            aligned.append((char + 'ْ', '○'))
            i += 2
        elif next_char in SHORT_HARAKAT:
            aligned.append((char + next_char, '/'))
            i += 2
        elif char in ['ا', 'و', 'ي', 'ى']:
            aligned.append((char, '○'))
            i += 1
        else:
            aligned.append((char, '/'))
            i += 1

    return aligned
