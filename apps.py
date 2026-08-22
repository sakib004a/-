import os
import gradio as gr
from google.genai import client
from PIL import Image

# পরিবেশ বা এনভায়রনমেন্ট ভ্যারিয়েবল থেকে API Key নেওয়া
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

ai = client.Client(api_key=GEMINI_API_KEY)

def analyze_plant_health(image):
    if image is None:
        return "অনুগ্রহ করে একটি ছবি আপলোড করুন।"
    
    try:
        pil_img = Image.fromarray(image)
        
        prompt = """
        তুমি একজন অভিজ্ঞ কৃষি বিশেষজ্ঞ। ছবিটি ভালোভাবে বিশ্লেষণ করে নিচের পয়েন্টগুলোতে স্পষ্ট বাংলা ভাষায় উত্তর দাও:

        ১. **ফসল/গাছের অবস্থা:** গাছ, ফুল, পাতা বা ফলটি সুস্থ নাকি কোনো সমস্যা রয়েছে?
        ২. **সমস্যার নাম (যদি থাকে):** রোগ, পোকার আক্রমণ নাকি পুষ্টির ঘাটতি? (নামটি বাংলা ও ইংরেজিতে বলো)
        ৩. **লক্ষণ:** ছবিতে কী কী অস্বাভাবিকতা দেখা যাচ্ছে?
        ৪. **কৃষকের জন্য সমাধান:** 
           - ঘরোয়া বা প্রাকৃতিক প্রতিকার
           - প্রয়োজনীয় জৈব/রাসায়নিক সার বা কীটনাশকের নাম ও স্প্রে করার পদ্ধতি
        ৫. **প্রতিরোধমূলক পরামর্শ:** ভবিষ্যতে এই সমস্যা এড়াতে করণীয়।

        যদি ছবিটি একদম সুস্থ গাছের হয়, তবে কৃষককে জানিয়ে দাও যে গাছটি ভালো আছে এবং সাধারণ পরিচর্যার পরামর্শ দাও।
        """
        
        response = ai.models.generate_content(
            model='gemini-2.5-flash',
            contents=[pil_img, prompt]
        )
        return response.text
    except Exception as e:
        return f"সমস্যা হয়েছে: {str(e)}"

# Gradio Interface UI
with gr.Blocks(title="🌾 কৃষক সহকারী") as demo:
    gr.Markdown("# 🌾 কৃষক সহকারী - ফসল ও গাছের রোগ নির্ণয় এআই")
    gr.Markdown("আক্রান্ত পাতা, ফুল বা ফলের ছবি আপলোড করে 'রোগ নির্ণয় করুন' বাটনে ক্লিক করুন।")
    
    with gr.Row():
        with gr.Column():
            img_input = gr.Image(label="ফসল বা গাছের ছবি দিন (ক্যামেরা বা গ্যালারি)")
            submit_btn = gr.Button("🔍 রোগ নির্ণয় করুন", variant="primary")
        with gr.Column():
            output_text = gr.Markdown(label="কৃষি ডাক্তারের পরামর্শ ও সমাধান")
            
    submit_btn.click(fn=analyze_plant_health, inputs=img_input, outputs=output_text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
