"""
API Key Verification Script
Tests the current API key and identifies which service it belongs to
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Load .env
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path, override=True)

api_key = os.getenv('GEMINI_API_KEY')

print("="*70)
print("API KEY VERIFICATION")
print("="*70)
print()

if not api_key:
    print("❌ No API key found in .env file")
    exit(1)

print(f"API Key Found: {api_key}")
print(f"Key Length: {len(api_key)} characters")
print(f"Key Prefix: {api_key[:10]}...")
print(f"Key Suffix: ...{api_key[-10:]}")
print()

print("="*70)
print("TESTING WITH GOOGLE GENERATIVE AI")
print("="*70)
print()

try:
    import google.generativeai as genai
    print("✅ google-generativeai library is installed")
    print()
    
    # Try to configure with this key
    print("Testing API key with Google Generative AI...")
    genai.configure(api_key=api_key)
    print("✅ API configured (no immediate error)")
    print()
    
    # Try to list models
    print("Attempting to list available models...")
    try:
        models = list(genai.list_models())
        print(f"✅ SUCCESS! Found {len(models)} models")
        print()
        print("Available models for content generation:")
        for model in models:
            if 'generateContent' in [m.name for m in model.supported_generation_methods]:
                model_name = model.name.replace('models/', '')
                print(f"  ✓ {model_name}")
        print()
        print("="*70)
        print("✅ YOUR API KEY IS VALID AND WORKING!")
        print("="*70)
        
    except Exception as list_error:
        print(f"❌ Failed to list models: {list_error}")
        print()
        
        # Try a direct generation test instead
        print("Trying direct content generation test...")
        try:
            # Try with gemini-pro (most common)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Say 'API key works' if you can read this")
            if response.text:
                print(f"✅ SUCCESS! Model responded: {response.text[:50]}")
                print()
                print("Your API key works with: gemini-pro")
        except Exception as gen_error:
            print(f"❌ Generation test failed: {gen_error}")
            print()
            print("This API key does NOT work with Gemini API")
            
except ImportError:
    print("❌ google-generativeai library not installed")
    print("Run: pip install google-generativeai")
except Exception as e:
    print(f"❌ Error: {e}")

print()
print("="*70)
print("API KEY FORMAT ANALYSIS")
print("="*70)

if api_key.startswith('AIzaSy'):
    print("✅ Format: Standard Gemini API key (AIzaSy...)")
    print("   This is the CORRECT format for Gemini")
elif api_key.startswith('AQ.'):
    print("❌ Format: Looks like OAuth 2.0 access token (AQ...)")
    print("   This is NOT compatible with Gemini API")
    print()
    print("   📝 You need a different type of key:")
    print("   1. Go to: https://aistudio.google.com/app/apikey")
    print("   2. Click 'Create API Key'")
    print("   3. The key should start with 'AIzaSy'")
    print("   4. Copy and paste it into .env file")
else:
    print(f"⚠️  Unknown format (starts with: {api_key[:10]}...)")
    print("   Standard Gemini keys start with 'AIzaSy'")

print()
