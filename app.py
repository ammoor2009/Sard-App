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

# تنسيق مخصص لتسهيل قراءة النتائج
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
        font-size: 20px;
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
# 2. محرك القواعد العروضية (Prosody Engine)
# -----------------------------------------------------------------------------
HARAKAT = ['َ', 'ُ', 'ِ', 'ً', 'ٌ', 'ٍ', 'ْ', 'ّ']
SHORT_HARAKAT = ['َ', 'ُ', 'ِ']
TANWEEN = {'ً': 'َنْ', 'ٌ': 'ُنْ', 'ٍ': 'ِنْ'}

def to_prosodic_text(text):
    """تحويل النص المشكول إلى كتابة عروضية أولية"""
    text = text.strip()
    
    # فك الشدة (الحرف المشدد = حرف ساكن + حرف متحرك)
    res = []
    i = 0
    n = len(text)
    while i < n:
        char = text[i]
        if char == 'ّ' and res:
            prev_char = res.pop()
            # تبحث عن الحركة الأخيرة قبل الشدة
            prev_haraka = ''
            if res and res[-1] in HARAKAT:
                prev_haraka = res.pop()
            
            # الشدة تعني حرف ساكن ثم نفس الحرف مع الحركة الجديدة
            next_haraka = ''
            if i + 1 < n and text[i+1] in SHORT_HARAKAT:
                next_haraka = text[i+1]
                i += 1
            
            res.append(prev_char)
            res.append('ْ')
            res.append(prev_char)
            if next_haraka:
                res.append(next_haraka)
        elif char in TANWEEN:
            res.append(TANWEEN[char])
        else:
            res.append(char)
        i += 1
        
    prosodic = "".join(res)
    
    # معالجة الألف الفارقة والوصل
    prosodic = re.sub(r'واً', 'وَنْ', prosodic)
    prosodic = re.sub(r'لْا', 'لَا', prosodic)
    
    return prosodic

def text_to_binary(text):
    """تحويل الكتابة العروضية إلى ترميز ثنائي (1 للمتحرك، 0 للساكن)"""
    binary = []
    i = 0
    n = len(text)
    
    while i < n:
        char = text[i]
        if char in HARAKAT or char in ['ا', 'و', 'ي']:
            pass
        else:
            # التحقق مما إذا كان الحرف متبوعاً بحركة أو سكون
            if i + 1 < n and text[i+1] in SHORT_HARAKAT:
                binary.append('1')
            elif i + 1 < n and text[i+1] == 'ْ':
                binary.append('0')
            elif char in ['ا', 'و', 'ي']:
                binary.append('0')
            else:
                # افتراض حركة إذا لم يشكل الحرف
                binary.append('1')
        i += 1
        
    return "".join(binary)

def detect_meter(binary_seq):
    """مطابقة الترميز الثنائي مع أوزان البحور الرئيسية"""
    # نماذج الأوزان الثنائية للبحور الأساسية
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
    return "بحر مجزوء أو تحتاج الضبط بالتشكيل الدقيق"

# -----------------------------------------------------------------------------
# 3. واجهة التفاعل والاستخدام
# -----------------------------------------------------------------------------
st.markdown("### ✍️ مُحَلِّلُ العَرُوضِ الآلِيِّ")
poem_text = st.text_area("أدخل البيت الشعري أو الشطر مشكولاً بدقة:", height=100, 
                         placeholder="مثال: عُلُوٌّ فِي الْحَيَاةِ وَفِي الْمَمَاتِ")

if st.button("تَقْطِيعُ النَّصِّ وَتَحْلِيلُهُ"):
    if poem_text.strip():
        prosodic_res = to_prosodic_text(poem_text)
        binary_res = text_to_binary(prosodic_res)
        meter_res = detect_meter(binary_res)
        
        st.write("---")
        st.markdown("#### 1️⃣ الكتابة العروضية:")
        st.markdown(f"<div class='prosody-text'>{prosodic_res}</div>", unsafe_allow_html=True)
        
        st.markdown("#### 2️⃣ الترميز الثنائي (1=متحرك ، 0=ساكن):")
        st.markdown(f"<div class='binary-code'>{binary_res}</div>", unsafe_allow_html=True)
        
        st.markdown("#### 3️⃣ البحر العروضي المترجح:")
        st.success(f"🎯 **{meter_res}**")
        
    else:
        st.warning("يرجى إدخال بيت شعري أو شطر مشكول أولاً.")

st.write("---")
st.caption("تطوير د. عمر الرواجفة © مختبر اللسانيات الحاسوبية")
