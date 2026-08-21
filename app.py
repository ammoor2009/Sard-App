import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="مختبر التحليل السردي", page_icon="📖", layout="wide")

st.title("📖 مختبر التحليل السردي والبنيوي")
st.subheader("د. عمر الرواجفة | قسم اللغة العربية وآدابها")
st.write("أداة أكاديمية لتفكيك النصوص الروائية والقصصية وفق مناهج النقد السردي الحديث.")
st.write("---")

# 2. جلب المفتاح وإعداد العميل
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ لم يتم العثور على GEMINI_API_KEY في إعدادات Streamlit Secrets.")

# 3. إدخال النص
text_input = st.text_area(
    "ضع النص السردي هنا للتحليل الشامل:",
    height=300,
    placeholder="انسخ النص السردي واكتبه هنا..."
)

col1, col2 = st.columns([3, 1])
with col1:
    btn_analyze = st.button("🔬 تقديم تحليل سردي شامل", type="primary", use_container_width=True)
with col2:
    if st.button("🗑️ مسح النص", use_container_width=True):
        st.rerun()

# 4. إرسال النص واستقبال النتيجة فقط
if btn_analyze:
    if not api_key:
        st.error("يرجى إضافة مفتاح API أولاً.")
    elif not text_input.strip():
        st.warning("يرجى إدخال النص السردي أولاً.")
    else:
        with st.spinner("جاري إرسال النص لمعالجته ونقده..."):
            try:
                # استدعاء النموذج المباشر
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                أنت ناقد أدبي وخبير أكاديمي متخصص في النقد السردي والسيميائيات (مناهج جيرار جينيت، ورولان بارت، والناقدين العرب).
                قم بإجراء تحليل بنيوي دقيق للنص الأدبي المرفق أدناه:

                النص السردي:
                \"\"\"
                {text_input}
                \"\"\"

                المطلوب تقديم تقرير نقد بنيوي شامل يحتوي على المحاور التالية بشكل مباشر:
                1. الراوي والتبئير (Focalization)
                2. الزمن السردي (Narrative Time)
                3. الشخصيات والخطاب السردي (Actantial Model)
                4. المونولوج واللغة السردية
                5. المكان والفضاء السردي (Space & Setting)
                """

                # الطلب يرسل النص إلى سيرفرات الذكاء الاصطناعي ويعود بنص فقط
                response = model.generate_content(prompt)
                
                st.write("---")
                st.markdown("### 📊 نتائج التحليل السردي والنقدي:")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال: {e}")

st.write("---")
st.caption("تطوير د. عمر الرواجفة © مختبر اللسانيات الحاسوبية وتحليل الخطاب")
