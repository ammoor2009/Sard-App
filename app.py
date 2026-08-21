import streamlit as st

# إعدادات صفحة الموقع
st.set_page_config(
    page_title="منصة العروض واللسانيات الحاسوبية",
    page_icon="📜",
    layout="centered"
)

# عنوان الموقع
st.title("📜 مختبر العروض واللسانيات الحاسوبية")
st.subheader("د. عمر الرواجفة")
st.write("---")

# واجهة التقطيع العروضي
st.markdown("### ✍️ مُحَلِّلُ العَرُوضِ الآلِيِّ")
poem_text = st.text_input("أدخل البيت الشعري مشكولاً بدقة:")

if st.button("تقطيع البيت الشعري"):
    if poem_text:
        st.info(f"البيت المدخل: **{poem_text}**")
        # محاكاة لنتيجة التقطيع
        st.success("جاري تحليل السلسلة الصوتية ومطابقتها مع أوزان الخليل...")
        st.code("11010 1101010 11010 110110", language="text")
        st.markdown("**البحر المتوقع:** البحر الطويل (تام)")
    else:
        st.warning("يرجى كتابة بيت شعري أولاً.")

st.write("---")
st.caption("جميع الحقوق محفوظة © منصة اللسانيات الحاسوبية")
