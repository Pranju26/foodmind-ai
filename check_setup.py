"""Simple setup checker"""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

print("Python version:", sys.version)
print("\nInstalled packages:")

try:
    import streamlit
    print(f"✅ streamlit {streamlit.__version__}")
except:
    print("❌ streamlit not found")

try:
    import dotenv
    print(f"✅ python-dotenv installed")
except:
    print("❌ python-dotenv not found")

try:
    import google.generativeai as genai
    print(f"✅ google-generativeai installed")
except:
    print("❌ google-generativeai not found")

print("\n" + "="*60)
print("Checking .env file...")

import os
env_file = ".env"
if os.path.exists(env_file):
    print(f"✅ {env_file} exists")
    with open(env_file, 'r') as f:
        for line in f:
            if 'GEMINI_API_KEY' in line and not line.strip().startswith('#'):
                parts = line.split('=', 1)
                if len(parts) == 2:
                    key = parts[1].strip().strip("'\"")
                    if key == 'your_gemini_api_key_here':
                        print("⚠️  API key is set to placeholder value")
                    elif len(key) >= 15:
                        print(f"✅ API key found (format: {key[:7]}...)")
                        try:
                            genai.configure(api_key=key)
                            m = genai.GenerativeModel('gemini-3.5-flash-lite')
                            res = m.generate_content('ping', request_options={'timeout': 10})
                            print("✅ Gemini API connection verified successfully!")
                        except Exception as e:
                            print(f"⚠️ API test note: {str(e)[:120]}")
                    else:
                        print(f"❌ INVALID: API key is too short")
else:
    print(f"❌ {env_file} not found")

print("="*60)
