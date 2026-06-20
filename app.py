import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cinematic Studio: Development Phase", layout="wide")
st.title("🎬 محرك الإنتاج: مرحلة تطوير الهوية البصرية")

api_key = st.sidebar.text_input("أدخل مفتاح API:", type="password")

# بيانات المرحلة الأولى
era = st.selectbox("الفترة الزمنية:", ["زمن النبوة", "العصر الأموي", "العصر العباسي", "العصر الأندلسي"])
story = st.text_area("أدخل قصة المشهد (ليستخرج منها الشخصيات):", height=150)

# حالة تخزين الشخصيات بعد التعديل
if 'final_identity' not in st.session_state:
    st.session_state.final_identity = None

# المرحلة 1: اقتراح الهوية
def suggest_identity(era, story, key):
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-pro')
    prompt = f"حلل القصة التالية ووقوعها في {era}. اقترح وصفاً دقيقاً ومفصلاً للشخصية الرئيسية (ملابس، ملامح، أسلوب) ليكون مرجعاً بصرياً. القصة: {story}"
    return model.generate_content(prompt).text

if st.button("اقتراح هوية الشخصيات"):
    st.session_state.proposed_identity = suggest_identity(era, story, api_key)

if 'proposed_identity' in st.session_state:
    st.info("إليك الهوية المقترحة. يمكنك تعديلها قبل الاعتماد:")
    st.session_state.final_identity = st.text_area("تعديل الهوية البصرية:", value=st.session_state.proposed_identity, height=150)
    
    if st.button("اعتماد الهوية والبدء في وضع خطة العمل"):
        st.success("تم اعتماد الهوية! الآن سيتم دمجها في كل المشاهد.")
        # هنا سنبدأ توليد الستوري بورد بناء على st.session_state.final_identity
        st.write("---")
        st.subheader("خطة العمل التنفيذية (الستوري بورد)")
        # استدعاء دالة توليد المشاهد بناء على الهوية المعتمدة (سيتم برمجتها هنا)
