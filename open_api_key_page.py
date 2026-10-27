"""
Opens Google AI Studio API Key page in your default browser
"""

import webbrowser

url = "https://aistudio.google.com/app/apikey"

print("="*70)
print("Opening Google AI Studio in your browser...")
print("="*70)
print()
print(f"URL: {url}")
print()
print("Follow these steps:")
print("1. Sign in with your Google account")
print("2. Click 'Create API Key'")
print("3. Select 'Create API key in new project'")
print("4. Copy the key (it will start with AIzaSy)")
print("5. Update your .env file with the key")
print()
print("="*70)

# Open browser
webbrowser.open(url)

print("✅ Browser opened!")
print()
input("Press Enter to close this window...")
