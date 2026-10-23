"""
Test Gemini API Key
This script helps you verify if your Gemini API key is working
"""

import os
from dotenv import load_dotenv

print("=" * 60)
print("🔑 GEMINI API KEY TESTER")
print("=" * 60)
print()

# Load environment variables
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

print("📋 Step 1: Checking .env file...")
if not api_key:
    print("❌ No API key found in .env file")
    print()
    print("🔧 HOW TO FIX:")
    print("1. Create or edit .env file in this folder")
    print("2. Add this line:")
    print("   GEMINI_API_KEY=your_actual_key_here")
    print()
    print("🌐 GET YOUR KEY:")
    print("   https://aistudio.google.com/app/apikey")
    print()
    exit(1)

print(f"✅ API key found in .env file")
print(f"   Length: {len(api_key)} characters")
print(f"   Starts with: {api_key[:7]}...")
print()

# Check key format
print("📋 Step 2: Validating key format...")
if api_key.startswith('AIzaSy'):
    print("✅ Key format looks correct (starts with 'AIzaSy')")
elif api_key.startswith('AQ.'):
    print("❌ INVALID KEY FORMAT!")
    print("   Your key starts with 'AQ.' but should start with 'AIzaSy'")
    print()
    print("🔧 HOW TO FIX:")
    print("1. Go to: https://aistudio.google.com/app/apikey")
    print("2. Create a NEW API key")
    print("3. Copy the new key (should start with 'AIzaSy')")
    print("4. Update your .env file with the new key")
    print()
    exit(1)
else:
    print("⚠️  Key format unusual (should start with 'AIzaSy')")
print()

# Try to import the library
print("📋 Step 3: Checking if library is installed...")
try:
    import google.generativeai as genai
    print("✅ google.generativeai library is installed")
except ImportError:
    print("❌ google.generativeai library NOT installed")
    print()
    print("🔧 HOW TO FIX:")
    print("   Run this command:")
    print("   pip install google-generativeai")
    print()
    exit(1)
print()

# Configure and test the API
print("📋 Step 4: Testing API connection...")
try:
    genai.configure(api_key=api_key)
    
    # Try to list models
    print("   Fetching available models...")
    models = list(genai.list_models())
    
    if models:
        print(f"✅ API key is VALID and WORKING!")
        print(f"   Found {len(models)} available models:")
        for model in models[:5]:  # Show first 5 models
            print(f"   - {model.name}")
        if len(models) > 5:
            print(f"   ... and {len(models) - 5} more")
    else:
        print("⚠️  API connected but no models available")
        
except Exception as e:
    error_msg = str(e)
    print(f"❌ API KEY ERROR!")
    print(f"   Error: {error_msg}")
    print()
    
    if "API_KEY_INVALID" in error_msg or "invalid" in error_msg.lower():
        print("🔧 YOUR API KEY IS INVALID")
        print()
        print("HOW TO FIX:")
        print("1. Go to: https://aistudio.google.com/app/apikey")
        print("2. Check if your key is listed and active")
        print("3. If not, create a NEW key")
        print("4. Update your .env file with the new key")
        print("5. Run this test again")
    elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
        print("🔧 QUOTA EXCEEDED")
        print("   You've used up your free tier limit")
        print("   Wait 24 hours or upgrade to paid tier")
    else:
        print("🔧 UNKNOWN ERROR")
        print("   Check your internet connection")
        print("   Verify key at: https://aistudio.google.com/app/apikey")
    print()
    exit(1)

print()

# Try a test generation
print("📋 Step 5: Testing text generation...")
try:
    # Find a suitable model
    suitable_model = None
    for model in genai.list_models():
        if 'generateContent' in [m.name for m in model.supported_generation_methods]:
            if 'gemini-pro' in model.name or 'gemini-1.5' in model.name:
                suitable_model = model.name.replace('models/', '')
                break
    
    if not suitable_model:
        suitable_model = 'gemini-pro'
    
    print(f"   Using model: {suitable_model}")
    model = genai.GenerativeModel(suitable_model)
    
    response = model.generate_content("Say 'Hello, FoodMind AI is working!' in one sentence")
    
    if response and response.text:
        print("✅ Text generation WORKING!")
        print(f"   Response: {response.text[:100]}...")
    else:
        print("⚠️  Generation returned empty response")
        
except Exception as e:
    print(f"❌ Generation test failed: {e}")
    print()
    exit(1)

print()
print("=" * 60)
print("🎉 SUCCESS! YOUR API KEY IS FULLY WORKING!")
print("=" * 60)
print()
print("✅ Your Gemini API key is valid and working correctly")
print("✅ FoodMind AI Assistant should now work")
print()
print("📱 NEXT STEPS:")
print("1. Make sure your app is running: streamlit run app.py")
print("2. Open: http://localhost:8501")
print("3. Login: PranjaliGadekar / Pranjali@123")
print("4. Go to: 🤖 AI Assistant")
print("5. Ask: 'I want to gain weight, give me suggestions'")
print()
print("🎯 If AI Assistant still doesn't work:")
print("   - Restart the app (Ctrl+C, then streamlit run app.py)")
print("   - Clear browser cache (Ctrl+Shift+Delete)")
print("   - Try incognito/private window")
print()
