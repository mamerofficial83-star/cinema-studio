import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="Cinema Director AI", layout="wide")
st.title("🎬 استوديو الإنتاج السينمائي المتكامل")

# الشريط الجانبي
with st.sidebar:
    api_key = st.text_input("أدخل مفتاح API:", type="password")
    st.divider()
    style = st.selectbox("الأسلوب:", ["واقعي", "أنيمي", "دراما تاريخية"])
    ratio = st.selectbox("مقاس الكادر:", ["16:9", "2.35:1", "9:16"])
    era = st.text_input("الفترة الزمنية:", placeholder="مثلاً: العصر العباسي")

# المحتوى الرئيسي
story = st.text_area("أدخل قصتك هنا:", height=200)

def generate_production(api_key, style, ratio, era, story):
    try:
        genai.configure(api_key=api_key)
        # نستخدم موديل آمن
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        أنت مخرج سينمائي محترف.
        المهمة: كتابة "ستوري بورد" شامل.
        1. الحقبة: {era} (يجب أن تكون التفاصيل دقيقة تاريخياً).
        2. الشخصيات: استنتج وصفاً ثابتاً للشخصية بناءً على الحقبة والقصة.
        3. قاعدة الأنبياء: توهج ذهبي يخفي الملامح إجبارياً.
        4. الإخراج: جدول (رقم المشهد، وصف المرجع البصري، مطالبة تحريك Veo3).
        5. الأسلوب: {style} | المقاس: {ratio}.
        
        القصة: {story}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"خطأ تقني: {str(e)}"

if st.button("بدء الإنتاج السينمائي"):
    if not api_key:
        st.error("يرجى إدخال مفتاح API في القائمة الجانبية.")
    elif not story or not era:
        st.error("يرجى ملء القصة والفترة الزمنية.")
    else:
        with st.spinner("جاري بناء الاستوديو والإنتاج..."):
            result = generate_production(api_key, style, ratio, era, story)
            st.markdown("### 📋 النتيجة:")
            st.text(result)
