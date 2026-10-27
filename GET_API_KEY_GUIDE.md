# 🔑 How to Get Your Gemini API Key

## ⚠️ IMPORTANT: Your Current Key is INVALID

Your current key in `.env` file:
```
YOUR_OLD_KEY_HERE
```

**This is NOT a Gemini API key!**
- It starts with `AQ.` (OAuth 2.0 token)
- Gemini keys start with `AIzaSy`
- It won't work with the Gemini API

---

## ✅ STEP-BY-STEP GUIDE

### Step 1: Open Google AI Studio

Click this link: **https://aistudio.google.com/app/apikey**

Or copy-paste into your browser:
```
https://aistudio.google.com/app/apikey
```

### Step 2: Sign In

Sign in with your Google account (Gmail).

### Step 3: Create API Key

You'll see a page titled **"Get an API key"**

Click the blue button that says:
```
🔑 Create API key
```

### Step 4: Select Project

You'll see a dropdown with options:
- **"Create API key in new project"** ← CLICK THIS (Recommended)
- Or select an existing Google Cloud project

### Step 5: Copy Your Key

A popup will appear with your new API key.

**The key will look like this:**
```
AIzaSyDaB1CdE2FgH3IjK4LmN5OpQ6RsT7UvW8X
```

**Important characteristics:**
- ✅ Starts with: `AIzaSy`
- ✅ Length: 39 characters
- ✅ No spaces
- ✅ Mix of letters and numbers

**Click the copy button** 📋 to copy it to clipboard.

### Step 6: Update .env File

1. Open the file: `c:\Users\Saurav\Downloads\Foodmind AI .py\.env`

2. Find this line:
```
GEMINI_API_KEY=YOUR_OLD_KEY_HERE
```

3. Replace it with your NEW key (paste from clipboard):
```
GEMINI_API_KEY=AIzaSyDaB1CdE2FgH3IjK4LmN5OpQ6RsT7UvW8X
```

4. **Save the file** (Ctrl+S)

### Step 7: Verify It Works

Run this command in terminal:
```bash
cd "c:\Users\Saurav\Downloads\Foodmind AI .py"
python verify_api_key.py
```

You should see:
```
✅ YOUR API KEY IS VALID AND WORKING!
```

### Step 8: Start the App

```bash
streamlit run app.py
```

Now navigate to the **AI Assistant** page and start chatting!

---

## 🎯 EXAMPLE OF CORRECT VS WRONG

### ❌ WRONG (What you currently have):
```
GEMINI_API_KEY=YOUR_OLD_KEY_HERE
```
- Starts with `AQ.` ← Wrong!
- 53 characters ← Wrong!
- This is an OAuth token, not Gemini key

### ✅ CORRECT (What you need):
```
GEMINI_API_KEY=AIzaSyDaB1CdE2FgH3IjK4LmN5OpQ6RsT7UvW8X
```
- Starts with `AIzaSy` ← Correct!
- 39 characters ← Correct!
- This is a valid Gemini API key

---

## 📸 Visual Guide

When you go to https://aistudio.google.com/app/apikey, you'll see:

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  Google AI Studio                               │
│  ═══════════════                                │
│                                                 │
│  Get an API key                                 │
│                                                 │
│  [🔑 Create API key] ← CLICK THIS BUTTON        │
│                                                 │
│  Your existing API keys:                        │
│  (none yet)                                     │
│                                                 │
└─────────────────────────────────────────────────┘
```

After clicking:

```
┌─────────────────────────────────────────────────┐
│  Create an API key                              │
│                                                 │
│  [▼] Create API key in new project ← SELECT     │
│                                                 │
│      [ Create ]  [ Cancel ]                     │
│                                                 │
└─────────────────────────────────────────────────┘
```

After creating:

```
┌─────────────────────────────────────────────────┐
│  Your API key                                   │
│                                                 │
│  AIzaSyDaB1CdE2FgH3IjK4LmN5OpQ6RsT7UvW8X       │
│                                         📋 Copy │
│                                                 │
│  ⚠️ Keep this key secure and don't share it!   │
│                                                 │
│  [ OK ]                                         │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 🔒 Security Note

**DO NOT SHARE** your API key:
- ❌ Don't post it online
- ❌ Don't commit it to GitHub
- ❌ Don't share it in Discord/Slack
- ✅ Keep it in your local `.env` file only

---

## 🆘 Troubleshooting

### Problem: "I don't see the Create API Key button"

**Solution:** Make sure you're signed into a Google account. Try:
- Signing out and back in
- Using a different browser
- Clearing browser cache

### Problem: "Create API key is grayed out"

**Solution:** You might have billing issues or regional restrictions.
- Check your Google Cloud billing status
- Try using a VPN if in a restricted region
- Contact Google Support

### Problem: "API key created but still doesn't work"

**Solution:** 
1. Make sure you copied the ENTIRE key (39 characters)
2. Check for extra spaces before/after the key in .env
3. Make sure you saved the .env file
4. Restart the Streamlit app

---

## 📞 Still Having Issues?

If you still can't get it working:

1. **Double-check the .env file format:**
   ```
   GEMINI_API_KEY=AIzaSyYOUR_ACTUAL_KEY_HERE
   ```
   - No quotes
   - No spaces around `=`
   - Key starts with `AIzaSy`

2. **Run the verification script:**
   ```bash
   python verify_api_key.py
   ```

3. **Check the output** - it will tell you exactly what's wrong

---

**🎉 Once you have a valid key, the AI Assistant will work perfectly!**
