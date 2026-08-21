import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="مختبر التحليل السردي", page_icon="📖", layout="wide")

# 2. التنسيق والواجهة
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

# 3. جلب مفتاح API
api_key = st.secrets.get("GEMINI_API_KEY")

st.title("📖 مختبر التحليل السردي والبنيوي")
st.subheader("د. عمر الرواجفة | قسم اللغة العربية وآدابها")
st.write("أداة أكاديمية تفاعلية لتفكيك النصوص الروائية والقصصية وفق مناهج النقد السردي الحديث.")
st.write("---")

if 'text' not in st.session_state:
    st.session_state['text'] = ""

text_input = st.text_area(
    "ضع النص السردي هنا للتحليل الشامل:",
    value=st.session_state['text'],
    height=350,
    placeholder="انسخ النص السردي واكتبه هنا..."
)

col1, col2 = st.columns([3, 1])

with col1:
    btn_analyze = st.button("🔬 تَقْدِيمُ تَحْلِيلٍ سَرْدِيٍّ شَامِلٍ", type="primary", use_container_width=True)

with col2:
    btn_clear = st.button("🗑️ مسح النص", use_container_width=True)

if btn_clear:
    st.session_state['text'] = ""
    st.rerun()

# 4. إجراء التحليل المباشر بواسطة HTTP REST Request
if btn_analyze:
    if not api_key:
        st.error("⚠️ لم يتم العثور على GEMINI_API_KEY في إعدادات Streamlit Secrets.")
    elif not text_input.strip():
        st.warning("يرجى إدخال النص السردي أولاً.")
    else:
        with st.spinner("جاري تفكيك النص وتحليله نقديّاً..."):
            try:
                # رابط الاتصال المباشر الرسمي بإصدار v1
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                prompt = f"""
                أنت ناقد أدبي وخبير أكاديمي متخصص في النقد السردي والسيميائيات (مناهج جيرار جينيت، ورولان بارت، والناقدين العرب).
                قم بإجراء تحليل نقد بنيوي حاسوبي ودقيق للنص الأدبي المرفق أدناه:

                النص السردي:
                \"\"\"
                {text_input}
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

                payload = {
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }]
                }

                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, json=payload, headers=headers)
                res_json = response.json()

                if response.status_code == 200:
                    analysis_result = res_json['candidates'][0]['content']['parts'][0]['text']
                    st.write("---")
                    st.markdown("### 📊 نتائج التحليل السردي والنقدي:")
                    st.markdown(f"<div class='result-box'>{analysis_result}</div>", unsafe_allow_html=True)
                else:
                    st.error(f"خطأ من API: {res_json.get('error', {}).get('message', 'خطأ غير معروف')}")

            except Exception as e:
                st.error(f"حدث خطأ أثناء إجراء التحليل: {e}")

st.write("---")
st.caption("تطوير د. عمر الرواجفة © مختبر اللسانيات الحاسوبية وتحليل الخطاب")
