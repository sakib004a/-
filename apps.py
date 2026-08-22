import os
import google.generativeai as genai
import gradio as gr
from PIL import Image

# আপনার পাওয়া AQ... শুরু হওয়া API Key
GEMINI_API_KEY = "AQ.Ab8RN6IR5nAr9U6qjBbeQvbXBp5Ikgpyx-_Uz4ThXZyJpO2izg"

# পুরোনো পদ্ধতিতে অথেন্টিকেশন সেটআপ
genai.configure(api_key=GEMINI_API_KEY)

def analyze_plant_health(image):
    if image is None:
        return "অনুগ্রহ করে একটি ছবি আপলোড করুন।"
    
    pil_img = Image.fromarray(image)
    
    prompt = """
    তুমি একজন অভিজ্ঞ কৃষি বিশেষজ্ঞ। ছবিটি ভালোভাবে বিশ্লেষণ করে নিচের পয়েন্টগুলোতে স্পষ্ট বাংলা ভাষায় উত্তর দাও:

    ১. **ফসল/গাছের অবস্থা:** গাছ, ফুল, পাতা বা ফলটি সুস্থ নাকি কোনো সমস্যা রয়েছে?
    ২. **সমস্যার নাম (যদি থাকে):** রোগ, পোকার আক্রমণ নাকি পুষ্টির ঘাটতি? (বাংলা ও ইংরেজি)
    ৩. **লক্ষণ:** ছবিতে কী কী অস্বাভাবিকতা দেখা যাচ্ছে?
    ৪. **কৃষকের জন্য সমাধান:** ঘরোয়া বা প্রাকৃতিক প্রতিকার এবং প্রয়োজনীয় সার/কীটনাশকের নাম।
    ৫. **প্রতিরোধমূলক পরামর্শ:** ভবিষ্যতে এড়াতে করণীয়।
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([prompt, pil_img])
        return response.text
    except Exception as e:
        return f"সমস্যা হয়েছে: {str(e)}"

demo = gr.Interface(
    fn=analyze_plant_health,
    inputs=gr.Image(label="ফসল, পাতা বা ফলের ছবি দিন"),
    outputs=gr.Markdown(label="কৃষি ডাক্তারের পরামর্শ ও সমাধান"),
    title="🌾 কৃষক সহকারী - ফসল ও গাছের রোগ নির্ণয় এআই",
    description="আক্রান্ত পাতা, ফুল বা ফলের ছবি আপলোড করুন। এআই সাথে সাথেই রোগের কারণ ও সমাধান জানিয়ে দেবে।"
)

app = demo.launch()
