import streamlit as st
import re

# -----------------------------------------------------------------------------
# 1. إعدادات الصفحة والواجهة
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="مختبر العروض واللسانيات الحاسوبية",
    page_icon="📜",
    layout="centered"
)

st.markdown("""
    <style>
    .prosody-text {
        font-size: 22px;
        font-weight: bold;
        color: #198754;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📜 مختبر العروض واللسانيات الحاسوبية")
st.subheader("د. عمر الرواجفة")
st.write("---")

# -----------------------------------------------------------------------------
# 2. ثوابت اللغة والرموز
# -----------------------------------------------------------------------------
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
    'ذلكما': 'ذَالِكُمَا',
    'ذلكم': 'ذَالِكُمْ',
    'طه': 'طَاهَا',
    'لكن': 'لَكِنْ',
    'لكنَّ': 'لَكِنَّ',
    'أولئك': 'أُلَائِك'
}

# -----------------------------------------------------------------------------
# 3. محرك الكتابة العروضية
# -----------------------------------------------------------------------------
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
    i = 0
    n = len(text)

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

            res.append(prev_char)
            res.append('ْ')
            res.append(prev_char)
            res.append(next_haraka)

        elif char in TANWEEN:
            if is_end_of_verse and i == n - 1:
                if char == 'ً':
                    res.append('َا')
            else:
                res.append(TANWEEN[char])

        elif char == 'ة':
            if is_end_of_verse and (i == n - 1 or (i < n - 1 and text[i+1] in SHORT_HARAKAT and i+2 == n)):
                res.append('هْ')
            else:
                res.append('ت')

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
    prosodic = re.sub(r'([َاِوُ])\s+([ْأإآاىل])', r'\2', prosodic)

    if is_end_of_verse and prosodic:
        if prosodic[-1] == 'َ':
            prosodic = prosodic[:-1] + 'َا'
        elif prosodic[-1] == 'ُ':
            prosodic = prosodic[:-1] + 'ُو'
        elif prosodic[-1] == 'ِ':
            prosodic = prosodic[:-1] + 'ِي'

    return prosodic

# -----------------------------------------------------------------------------
# 4. تفكيك النص العروضي إلى أزواج محاذاتية
# -----------------------------------------------------------------------------
def get_aligned_prosody(prosodic_text):
    aligned = []
    text = re.sub(r'\s+', '', prosodic_text)
    i = 0
    n = len(text)

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

# -----------------------------------------------------------------------------
# 5. مطابقة البحور
# -----------------------------------------------------------------------------
def detect_meter(symbol_seq):
    meters = {
        "البحر الطويل": ["//○/○//○/○//○/○//○/○", "//○/○//○/○//○/○//○//○"],
        "البحر البسيط": ["//○//○/○//○//○/○", "//○//○/○//○//○/○//○//○/○"],
        "البحر الكامل": ["///○/○///○/○///○/○", "//○/○//○/○//○/○"],
        "البحر الوافر": ["//○///○//○///○//○/○", "//○///○//○///○"],
        "البحر الخفيف": ["/○//○/○/○//○/○/○//○", "/○//○/○/○//○/○"],
        "البحر الرجز": ["//○//○/○//○//○/○//○//○/○"]
    }
    
    clean_seq = symbol_seq.replace(" ", "")
    for meter, patterns in meters.items():
        for pattern in patterns:
            if pattern in clean_seq or clean_seq in pattern:
                return meter
    return "بحر مجزوء أو ينبغي التحقق من دقة التشكيل"

# -----------------------------------------------------------------------------
# 6. واجهة الاستخدام
# -----------------------------------------------------------------------------
st.markdown("### ✍️ مُحَلِّلُ العَرُوضِ الآلِيِّ")
poem_text = st.text_area("أدخل البيت الشعري أو الشطر مشكولاً بدقة:", height=100, 
                         placeholder="مثال: عُلُوٌّ فِي الْحَيَاةِ وَفِي الْمَمَاتِ")

if st.button("تَقْطِيعُ النَّصِّ وَتَحْلِيلُهُ"):
    if poem_text.strip():
        prosodic_res = process_prosodic_rules(poem_text, is_end_of_verse=True)
        aligned_data = get_aligned_prosody(prosodic_res)
        symbols_res = "".join([s for _, s in aligned_data])
        meter_res = detect_meter(symbols_res)
        
        st.write("---")
        st.markdown("#### 1️⃣ الكتابة العروضية:")
        st.markdown(f"<div class='prosody-text'>{prosodic_res}</div>", unsafe_allow_html=True)
        
        st.markdown("#### 2️⃣ التقطيع المحاذى (/ = متحرك ، ○ = ساكن):")
        
        # عرض محاذى متجاوب باستخدام أعمدة Streamlit
        cols = st.columns(len(aligned_data))
        for idx, (char_with_haraka, symbol) in enumerate(aligned_data):
            with cols[idx]:
                st.metric(label=char_with_haraka, value=symbol)
        
        st.markdown("#### 3️⃣ البحر العروضي:")
        st.success(f"🎯 **{meter_res}**")
        
    else:
        st.warning("يرجى إدخال البيت الشعري أو الشطر مشكولاً أولاً.")

st.write("---")
st.caption("تطوير د. عمر الرواجفة © مختبر اللسانيات الحاسوبية")
