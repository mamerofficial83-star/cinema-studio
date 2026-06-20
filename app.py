import streamlit as st
import google.generativeai as genai

# إعداد الواجهة لتكون احترافية
st.set_page_config(page_title="Cinematic Director Studio", layout="wide")
st.title("🎬 DIRECTOR'S PROTOCOL: Cinematic Production Suite")

# إدخال المفتاح (للأمان)
api_key = st.sidebar.text_input("أدخل مفتاح Google API الخاص بك:", type="password")

def run_production_engine(story, style, aspect_ratio):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt = f"""
    أنت مدير إنتاج سينمائي. مهمتك تفكيك القصة إلى 9 سطور (مشاهد) في كل دفعة.
    الأسلوب السينمائي: {style}
    مقاس الكادر: {aspect_ratio}
    التعليمات الإجبارية:
    1. لا موسيقى، لا حوار، صمت تام، مؤثرات بيئية فقط.
    2. مطالبات Veo3 للتحريك: واقعية، 8 ثوانٍ، حركة كاميرا سينمائية (Pan, Tilt, Dolly).
    3. وصف الشخصيات: ثابت ومفصل كما تم الاتفاق عليه سابقاً.
    4. يمنع منعاً باتاً وجود نصوص إنجليزية أو رموز غير عربية.
    القصة: {story}
    """
    response = model.generate_content(prompt)
    return response.text

# الواجهة
col1, col2 = st.columns([1, 2])
with col1:
    style = st.selectbox("الأسلوب:", ["واقعي", "أنيمي", "دراما تاريخية"])
    ratio = st.selectbox("المقاس:", ["16:9", "2.35:1", "9:16"])
    submit = st.button("توليد المشاهد والتحريك")

with col2:
    story = st.text_area("ضع القصة هنا (سطر لكل مشهد):", height=300)

if submit and api_key:
    with st.spinner("جاري معالجة الإنتاج السينمائي..."):
        result = run_production_engine(story, style, ratio)
        st.markdown("### 📋 نتائج الإنتاج:")
        st.write(result)
