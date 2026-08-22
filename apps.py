import os
import io
import base64
import gradio as gr
from groq import Groq
from PIL import Image

GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

def analyze_plant_health(image):
    if image is None:
        return "অনুগ্রহ করে একটি ছবি আপলোড করুন।"
    
    try:
        pil_img = Image.fromarray(image)
        buffered = io.BytesIO()
        pil_img.save(buffered, format="JPEG")
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        prompt = """
        তুমি একজন অভিজ্ঞ কৃষি বিশেষজ্ঞ। ছবিটি ভালোভাবে বিশ্লেষণ করে নিচের পয়েন্টগুলোতে স্পষ্ট বাংলা ভাষায় উত্তর দাও:

        ১. **ফসল/গাছের অবস্থা:** গাছ, ফুল, পাতা বা ফলটি সুস্থ নাকি কোনো সমস্যা রয়েছে?
        ২. **সমস্যার নাম (যদি থাকে):** রোগ, পোকার আক্রমণ নাকি পুষ্টির ঘাটতি? (বাংলা ও ইংরেজি)
        ৩. **লক্ষণ:** ছবিতে কী কী অস্বাভাবিকতা দেখা যাচ্ছে?
        ৪. **কৃষকের জন্য সমাধান:** ঘরোয়া বা প্রাকৃতিক প্রতিকার এবং প্রয়োজনীয় সার/কীটনাশকের নাম।
        ৫. **প্রতিরোধমূলক পরামর্শ:** ভবিষ্যতে এড়াতে করণীয়।

        যদি ছবিটি একদম সুস্থ গাছের হয়, তবে কৃষককে জানিয়ে দাও যে গাছটি ভালো আছে।
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model="qwen/qwen3.6-27b",  # Groq-এর বর্তমানে একটিভ ভিশন মডেল
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"সমস্যা হয়েছে: {str(e)}"

demo = gr.Interface(
    fn=analyze_plant_health,
    inputs=gr.Image(label="ফসল, পাতা বা ফলের ছবি দিন"),
    outputs=gr.Markdown(label="কৃষি ডাক্তারের পরামর্শ ও সমাধান"),
    title="🌾 কৃষক সহকারী - ফসল ও গাছের রোগ নির্ণয় এআই",
    description="আক্রান্ত পাতা, ফুল বা ফলের ছবি আপলোড করুন। এআই সাথে সাথেই রোগের কারণ ও সমাধান জানিয়ে দেবে।"
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
