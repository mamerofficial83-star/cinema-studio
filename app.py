import streamlit as st
import google.generativeai as genai

# إعداد واجهة البرنامج
st.set_page_config(page_title="Cinematic Pro Studio", layout="centered")
st.title("🎬 محرك الإنتاج السينمائي الاحترافي")

# إدخال المفتاح
api_key = st.sidebar.text_input("أدخل مفتاح API (من Google AI Studio):", type="password")

# خيارات المستخدم
style = st.selectbox("الأسلوب السينمائي:", ["واقعي", "أنيمي", "دراما تاريخية"])
ratio = st.selectbox("مقاس الكادر:", ["16:9", "2.35:1", "9:16"])
story = st.text_area("ضع القصة هنا (سطر لكل مشهد):", height=200)

def generate_scenes(story_text, style_val, ratio_val, key):
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        prompt = f"""
        أنت مدير إنتاج سينمائي خبير. قم بتنفيذ التالي:
        1. قسّم القصة المرفقة إلى وحدات من 9 سطور (مشاهد).
        2. لكل مشهد: اكتب (مطالبة صورة مرجعية) + (مطالبة Veo3 للتحريك).
        3. التعليمات الإجبارية:
           - لا موسيقى، لا حوارات، فقط مؤثرات بيئية.
           - ثبات تام للشخصيات وزوايا كاميرا متنوعة.
           - زمن التحريك: 8 ثوانٍ بدقة واقعية.
           - اللغة: عربية فقط للمطالبة.
        القصة: {story_text}
        الأسلوب: {style_val}
        المقاس: {ratio_val}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"حدث خطأ أثناء الإنتاج: {e}"

if st.button("بدء الإنتاج"):
    if not api_key:
        st.error("يرجى إدخال مفتاح API في الشريط الجانبي أولاً.")
    elif not story:
        st.warning("يرجى كتابة القصة.")
    else:
        with st.spinner("جاري التوليد..."):
            result = generate_scenes(story, style, ratio, api_key)
            st.markdown("### 📋 النتائج:")
            st.write(result)
        st.markdown("### 📋 نتائج الإنتاج:")
        st.write(result)
