import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cinema Director AI", layout="wide")
st.title("🎬 استوديو الإنتاج السينمائي")

api_key = st.sidebar.text_input("أدخل مفتاح API:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # البحث عن الموديلات المتاحة في حسابك
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if not available_models:
            st.error("لم يتم العثور على أي موديلات متاحة في مفتاحك. تأكد من تفعيل Google Generative AI API في Google Cloud.")
        else:
            # نختار أول موديل متاح مهما كان اسمه
            selected_model = available_models[0]
            st.write(f"تم العثور على موديل متاح: {selected_model}")
            
            # باقي الإعدادات
            style = st.selectbox("الأسلوب:", ["واقعي", "أنيمي", "دراما تاريخية"])
            ratio = st.selectbox("مقاس الكادر:", ["16:9", "2.35:1", "9:16"])
            era = st.text_input("الفترة الزمنية:")
            story = st.text_area("القصة:")

            if st.button("بدء الإنتاج"):
                model = genai.GenerativeModel(selected_model)
                prompt = f"المهمة: كتابة ستوري بورد. الحقبة: {era}. الأسلوب: {style}. القصة: {story}. قاعدة الأنبياء: توهج ذهبي."
                response = model.generate_content(prompt)
                st.text(response.text)
    except Exception as e:
        st.error(f"خطأ في الاتصال: {str(e)}")
else:
    st.info("الرجاء إدخال مفتاح API في القائمة الجانبية.")
