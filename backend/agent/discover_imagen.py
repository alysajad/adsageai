
import google.generativeai as genai
import sys

print(f"GenAI Version: {genai.__version__}")

print("\n--- Trying Direct Import ---")
try:
    from google.generativeai import ImageGenerationModel
    print("✅ Found ImageGenerationModel in top level")
except ImportError:
    print("❌ Not in top level")

print("\n--- Trying Submodule Import ---")
try:
    from google.generativeai import imagen
    print("✅ Found 'imagen' submodule")
    print(dir(imagen))
except ImportError:
    print("❌ 'imagen' submodule not found")

try:
    import google.generativeai.types as types
    print("\n--- Inspecting types ---")
    if 'ImageGenerationModel' in dir(types):
        print("✅ Found ImageGenerationModel in types")
    else:
        print("❌ Not in types")
except ImportError:
    print("❌ types submodule not found")
