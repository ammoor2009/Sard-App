import streamlit as st
from google import genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="مختبر التحليل السردي", page_icon="📖", layout="wide")

# 2. تنسيق الواجهة (CSS)
st.markdown("""
    <style>
    .stTextArea textarea { color: #1e1e1e !important; background-color: #ffffff !important; }
    .result-box { background-color: #f8f9fa; color: #212529; padding: 20px; border-radius: 10px; border-right: 5px solid #0d6efd; direction: rtl; }
    </style>
""", unsafe_allow_html=True)

# 3. إعدادات التطبيق
st.title("📖 مختبر التحليل السردي والبنيوي")
st.subheader("د. عمر الرواجفة | قسم اللغة العربية وآدابها")

# جلب المفتاح من Secrets
API_KEY = st.secrets.get("GEMINI_API_KEY")

# 4. واجهة المستخدم
if 'text' not in st.session_state: st.session_state['text'] = ""

text = st.text_area("ضع النص السردي هنا:", value=st.session_state['text'], height=300)

if st.button("🔬 تَقْدِيمُ تَحْلِيلٍ سَرْدِيٍّ"):
    if not API_KEY:
        st.error("خطأ: تأكد من إضافة GEMINI_API_KEY في إعدادات Streamlit.")
    elif not text.strip():
        st.warning("الرجاء إدخال النص أولاً.")
    else:
        with st.spinner("جاري التحليل..."):
            try:
                # إنشاء العميل
                client = genai.Client(api_key=API_KEY)
                
                # نص الطلب (Prompt)
                prompt = f"""
                أنت خبير في النقد السردي والبنيوي. حلل النص التالي تحليلاً أكاديمياً دقيقاً:
                {text}
                
                المطلوب:
                1. الراوي والتبئير.
                2. الزمن السردي.
                3. الشخصيات والخطاب السردي.
                4. المونولوج واللغة.
                5. المكان والفضاء السردي.
                """

                # استدعاء الموديل بأبسط صيغة ممكنة
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt
                )

                st.markdown("### 📊 نتائج التحليل:")
                st.markdown(f"<div class='result-box'>{response.text}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"خطأ في الاتصال: {e}")
