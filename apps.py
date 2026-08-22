import os
import gradio as gr
import google.generativeai as genai
from PIL import Image

# আপনার API Key এখানে বসান
GEMINI_API_KEY = "AQ.Ab8RN6JUjb58V1aCnKQdq3T7J1P3qH51Lvt3dl46U0cyGoSabQ" 
genai.configure(api_key=GEMINI_API_KEY)

# Gemini Model সেটআপ
model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_plant_health(image):
    if image is None:
        return "অনুগ্রহ করে একটি ছবি আপলোড করুন।"
    
    pil_img = Image.fromarray(image)
    
    prompt = """
    তুমি একজন অভিজ্ঞ কৃষি বিশেষজ্ঞ। ছবিটি ভালোভাবে বিশ্লেষণ করে নিচের পয়েন্টগুলোতে স্পষ্ট বাংলা ভাষায় উত্তর দাও:
    ১. ফসল/গাছের অবস্থা
    ২. সমস্যার নাম (যদি থাকে)
    ৩. লক্ষণ
    ৪. কৃষকের জন্য সহজ সমাধান ও সার/কীটনাশকের নিয়ম
    ৫. প্রতিরোধমূলক পরামর্শ
    """
    
    try:
        response = model.generate_content([prompt, pil_img])
        return response.text
    except Exception as e:
        return f"সমস্যা হয়েছে: {str(e)}"

interface = gr.Interface(
    fn=analyze_plant_health,
    inputs=gr.Image(label="ফসল, পাতা বা ফলের ছবি দিন"),
    outputs=gr.Markdown(label="কৃষি ডাক্তারের পরামর্শ ও সমাধান"),
    title="🌾 কৃষক সহকারী"
)

port = int(os.environ.get("PORT", 7860))
interface.launch(server_name="0.0.0.0", server_port=port)
