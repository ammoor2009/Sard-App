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

# تخصيص التصميم ومظهر الأزرار ومربع النص
st.markdown("""
    <style>
    /* تنسيق مربع النص الكبير */
    .stTextArea textarea {
        font-size: 17px !important;
        line-height: 1.8 !important;
        direction: rtl !important;
        border-radius: 10px !important;
        background-color: #fdfdfd !important;
    }
    /* زر التحليل السردي */
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
    div.stButton > button[key="analyze_btn"]:hover {
        background-color: #157347 !important;
    }
    /* زر المسح */
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
    div.stButton > button[key="clear_btn"]:hover {
        background-color: #bb2d3b !important;
    }
    /* صندوق عرض النتائج */
    .result-box {
        background-color: #f8f9fa;
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
# 2. استدعاء مفتاح API بأمان من Streamlit Secrets
# -----------------------------------------------------------------------------
API_KEY = st.secrets.get("GEMINI_API_KEY", "")

st.title("📖 مختبر التحليل السردي والبنيوي")
st.subheader("د. عمر الرواجفة | قسم اللغة العربية وآدابها")
st.write("أداة أكاديمية تفاعلية قائمة على الذكاء الاصطناعي لتفكيك النصوص الروائية والقصصية وفق مناهج النقد السردي والسيميائيات الحديثة.")
st.write("---")

# -----------------------------------------------------------------------------
# 3. مربع النص وإدارة الأزرار
# -----------------------------------------------------------------------------
if 'narrative_text' not in st.session_state:
    st.session_state['narrative_text'] = ""

narrative_input = st.text_area(
    "ضع النص السردي (رواية، قصّة، مقطع سردي) هنا للتحليل الكامل:",
    value=st.session_state['narrative_text'],
    height=380,
    placeholder="انسخ النص السردي الطويل واكتبه هنا (يتسع لمئات الكلمات والصفحات)..."
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
# 4. محرك التحليل بالذكاء الاصطناعي
# -----------------------------------------------------------------------------
if analyze_click:
    if not API_KEY:
        st.error("⚠️ لم يتم العثور على مفتاح GEMINI_API_KEY داخل Secrets. يرجى إضافته في إعدادات Streamlit Cloud.")
    elif not narrative_input.strip():
        st.warning("يرجى إدخال النص السردي أولاً قبل بدء التحليل.")
    else:
        with st.spinner("جاري تفكيك النص السردي وتحليله وفق المناهج النقديّة والسيميائية..."):
            try:
                client = genai.Client(api_key=API_KEY)
                
                prompt = f"""
                أنت ناقد أدبي وخبير أكاديمي متخصص في النقد السردي والسيميائيات (مناهج جيرار جينيت، ورولان بارت، والناقدين العرب).
                قم بإجراء تحليل نقد بنيوي حاسوبي ودقيق للنص الأدبي المرفق أدناه:

                النص السردي:
                \"\"\"
                {narrative_input}
                \"\"\"

                المطلوب تقديم تقرير نقد بنيوي شامل ومفصل يحتوي على المحاور التالية بشكل مباشر ومقسم بوضوح:

                1. **الراوي والتبئير (Focalization):**
                   - نوع الراوي (مشارِك/عليم/خارجي) مع تحديد ضمير السرد الأغلب.
                   - نوع التبئير (صفر/داخلي/خارجي) وتحولاته داخل النص.

                2. **الزمن السردي (Narrative Time):**
                   - المفارقات الزمنية (الاسترجاع Analepsis / الاستباق Prolepsis).
                   - السرعة السردية (الخلاصة، المشهد، الوقفات الوصفية، الحذف).

                3. **الشخصيات والخطاب السردي:**
                   - الشخصيات (رئيسية/ثانوية) ودورها العاملِي (Actantial Model).
                   - أشكال الخطاب (مباشر، غير مباشر، غير مباشر حر).

                4. **المونولوج واللغة السردية:**
                   - النجوى الداخلية (المونولوج الباطني) والتداعي الحر للأفكار.
                   - مستويات اللغة السردية والأنساق المعجمية والدلالية الأبرز.

                5. **المكان والفضاء السردي (Space & Setting):**
                   - طبيعة أطر المكان (مغلق/مفتوح، أليف/معادٍ) وعلاقته بحالة الشخصيات النفسية والدلالية.
                """

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.3
                    )
                )

                st.write("---")
                st.markdown("### 📊 نتائج التحليل السردي والنقدي:")
                st.markdown(f"<div class='result-box'>{response.text}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"حدث خطأ أثناء إجراء التحليل: {e}")

st.write("---")
st.caption("تطوير د. عمر الرواجفة © مختبر اللسانيات الحاسوبية وتحليل الخطاب")
