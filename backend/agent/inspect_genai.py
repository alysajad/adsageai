
import google.generativeai as genai
print(dir(genai))
try:
    print(f"genai.ImageGenerationModel: {genai.ImageGenerationModel}")
except AttributeError:
    print("genai.ImageGenerationModel NOT FOUND")
