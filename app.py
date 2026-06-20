import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cinematic Identity Engine", layout="wide")
st.title("🎬 محرك الإنتاج بالهوية البصرية الثابتة")

# الشريط الجانبي
api_key = st.sidebar.text_input("أدخل مفتاح API:", type="password")

# إعدادات الهوية الثابتة
st.subheader("إعدادات الهوية الثابتة")
identity_desc = st.text_area("أدخل الوصف الدقيق للشخصية (سيتكرر في كل المشاهد):", 
                             placeholder="مثال: رجل نحيل، لحية خفيفة سوداء، يرتدي ثوباً قطنياً طويلاً باللون البيج...")
era = st.selectbox("الفترة الزمنية:", ["زمن النبوة", "العصر الأموي", "العصر العباسي"])

# القصة
story = st.text_area("القصة (اكتب الأحداث):", height=200)

def generate_fixed_identity_board(identity, era, story, key):
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt = f"""
    أنت مخرج سينمائي. مهمتك إنتاج ستوري بورد يعتمد على هوية بصرية ثابتة.
    
    الهوية الثابتة التي يجب دمجها في كل مشهد: {identity}
    الفترة الزمنية: {era}
    
    البروتوكول الإجباري:
    1. في كل مطالبة (سواء للصورة أو للتحريك)، ابدأ بـ: "Fixed Character Identity: {identity}, Context: {era}..."
    2. قاعدة الأنبياء: إذا ظهر نبي، استبدل الوصف بـ: "Golden Glow Effect concealing all facial features, figure in historical attire of {era}".
    3. المخرجات: جدول من (رقم المشهد، مطالبة توليد الصورة، مطالبة تحريك Veo3).
    4. التعليمات: لا موسيقى، لا حوار، تحريك احترافي 8 ثوانٍ، واقعي.
    
    القصة: {story}
    """
    return model.generate_content(prompt).text

if st.button("بدء الإنتاج بالهوية الثابتة"):
    if api_key and identity_desc and story:
        with st.spinner("جاري دمج الهوية في المشاهد..."):
            board = generate_fixed_identity_board(identity_desc, era, story, api_key)
            st.markdown("### 📋 الستوري بورد المعتمد:")
            st.text(board)
    else:
        st.error("يرجى إدخال المفتاح ووصف الشخصية والقصة.")
