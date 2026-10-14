import streamlit as st
from PIL import Image
from google import genai

st.set_page_config(page_title="MCQ Generator", page_icon="📚")
st.title("📚 বইয়ের পাতা থেকে MCQ জেনারেটর")

api_key = st.sidebar.text_input("Gemini API Key দিন", type="password")

if not api_key:
    st.info("👈 কাজ শুরু করতে বামপাশের সাইডবারে আপনার Gemini API Key টি বসান।")
    st.stop()

client = genai.Client(api_key=api_key)

uploaded_file = st.file_uploader("বইয়ের পাতার ছবি আপলোড করুন", type=["jpg", "jpeg", "png"])
num_q = st.slider("কয়টি প্রশ্ন চান?", 1, 15, 5)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='আপলোড করা পাতা', use_container_width=True)
    
    if st.button("🔥 MCQ তৈরি করুন"):
        with st.spinner('এআই প্রশ্ন তৈরি করছে...'):
            try:
                prompt = f"""
                এই বইয়ের পৃষ্ঠাটি মনোযোগ দিয়ে পড়ো। এর বিষয়বস্তুর ওপর ভিত্তি করে {num_q} টি মানসম্মত MCQ তৈরি করো।
                ফরম্যাট:
                ১. প্রশ্ন
                ২. ৪টি অপশন (ক, খ, গ, ঘ)
                ৩. **সঠিক উত্তর:** 
                ৪. **ব্যাখ্যা:** (সংক্ষিপ্ত)
                """
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[image, prompt]
                )
                st.success("সম্পন্ন হয়েছে!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"সমস্যা হয়েছে: {e}")
