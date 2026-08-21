import streamlit as st
import re

# -----------------------------------------------------------------------------
# 1. إعدادات الواجهة والتصاميم
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="مختبر العروض واللسانيات الحاسوبية",
    page_icon="📜",
    layout="centered"
)

# تنسيق الأزرار وجدول التقطيع المحاذى من اليمين إلى اليسار
st.markdown("""
    <style>
    /* زر التقطيع الرئيسي */
    div.stButton > button:first-child {
        background-color: #0d6efd;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 24px;
        width: 100%;
        border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #0b5ed7;
        color: white;
    }
    .prosody-text {
        font-size: 22px;
        font-weight: bold;
        color: #198754;
        text-align: center;
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
        direction: rtl;
    }
    /* حاوية جدول التقطيع المحاذى من اليمين لليسار */
    .taqtee-container {
        display: flex;
        flex-direction: row;
        direction: rtl;
        justify-content: flex-start;
        overflow-x: auto;
        padding: 10px 0;
        margin: 15px 0;
        gap: 4px;
    }
    .taqtee-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #f8f9fa;
        border: 1px solid #ced4da;
        border-radius: 6px;
        min-width: 36px;
        padding: 6px 4px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    .taqtee-char {
        font-size: 20px;
        font-weight: bold;
        color: #212529;
        margin-bottom: 4px;
    }
    .taqtee-symbol {
        font-size: 22px;
        font-weight: bold;
        color: #0d6efd;
        border-top: 1px dashed #adb5bd;
        width: 100%;
        text-align: center;
        padding-top: 2px;
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
# 6. قسم التفاعل مع الواجهة
# -----------------------------------------------------------------------------
if 'input_text' not in st.session_state:
    st.session_state['input_text'] = "عُلُوٌّ فِي الْحَيَاةِ وَفِي الْمَمَاتِ"

st.markdown("##### 💡 أمثلة وشواهد شعرية سريعة (اضغط للتجربة):")

col_ex1, col_ex2, col_ex3 = st.columns(3)

with col_ex1:
    if st.button("📌 البحر الطويل"):
        st.session_state['input_text'] = "عَلَى قَدْرِ أَهْلِ الْعَزْمِ تَأْتِي الْعَزَائِمُ"

with col_ex2:
    if st.button("📌 البحر الكامل"):
        st.session_state['input_text'] = "إِذَا المَرْءُ لَمْ يَدْنَسْ مِنَ اللُّؤْمِ عِرْضُهُ"

with col_ex3:
    if st.button("📌 البحر البسيط"):
        st.session_state['input_text'] = "الْخَيْلُ وَاللَّيْلُ وَالْبَيْدَاءُ تَعْرِفُنِي"

poem_text = st.text_area(
    "أدخل البيت الشعري أو الشطر مشكولاً بدقة:",
    value=st.session_state['input_text'],
    height=100
)

btn_col1, btn_col2 = st.columns([3, 1])

with btn_col1:
    analyze_btn = st.button("⚡ تَقْطِيعُ النَّصِّ وَتَحْلِيلُهُ")

with btn_col2:
    if st.button("🗑️ مسح"):
        st.session_state['input_text'] = ""
        st.rerun()

if analyze_btn:
    if poem_text.strip():
        prosodic_res = process_prosodic_rules(poem_text, is_end_of_verse=True)
        aligned_data = get_aligned_prosody(prosodic_res)
        symbols_res = "".join([s for _, s in aligned_data])
        meter_res = detect_meter(symbols_res)
        
        st.write("---")
        st.markdown("#### 1️⃣ الكتابة العروضية:")
        st.markdown(f"<div class='prosody-text'>{prosodic_res}</div>", unsafe_allow_html=True)
        
        st.markdown("#### 2️⃣ التقطيع المحاذى (من اليمين إلى اليسار):")
        
        # بناء بطاقات التقطيع باتجاه RTL من اليمين لليسار
        cards_html = "<div class='taqtee-container'>"
        for char_with_haraka, symbol in aligned_data:
            cards_html += f"""
            <div class='taqtee-card'>
                <div class='taqtee-char'>{char_with_haraka}</div>
                <div class='taqtee-symbol'>{symbol}</div>
            </div>
            """
        cards_html += "</div>"
        
        st.markdown(cards_html, unsafe_allow_html=True)
        
        st.markdown("#### 3️⃣ البحر العروضي المتوقع:")
        st.success(f"🎯 **{meter_res}**")
        
    else:
        st.warning("يرجى إدخال البيت الشعري أو الشطر مشكولاً أولاً.")

st.write("---")
st.caption("تطوير د. عمر الرواجفة © مختبر اللسانيات الحاسوبية")
