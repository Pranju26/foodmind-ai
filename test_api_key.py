"""
FoodMind AI - API Key Diagnostic Tool
Run this script to check your Gemini API configuration
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

print("=" * 60)
print("🔍 FoodMind AI - API Key Diagnostic Tool")
print("=" * 60)
print()

# Load environment variables
env_path = Path(__file__).parent / '.env'
print(f"📁 Looking for .env file at: {env_path}")

if not env_path.exists():
    print("❌ ERROR: .env file not found!")
    print(f"   Expected location: {env_path}")
    print("\n   Please create a .env file with your API key.")
    exit(1)

print("✅ .env file found")
print()

# Load environment
load_dotenv(env_path, override=True)

# Check API key
api_key = os.getenv('GEMINI_API_KEY')

print("🔑 API Key Analysis:")
print("-" * 60)

if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file")
    print("\n   Make sure your .env file contains:")
    print("   GEMINI_API_KEY=your_actual_key_here")
    exit(1)

if api_key == 'your_gemini_api_key_here':
    print("❌ ERROR: API key not configured")
    print("   The default placeholder value is still present.")
    print("\n   You need to replace it with a real API key from:")
    print("   https://aistudio.google.com/app/apikey")
    exit(1)

print(f"✅ API key found in environment")
print(f"   Length: {len(api_key)} characters")
print(f"   Starts with: {api_key[:10]}...")
print(f"   Ends with: ...{api_key[-5:]}")
print()

# Validate format
print("📋 Format Validation:")
print("-" * 60)

if api_key.startswith('AQ.'):
    print("✅ Key format: Google AI Studio Auth Key (AQ.*)")
elif api_key.startswith('AIzaSy'):
    print("✅ Key format: Google Standard API Key (AIzaSy*)")
else:
    print(f"ℹ️  Key format prefix: {api_key[:7]}...")

if len(api_key) < 15:
    print(f"❌ ERROR: Key is too short ({len(api_key)} chars)")
    exit(1)
else:
    print(f"✅ Key length: {len(api_key)} characters")

print()

# Test API connection
print("🌐 Testing API Connection:")
print("-" * 60)

try:
    import google.generativeai as genai
    print("✅ google-generativeai library is installed")
except ImportError:
    print("❌ ERROR: google-generativeai not installed")
    print("\n   Run: pip install google-generativeai")
    exit(1)

print("🔄 Configuring API...")
try:
    genai.configure(api_key=api_key)
    print("✅ API configured successfully")
except Exception as e:
    print(f"❌ Configuration failed: {e}")
    exit(1)

print("🔄 Testing model access...")
try:
    models = list(genai.list_models())
    print(f"✅ Successfully connected to Gemini API!")
    print(f"   Found {len(models)} available models")
    
    # Show compatible models
    print("\n📦 Available Models for Content Generation:")
    for model in models:
        methods = [m if isinstance(m, str) else getattr(m, 'name', str(m)) for m in model.supported_generation_methods]
        if 'generateContent' in methods:
            model_name = model.name.replace('models/', '')
            print(f"   ✓ {model_name}")
    
except Exception as e:
    error_str = str(e)
    print(f"❌ API Connection Failed!")
    print(f"   Error: {error_str}")
    print()
    
    # Provide specific guidance based on error
    if "API_KEY_INVALID" in error_str or "invalid" in error_str.lower():
        print("   🔍 Diagnosis: Your API key is invalid or revoked")
        print()
        print("   📝 Solution:")
        print("   1. Go to: https://aistudio.google.com/app/apikey")
        print("   2. Check if your key is still active")
        print("   3. Create a NEW API key")
        print("   4. Update your .env file")
        print("   5. Run this test again")
    
    elif "403" in error_str or "permission" in error_str.lower():
        print("   🔍 Diagnosis: Permission denied")
        print()
        print("   📝 Solution:")
        print("   1. Your API key may not have access to Gemini models")
        print("   2. Create a new key at: https://aistudio.google.com/app/apikey")
        print("   3. Make sure to select proper permissions")
    
    elif "404" in error_str:
        print("   🔍 Diagnosis: Service not found")
        print("   This might be a temporary issue or regional restriction")
    
    elif "quota" in error_str.lower() or "limit" in error_str.lower():
        print("   🔍 Diagnosis: API quota exceeded")
        print("   You've reached your free tier limit")
        print("   Wait 24 hours or upgrade your plan")
    
    else:
        print("   🔍 Check your internet connection")
        print("   🔍 Verify the API key is correctly copied")
    
    exit(1)

print()
print("=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print()
print("🎉 Your Gemini API is configured correctly!")
print()
print("You can now use the AI Assistant in FoodMind AI.")
print("Start the app with: streamlit run app.py")
print()
