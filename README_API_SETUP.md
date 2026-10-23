# 🚀 Quick Start: Gemini Free API for FoodMind AI

## ⚡ 3-Minute Setup

### Step 1: Get FREE API Key (1 min)
1. Visit: **https://aistudio.google.com/app/apikey**
2. Sign in with Google
3. Click **"Create API Key"** (no credit card needed)
4. Copy the key (starts with `AIzaSy`)

### Step 2: Update .env File (30 sec)
1. Open: `.env` in the project folder
2. Add your key:
   ```
   GEMINI_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
3. Save (Ctrl+S)

### Step 3: Test (30 sec)
Run in terminal:
```bash
python test_gemini_api.py
```

### Step 4: Start App (1 min)
```bash
streamlit run app.py
```

Open: **http://localhost:8501**

---

## ✅ What You Get (FREE)

- **🤖 AI Nutrition Assistant** - Ask nutrition questions
- **📸 Food Image Analysis** - Analyze food photos
- **15 requests/minute** - Perfect for personal use
- **1,500 requests/day** - More than enough
- **No credit card** - Completely free

---

## 🎯 Free Tier Limits

| Feature | Limit |
|---------|-------|
| Requests per minute | 15 |
| Requests per day | 1,500 |
| Tokens per month | 1 million |
| **Cost** | **FREE** |

---

## ❓ Common Issues

### "Invalid API key format"
- Key must start with `AIzaSy`
- Get from: https://aistudio.google.com/app/apikey

### "Quota exceeded"
- Wait 1 minute (15/min limit)
- OR wait 24 hours (1500/day limit)

### "Model not found"
- Create new key from Google AI Studio
- NOT Google Cloud Platform

---

## 📚 Full Documentation

- **Complete Setup Guide**: `GEMINI_FREE_API_SETUP.md`
- **Test Script**: `test_gemini_api.py`
- **Get API Key**: https://aistudio.google.com/app/apikey

---

## 🎉 That's It!

You're ready to use AI features in FoodMind AI!

**Models Used:**
- `gemini-1.5-flash` (fast, optimized for images)
- `gemini-1.5-pro` (detailed analysis)

Both are **FREE**! 🚀
