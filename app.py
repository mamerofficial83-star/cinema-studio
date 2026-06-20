import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cinematic Studio Pro", layout="wide")
st.title("🎬 محرك الإنتاج السينمائي المتكامل")

# إعدادات المستخدم الجانبية
api_key = st.sidebar.text_input("أدخل مفتاح API:", type="password")

# المدخلات الأساسية
col1, col2, col3 = st.columns(3)
with col1:
    style = st.selectbox("الأسلوب:", ["واقعي", "أنيمي", "دراما تاريخية", "سينمائي كلاسيكي"])
with col2:
    ratio = st.selectbox("مقاس الفيديو:", ["16:9", "2.35:1", "9:16"])
with col3:
    era = st.text_input("الفترة الزمنية:", placeholder="مثلاً: العصر العباسي")

story = st.text_area("القصة:", height=150)

# دوال العمل
def get_model(key):
    genai.configure(api_key=key)
    for model_name in ["gemini-1.5-flash", "gemini-1.0-pro"]:
        try: return genai.GenerativeModel(model_name)
        except: continue
    return None

# التحكم بالمراحل
if 'step' not in st.session_state: st.session_state.step = 1

if st.button("المرحلة 1: تحليل القصة واقتراح الهوية"):
    model = get_model(api_key)
    if model:
        prompt = f"بناءً على الفترة الزمنية '{era}' والقصة '{story}'، اقترح وصفاً دقيقاً للشخصية (ملابس، ملامح) لنستخدمه كمرجع ثابت."
        st.session_state.proposed_identity = model.generate_content(prompt).text
        st.session_state.step = 2

if st.session_state.step >= 2:
    st.session_state.final_identity = st.text_area("تعديل الهوية (المرجع الثابت):", value=st.session_state.get('proposed_identity', ''), height=150)
    if st.button("المرحلة 2: اعتماد الهوية وتوليد الستوري بورد"):
        st.session_state.step = 3

if st.session_state.step == 3:
    st.write("---")
    st.subheader("نتائج الإنتاج النهائي")
    model = get_model(api_key)
    full_prompt = f"""
    أنت مدير إنتاج. استخرج ستوري بورد من القصة: {story}
    الهوية البصرية الثابتة: {st.session_state.final_identity}
    الأسلوب: {style} | المقاس: {ratio} | الحقبة: {era}
    قاعدة الأنبياء: توهج ذهبي يخفي الملامح.
    الجدول: (رقم المشهد، وصف المرجع البصري، مطالبة تحريك Veo3).
    """
    st.text(model.generate_content(full_prompt).text)
