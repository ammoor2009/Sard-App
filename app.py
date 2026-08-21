import streamlit as st
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# 1. إعدادات الواجهة والصفحة
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="مُحَلِّلُ النَّصِّ النَّرْدِيِّ وَالسَّرْدِيِّ",
    page_icon="📖",
    layout="wide"
)

st.markdown("""
    <style>
    .stTextArea textarea {
        font-size: 17px !important;
        line-height: 1.8 !important;
        direction: rtl !important;
        border-radius: 10px !important;
        background-color: #ffffff !important;
        color: #1e1e1e !important;
    }
    div[data-baseweb="textarea"] textarea {
        color: #1e1e1e !important;
    }
    div.stButton > button[key="analyze_btn"] {
        background-color: #198754 !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        width: 100% !important;
        border: none !important;
    }
    div.stButton > button[key="clear_btn"] {
        background-color: #dc3545 !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        width: 100% !important;
        border: none !important;
    }
    .result-box {
        background-color: #f8f9fa;
        color: #212529;
        padding: 22px;
        border-radius: 10px;
        border-right: 5px solid #0d6efd;
        direction: rtl;
        font-size: 16px;
        line-height: 1.8;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. استدعاء المفتاح بأمان
# -----------------------------------------------------------------------------
API_KEY = st.secrets.get("GEMINI_API_KEY", "")

st.title("📖 مختبر التحليل السردي والبنيوي")
st.subheader("د. عمر الرواجفة | قسم اللغة العربية وآدابها")
st.write("أداة أكاديمية لتفكيك النصوص السردية وفق مناهج النقد الحديث.")
st.write("---")

# -----------------------------------------------------------------------------
# 3. الواجهة
# -----------------------------------------------------------------------------
if 'narrative_text' not in st.session_state:
    st.session_state['narrative_text'] = ""

narrative_input = st.text_area(
    "ضع النص السردي هنا:",
    value=st.session_state['narrative_text'],
    height=380,
    placeholder="انسخ النص السردي..."
)

col_btn1, col_btn2 = st.columns([3, 1])

with col_btn1:
    analyze_click = st.button("🔬 تَقْدِيمُ تَحْلِيلٍ سَرْدِيٍّ شَامِلٍ", key="analyze_btn")
with col_btn2:
    clear_click = st.button("🗑️ مسح النص", key="clear_btn")

if clear_click:
    st.session_state['narrative_text'] = ""
    st.rerun()

# -----------------------------------------------------------------------------
# 4. محرك التحليل (باستخدام الموديل الأكثر استقراراً)
# -----------------------------------------------------------------------------
if analyze_click:
    if not API_KEY:
        st.error("يرجى إضافة GEMINI_API_KEY في إعدادات Streamlit.")
    elif not narrative_input.strip():
        st.warning("يرجى إدخال النص أولاً.")
    else:
        with st.spinner("جاري التحليل..."):
            try:
                client = genai.Client(api_key=API_KEY)
                
                # استخدام الموديل المستقر
                model_id = 'gemini-1.5-flash' 
                
                prompt = f"""
                أنت ناقد أدبي وخبير أكاديمي متخصص في النقد السردي.
                حلل النص التالي تحليلاً بنيوياً:
                {narrative_input}
                
                المطلوب:
                1. الراوي والتبئير.
                2. الزمن السردي (استرجاع، استباق، سرعة).
                3. الشخصيات والخطاب السردي.
                4. المونولوج واللغة.
                5. المكان والفضاء السردي.
                """

                response = client.models.generate_content(
                    model=model_id,
                    contents=prompt
                )

                st.markdown("### 📊 نتائج التحليل:")
                st.markdown(f"<div class='result-box'>{response.text}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالخادم (قد يكون ضغطاً مؤقتاً): {e}")

st.caption("تطوير د. عمر الرواجفة © مختبر اللسانيات الحاسوبية")
