import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="مختبر التحليل السردي", page_icon="📖", layout="wide")

# إعداد المفتاح
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    # إعداد النموذج
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("مفتاح API مفقود!")

# الواجهة
st.title("📖 مختبر التحليل السردي والبنيوي")
if 'text' not in st.session_state: st.session_state['text'] = ""
text = st.text_area("ضع النص السردي هنا:", value=st.session_state['text'], height=300)

if st.button("🔬 تَقْدِيمُ تَحْلِيلٍ سَرْدِيٍّ"):
    if not api_key:
        st.error("تأكد من إضافة GEMINI_API_KEY في إعدادات Streamlit.")
    elif not text.strip():
        st.warning("الرجاء إدخال النص أولاً.")
    else:
        with st.spinner("جاري التحليل..."):
            try:
                response = model.generate_content(f"حلل النص التالي بنيوياً: {text}")
                st.markdown("### 📊 نتائج التحليل:")
                st.write(response.text)
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال: {e}")
