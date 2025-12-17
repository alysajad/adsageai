
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_image(prompt):
    """
    Generates an image using the 'Nano Banana' (Pollinations) model.
    """
    try:
        print(f"🎨 Generating image for prompt: {prompt}")
        
        # Using Imagen 4.0 Fast via Direct API (since SDK had issues)
        import requests
        import base64
        from io import BytesIO
        from PIL import Image
        import os

        # Hardcoded URL for the discovered working model
        api_key = os.getenv("GEMINI_API_KEY")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-fast-generate-001:predict?key={api_key}"
        
        headers = { "Content-Type": "application/json" }
        data = {
            "instances": [
                { "prompt": prompt }
            ],
            "parameters": {
                "sampleCount": 1,
                "aspectRatio": "1:1"
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            predictions = result.get('predictions', [])
            if predictions and 'bytesBase64Encoded' in predictions[0]:
                image_data = base64.b64decode(predictions[0]['bytesBase64Encoded'])
                return Image.open(BytesIO(image_data))
            elif predictions and 'mimeType' in predictions[0]:
                 # Some versions return just the bytes? Or key name differs
                 print(f"⚠️ Unexpected keys: {predictions[0].keys()}")
                 return None
        else:
             print(f"❌ Imagen API Error: {response.text}")

        # Fallback if Google API fails (for demo continuity)
        print("⚠️ Falling back to Pollinations...")
        encoded_prompt = requests.utils.quote(prompt)
        url_poly = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=true"
        response_poly = requests.get(url_poly)
        if response_poly.status_code == 200:
             return Image.open(BytesIO(response_poly.content))
             
        return None

    except Exception as e:
        print(f"❌ Image Generation Error: {e}")
        return None
