
import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"CWD: {os.getcwd()}")
print("sys.path:")
for p in sys.path:
    print(f"  {p}")

try:
    import google
    print(f"✅ Imported google from: {google.__file__}")
    print(f"google.__path__: {google.__path__}")
except ImportError as e:
    print(f"❌ Failed to import google: {e}")

try:
    import google.generativeai
    print(f"✅ Imported google.generativeai from: {google.generativeai.__file__}")
except ImportError as e:
    print(f"❌ Failed to import google.generativeai: {e}")

try:
    import pkg_resources
    ver = pkg_resources.get_distribution("google-generativeai").version
    print(f"📦 Installed google-generativeai version: {ver}")
except Exception as e:
    print(f"❌ Failed to check version via pkg_resources: {e}")
