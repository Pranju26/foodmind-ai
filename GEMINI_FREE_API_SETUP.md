# 🚀 Gemini Free API Setup Guide for FoodMind AI

This guide will help you set up the **FREE** Gemini API to enable AI features in FoodMind AI.

---

## ✅ What You Get with Free Tier

- **No credit card required**
- **15 requests per minute**
- **1,500 requests per day**
- **1 million tokens per month**
- Access to models:
  - `gemini-1.5-flash` (fast, optimized for images and text)
  - `gemini-1.5-pro` (limited free usage)

Perfect for FoodMind AI's features:
- 🤖 AI Nutrition Assistant
- 📸 Food Image Analysis

---

## 📋 Step-by-Step Setup (5 minutes)

### Step 1: Get Your Free API Key

1. **Visit Google AI Studio:**
   ```
   https://aistudio.google.com/app/apikey
   ```

2. **Sign in** with your Google account

3. **Click "Create API Key"**
   - Select "Create API key in new project" (recommended for beginners)
   - OR select an existing Google Cloud project

4. **Copy your API key**
   - It will look like: `AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - ✅ Always starts with `AIzaSy`
   - ✅ Exactly 39 characters long

---

### Step 2: Add API Key to FoodMind AI

1. **Open the `.env` file:**
   ```
   Location: c:\Users\Saurav\Downloads\Foodmind AI .py\.env
   ```

2. **Find this line:**
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Replace with your actual key:**
   ```
   GEMINI_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

4. **Save the file** (Ctrl + S)

---

### Step 3: Restart the App

1. **Stop the app** if it's running (Ctrl + C in terminal)

2. **Start it again:**
   ```bash
   streamlit run app.py
   ```

3. **Open in browser:**
   ```
   http://localhost:8501
   ```

---

## 🧪 Test Your Setup

### Test AI Assistant:
1. Login to FoodMind AI
2. Go to **🤖 AI Assistant**
3. Ask: "What foods are high in protein?"
4. You should get an AI response! ✅

### Test Image Analysis:
1. Go to **🔍 Food Analysis**
2. Click **📸 Analyze Food Image** tab
3. Upload a food photo
4. Click **🤖 Analyze with AI**
5. Get nutrition estimates! ✅

---

## ❌ Common Issues & Solutions

### Issue 1: "Invalid API key format"
**Symptom:** Key starts with something other than `AIzaSy`

**Solution:**
- You might have copied the wrong key
- Go back to https://aistudio.google.com/app/apikey
- Create a NEW key
- Make sure it starts with `AIzaSy`

---

### Issue 2: "API key is invalid or has been revoked"
**Symptoms:** 
- Authentication failed
- 403 permission error

**Solutions:**
1. Check if key is still active at: https://aistudio.google.com/app/apikey
2. Delete old key and create a new one
3. Make sure you copied the ENTIRE key (39 characters)
4. Check for extra spaces in .env file

---

### Issue 3: "Model not found" or "404 error"
**Symptom:** `gemini-1.5-flash is not found`

**Solution:**
- Your API key might not have access to the model
- Try creating a fresh API key
- Ensure you're using the FREE tier key from Google AI Studio
- NOT Google Cloud Platform API key (different service)

---

### Issue 4: "Quota exceeded"
**Symptoms:**
- "API quota exceeded"
- Rate limit errors

**Solutions:**
- **Wait 1 minute** (15 requests/minute limit)
- **Wait 24 hours** for daily quota reset (1,500 requests/day)
- Check usage at: https://aistudio.google.com/app/apikey

---

### Issue 5: Spaces or quotes in .env file
**Wrong ❌:**
```
GEMINI_API_KEY = "AIzaSyDxxxxx"
GEMINI_API_KEY = 'AIzaSyDxxxxx'
GEMINI_API_KEY= AIzaSyDxxxxx (trailing space)
```

**Correct ✅:**
```
GEMINI_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
- No spaces around `=`
- No quotes
- No trailing spaces

---

## 📊 Free Tier Limits

| Feature | Free Tier Limit |
|---------|----------------|
| Requests per minute | 15 RPM |
| Requests per day | 1,500 RPD |
| Tokens per month | 1 million |
| Cost | **FREE** |
| Credit card | **Not required** |

**For FoodMind AI usage:**
- Each AI Assistant question = 1 request
- Each image analysis = 1 request
- Typical daily usage = 10-50 requests
- **You're well within free limits!** ✅

---

## 🔐 Security Best Practices

1. **Never share your API key publicly**
   - Don't post in forums, Discord, GitHub
   - `.env` file is in `.gitignore` (protected)

2. **Rotate keys regularly**
   - Create new key every few months
   - Delete old keys from Google AI Studio

3. **Monitor usage**
   - Check usage at: https://aistudio.google.com/app/apikey
   - Set up usage alerts if available

---

## 🎯 Models Used in FoodMind AI

### Primary: `gemini-1.5-flash`
- **Best for:** Quick responses, image analysis
- **Speed:** Fast (< 2 seconds)
- **Use case:** Food image analysis, quick nutrition questions
- **Free tier:** ✅ Fully supported

### Fallback: `gemini-1.5-pro`
- **Best for:** Complex queries, detailed analysis
- **Speed:** Slower (2-5 seconds)
- **Use case:** Detailed nutrition planning
- **Free tier:** ✅ Limited usage

---

## 💡 Tips for Best Results

### For AI Assistant:
- Ask specific questions
- Keep questions under 50 words
- Example good questions:
  - "What are high-protein vegetarian foods?"
  - "Suggest a 500-calorie breakfast"
  - "How can I increase my iron intake?"

### For Image Analysis:
- Use good lighting
- Clear, focused photos
- Include the whole plate
- Avoid blurry or dark images
- Best file formats: JPG, PNG
- Max file size: 5MB

---

## 📚 Additional Resources

- **Google AI Studio:** https://aistudio.google.com/
- **API Documentation:** https://ai.google.dev/docs
- **Model Info:** https://ai.google.dev/models/gemini
- **Pricing:** https://ai.google.dev/pricing

---

## ✅ Quick Checklist

- [ ] Created Google account (if needed)
- [ ] Visited https://aistudio.google.com/app/apikey
- [ ] Created API key (starts with AIzaSy)
- [ ] Opened `.env` file
- [ ] Pasted key: `GEMINI_API_KEY=AIzaSy...`
- [ ] Saved file (no spaces, no quotes)
- [ ] Restarted app
- [ ] Tested AI Assistant
- [ ] Tested Image Analysis

---

## 🆘 Still Not Working?

1. **Check .env file format:**
   ```bash
   # Run in terminal to see your key format
   cd "c:\Users\Saurav\Downloads\Foodmind AI .py"
   python test_gemini_api.py
   ```

2. **Verify key is valid:**
   - Go to https://aistudio.google.com/app/apikey
   - Check key status (should show "Active")

3. **Try a fresh start:**
   - Delete old API key
   - Create NEW API key
   - Update .env file
   - Restart app

4. **Check internet connection:**
   - API requires internet access
   - Check firewall settings

---

## 🎉 Success!

Once setup is complete, you'll have:
- ✅ AI-powered nutrition advice
- ✅ Automatic food image analysis
- ✅ Personalized meal suggestions
- ✅ All powered by FREE Gemini API!

Enjoy FoodMind AI! 🚀
