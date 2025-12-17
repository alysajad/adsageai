
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key present: {bool(api_key)}")

if api_key:
    genai.configure(api_key=api_key)

try:
    print("Attempting to list models...")
    for m in genai.list_models():
        if 'generateImages' in m.supported_generation_methods:
            print(f"Found Image Model: {m.name}")

    print("\nAttempting generation with 'imagen-3.0-generate-001'...")
    model = genai.ImageGenerationModel("imagen-3.0-generate-001")
    response = model.generate_images(
        prompt="A futuristic banana wearing sunglasses",
        number_of_images=1,
    )
    print("✅ Success!")
    response.images[0].show()
except Exception as e:
    print(f"❌ Error during generation: {e}")
