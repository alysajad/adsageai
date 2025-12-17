
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")



# Using the discovered model: imagen-4.0-fast-generate-001
url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict?key={API_KEY}"
# Note: Trying 3.0 first as per docs often being 3.0, but if 4.0 showed up we use that path? 
# Actually let's try 3.0 per previous 404, wait, 404 meant invalid model. 
# The list showed 'models/imagen-4.0-fast-generate-001'.
url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-fast-generate-001:predict?key={API_KEY}"

print(f"Testing API: {url.split('?')[0]}")

headers = {
    "Content-Type": "application/json"
}

# The 'predict' method typically takes 'instances'
data = {
    "instances": [
        {
            "prompt": "A beautiful cinematic shot of a futuristic banana, 8k resolution, photorealistic"
        }
    ],
    "parameters": {
        "sampleCount": 1,
        "aspectRatio": "1:1"
    }
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Success!")
        result = response.json()
        print("Keys:", result.keys())
        predictions = result.get('predictions', [])
        if predictions:
            # Usually prediction contains bytesBase64Encoded or similar
            print(f"Received {len(predictions)} predictions.")
            print(f"Prediction keys: {predictions[0].keys()}")
            
    else:
        print(f"❌ Error: {response.text}")
except Exception as e:
    print(e)
