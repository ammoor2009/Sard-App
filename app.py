import streamlit as st
# استيراد دالّات التقطيع والبحور من الملفات الفرعية (إذا أنشأتها) 
# أو استخدام المحرك المباشر
from prosody import process_prosodic_rules, get_aligned_prosody
from meters import detect_meter

# -----------------------------------------------------------------------------
# 1. إعدادات الواجهة والتصاميم
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="مختبر العروض واللسانيات الحاسوبية",
    page_icon="📜",
    layout="centered"
)

# تنسيق الأزرار والبطاقات
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
    }
    </style>
""", unsafe_allow_html=True)

st.title("📜 مختبر العروض واللسانيات الحاسوبية")
st.subheader("د. عمر الرواجفة")
st.write("---")

# إدارة حالة النص بين الضغطات
if 'input_text' not in st.session_state:
    st.session_state['input_text'] = "عُلُوٌّ فِي الْحَيَاةِ وَفِي الْمَمَاتِ"

# -----------------------------------------------------------------------------
# 2. قسم أزرار الأمثلة السريعة
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# 3. صندوق إدخال النص الأولي
# -----------------------------------------------------------------------------
poem_text = st.text_area(
    "أدخل البيت الشعري أو الشطر مشكولاً بدقة:",
    value=st.session_state['input_text'],
    height=100
)

# -----------------------------------------------------------------------------
# 4. أزرار التحكم والعمليات
# -----------------------------------------------------------------------------
btn_col1, btn_col2 = st.columns([3, 1])

with btn_col1:
    analyze_btn = st.button("⚡ تَقْطِيعُ النَّصِّ وَتَحْلِيلُهُ")

with btn_col2:
    if st.button("🗑️ مسح"):
        st.session_state['input_text'] = ""
        st.rerun()

# -----------------------------------------------------------------------------
# 5. تنفيذ التقطيع وعرض النتائج
# -----------------------------------------------------------------------------
if analyze_btn:
    if poem_text.strip():
        prosodic_res = process_prosodic_rules(poem_text, is_end_of_verse=True)
        aligned_data = get_aligned_prosody(prosodic_res)
        symbols_res = "".join([s for _, s in aligned_data])
        meter_res = detect_meter(symbols_res)
        
        st.write("---")
        st.markdown("#### 1️⃣ الكتابة العروضية:")
        st.markdown(f"<div class='prosody-text'>{prosodic_res}</div>", unsafe_allow_html=True)
        
        st.markdown("#### 2️⃣ التقطيع المحاذى (/ = متحرك ، ○ = ساكن):")
        
        # عرض محاذى متجاوب باستخدام أعمدة التقطيع
        cols = st.columns(len(aligned_data))
        for idx, (char_with_haraka, symbol) in enumerate(aligned_data):
            with cols[idx]:
                st.metric(label=char_with_haraka, value=symbol)
        
        st.markdown("#### 3️⃣ البحر العروضي المتوقع:")
        st.success(f"🎯 **{meter_res}**")
        
    else:
        st.warning("يرجى إدخال البيت الشعري أو الشطر مشكولاً أولاً.")

st.write("---")
st.caption("تطوير د. عمر الرواجفة © مختبر اللسانيات الحاسوبية")
