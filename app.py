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
    .binary-code {
        font-family: 'Courier New', monospace;
        font-size: 24px;
        font-weight: bold;
        color: #0d6efd;
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        letter-spacing: 2px;
    }
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

# الألفات الخنجرية والكلمات ذات المحذوف الإملائي (قواعد 6، 17)
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
    'أولئك': 'أُلَائِك'  # حذف الواو الزائدة (قاعدة 7)
}

# -----------------------------------------------------------------------------
# 3. محرك الكتابة العروضية وفق الشروط الـ 19
# -----------------------------------------------------------------------------
def process_prosodic_rules(text, is_end_of_verse=True):
    """
    تطبيق قواعد الكتابة العروضية الشاملة:
    ما ينطق يكتب، ما لا ينطق يحذف، فك الشدة، التنوين، أل الشمسية/القمرية،
    همزة الوصل، الألف الفارقة، والوقف.
    """
    # استبدال الكلمات الخاصة ذات الألف الخنجرية والواو الزائدة (قواعد 6، 7، 17)
    words = text.split()
    processed_words = []
    for w in words:
        clean_w = re.sub(r'[ًٌٍَُِّْ]', '', w)
        if clean_w in SPECIAL_WORDS:
            w = SPECIAL_WORDS[clean_w]
        processed_words.append(w)
    text = " ".join(processed_words)

    # القاعدة 12: حذف الألف الفارقة بعد واو الجماعة (وا -> و)
    text = re.sub(r'وا(\s|$)', r'و\1', text)

    # القاعدة 10 & 11: معالجة (أل) الشمسية والقمرية + همزة الوصل (قاعدة 8)
    # 1. (أل) الشمسية: حذف (أل) وتضعيف الحرف الشمسي عند الوصل أو الابتداء
    for sun in SUN_LETTERS:
        # في بداية الكلام: ال + حرف شمسي -> الحرف الشمسي مشدد
        text = re.sub(rf'(^|\s)ال([{sun}])', rf'\1\2َّ', text)
        text = re.sub(rf'(^|\s)َال([{sun}])', rf'\1\2َّ', text)
        
    # 2. (أل) القمرية وهمزة الوصل عند الوصل (قاعدة 8 و11)
    # حذف همزة الوصل في (الـ) القمرية إذا سبقت بحرف
    text = re.sub(r'([^\s])\s*ال', r'\1لْ', text)
    # حذف همزة الوصل العامة في درج الكلام (ابن، اسم، است، إلخ)
    text = re.sub(r'([^\s])\s*ٱ', r'\1', text)

    # معالجة الشدة والتشكيل والتنوين حرفاً بحرف
    res = []
    i = 0
    n = len(text)

    while i < n:
        char = text[i]

        # القاعدة 3 & 10: فك الحرف المشدد إلى (ساكن + متحرك)
        if char == 'ّ' and res:
            prev_char = res.pop()
            # التقاط الحركة السابقة إن وجدت
            prev_haraka = ''
            if res and res[-1] in SHORT_HARAKAT:
                prev_haraka = res.pop()

            # الحركة التالية للشدة
            next_haraka = 'َ'
            if i + 1 < n and text[i+1] in SHORT_HARAKAT:
                next_haraka = text[i+1]
                i += 1

            res.append(prev_char)
            res.append('ْ')  # الأول ساكن
            res.append(prev_char)
            res.append(next_haraka)  # الثاني متحرك

        # القاعدة 4 & 15: التنوين يكتب نوناً ساكنة في الوصل
        elif char in TANWEEN:
            if is_end_of_verse and i == n - 1:
                # القاعدة 15: يسقط التنوين عند الوقف (أو يقلب ألفاً في تنوين الفتح)
                if char == 'ً':
                    res.append('َا')
            else:
                res.append(TANWEEN[char])

        # القاعدة 16: التاء المربوطة (تاء في الوصل، هاء عند الوقف)
        elif char == 'ة':
            if is_end_of_verse and (i == n - 1 or (i < n - 1 and text[i+1] in SHORT_HARAKAT and i+2 == n)):
                res.append('هْ')
            else:
                res.append('ت')

        else:
            res.append(char)

        i += 1

    prosodic = "".join(res)

    # القاعدة 2 & 18: حذف حروف المد عند التقاء الساكنين في الوصل
    prosodic = re.sub(r'([َاِوُ])\s+([ْأإإآاىل])', r'\2', prosodic)

    # القاعدة 14: معالجة الوقف في نهاية الشطر/البيت (إشباع الحركة الأخيرة)
    if is_end_of_verse and prosodic:
        if prosodic[-1] == 'َ':
            prosodic = prosodic[:-1] + 'َا'
        elif prosodic[-1] == 'ُ':
            prosodic = prosodic[:-1] + 'ُو'
        elif prosodic[-1] == 'ِ':
            prosodic = prosodic[:-1] + 'ِي'

    return prosodic

# -----------------------------------------------------------------------------
# 4. تحويل النص العروضي إلى ترميز ثنائي (1/0)
# -----------------------------------------------------------------------------
def text_to_binary(prosodic_text):
    """
    تحويل الكتابة العروضية إلى ترميز ثنائي:
    1 = متحرك
    0 = ساكن
    """
    binary = []
    text = re.sub(r'\s+', '', prosodic_text)  # إزالة الفواصل
    i = 0
    n = len(text)

    while i < n:
        char = text[i]
        
        if char in SHORT_HARAKAT:
            i += 1
            continue

        # فحص الحرف التالي لتحديد هل هو متحرك أم ساكن
        next_char = text[i+1] if i + 1 < n else ''

        if next_char == 'ْ' or char in ['ا', 'و', 'ي', 'ى', 'ءْ']:
            binary.append('0')
            if next_char == 'ْ':
                i += 1
        elif next_char in SHORT_HARAKAT:
            binary.append('1')
        else:
            # افتراض الحركة إذا لم يحدد السكون
            binary.append('1')

        i += 1

    return "".join(binary)

# -----------------------------------------------------------------------------
# 5. مطابقة البحور الشعريّة
# -----------------------------------------------------------------------------
def detect_meter(binary_seq):
    meters = {
        "البحر الطويل": ["1101011010101101011010", "11010110101011010110110"],
        "البحر البسيط": ["1101101011011010", "110110101101101011011010"],
        "البحر الكامل": ["111010111010111010", "110101101011010"],
        "البحر الوافر": ["1101110110111011010", "11011101101110"],
        "البحر الخفيف": ["1011010101101010110", "10110101011010"],
        "البحر الرجز": ["110110101101101011011010"]
    }
    
    clean_seq = binary_seq.replace(" ", "")
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
        binary_res = text_to_binary(prosodic_res)
        meter_res = detect_meter(binary_res)
        
        st.write("---")
        st.markdown("#### 1️⃣ الكتابة العروضية (تطبيق القواعد الـ 19):")
        st.markdown(f"<div class='prosody-text'>{prosodic_res}</div>", unsafe_allow_html=True)
        
        st.markdown("#### 2️⃣ الترميز الثنائي (1=متحرك ، 0=ساكن):")
        st.markdown(f"<div class='binary-code'>{binary_res}</div>", unsafe_allow_html=True)
        
        st.markdown("#### 3️⃣ البحر العروضي:")
        st.success(f"🎯 **{meter_res}**")
        
    else:
        st.warning("يرجى إدخل البيت الشعري أو الشطر مشكولاً أولاً.")

st.write("---")
st.caption("تطوير د. عمر الرواجفة © مختبر اللسانيات الحاسوبية")
