# app.py
import streamlit as st
# استيراد الوظائف من الملفات الخارجيّة
from prosody import process_prosodic_rules, get_aligned_prosody
from meters import detect_meter

st.set_page_config(page_title="مختبر العروض واللسانيات الحاسوبية", page_icon="📜", layout="centered")

st.markdown("<style>.prosody-text { font-size: 22px; font-weight: bold; color: #198754; text-align: center; }</style>", unsafe_allow_html=True)

st.title("📜 مختبر العروض واللسانيات الحاسوبية")
st.subheader("د. عمر الرواجفة")
st.write("---")

poem_text = st.text_area("أدخل البيت الشعري أو الشطر مشكولاً بدقة:", height=100, placeholder="مثال: عُلُوٌّ فِي الْحَيَاةِ وَفِي الْمَمَاتِ")

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
