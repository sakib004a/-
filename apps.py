import os
import gradio as gr
from google.genai import client
from PIL import Image

# আপনার API Key
GEMINI_API_KEY = "AQ.Ab8RN6JUjb58V1aCnKQdq3T7J1P3qH51Lvt3dl46U0cyGoSabQ"

ai = client.Client(api_key=GEMINI_API_KEY)

def analyze_plant_health(image):
    if image is None:
        return "অনুগ্রহ করে একটি ছবি আপলোড করুন।"
    
    # NumPy array থেকে PIL Image-এ কনভার্ট
    pil_img = Image.fromarray(image).convert("RGB")
    
    prompt = """
    তুমি একজন অভিজ্ঞ কৃষি বিশেষজ্ঞ। ছবিটি ভালোভাবে বিশ্লেষণ করে নিচের পয়েন্টগুলোতে স্পষ্ট বাংলা ভাষায় উত্তর দাও:

    ১. **ফসল/গাছের অবস্থা:** গাছ, ফুল, পাতা বা ফলটি সুস্থ নাকি কোনো সমস্যা রয়েছে?
    ২. **সমস্যার নাম (যদি থাকে):** রোগ, পোকার আক্রমণ নাকি পুষ্টির ঘাটতি? (বাংলা ও ইংরেজি)
    ৩. **লক্ষণ:** ছবিতে কী কী অস্বাভাবিকতা দেখা যাচ্ছে?
    ৪. **কৃষকের জন্য সমাধান:** ঘরোয়া ও প্রাকৃতিক প্রতিকার, এবং প্রয়োজনীয় সার বা কীটনাশকের নাম।
    ৫. **প্রতিরোধমূলক পরামর্শ:** ভবিষ্যতে এই সমস্যা এড়াতে করণীয়।
    """
    
    try:
        response = ai.models.generate_content(
            model='gemini-2.5-flash',
            contents=[pil_img, prompt]
        )
        return response.text
    except Exception as e:
        return f"সমস্যা হয়েছে: {str(e)}"

# Gradio Interface
demo = gr.Interface(
    fn=analyze_plant_health,
    inputs=gr.Image(label="ফসল, পাতা বা ফলের ছবি দিন"),
    outputs=gr.Markdown(label="কৃষি ডাক্তারের পরামর্শ ও সমাধান"),
    title="🌾 কৃষক সহকারী - ফসল ও গাছের রোগ নির্ণয় এআই"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
