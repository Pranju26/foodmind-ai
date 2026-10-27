# FoodMind AI - Setup Instructions

## 🚨 CURRENT ISSUES & FIXES

You're experiencing two main problems:

### Issue 1: Invalid API Key ❌
**Problem:** Your `.env` file contains an invalid Gemini API key
- Current key starts with: `AQ.Ab...`
- Valid Gemini keys start with: `AIzaSy`
- Your key is from a different service (not Gemini)

### Issue 2: Console Shows Nothing 🖥️
**Problem:** No output in console when running the app
- This is because packages might not be installed in the correct Python environment
- OR the Streamlit app is not starting properly

---

## 📝 COMPLETE FIX - Step by Step

### Step 1: Install Required Packages

Open your terminal/command prompt and run:

```bash
cd "c:\Users\Saurav\Downloads\Foodmind AI .py"
pip install -r requirements.txt
```

If that doesn't work, install packages individually:

```bash
pip install streamlit pillow pandas matplotlib requests google-generativeai python-dotenv
```

### Step 2: Get a Valid Gemini API Key

1. **Visit Google AI Studio:**
   - Go to: https://aistudio.google.com/app/apikey
   
2. **Sign in with your Google account**

3. **Create API Key:**
   - Click the **"Create API Key"** button
   - Select "Create API key in new project" (recommended)
   
4. **Copy the key:**
   - The key will look like: `AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - It MUST start with `AIzaSy`
   - It will be 39 characters long
   - **Copy it immediately** (you can't view it again later)

5. **Update .env file:**
   - Open file: `c:\Users\Saurav\Downloads\Foodmind AI .py\.env`
   - Find the line: `GEMINI_API_KEY=your_gemini_api_key_here`
   - Replace with your new key (NO quotes, NO spaces):
     ```
     GEMINI_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
     ```
   - Save the file

### Step 3: Run the Application

```bash
cd "c:\Users\Saurav\Downloads\Foodmind AI .py"
streamlit run app.py
```

You should see output like:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Step 4: Verify Setup

1. Open the app in your browser (it should open automatically)
2. Navigate to the **AI Assistant** page
3. The app will validate your API key
4. If valid, you can start asking nutrition questions!

---

## 🔍 TROUBLESHOOTING

### Problem: "streamlit: command not found"

**Solution:** Streamlit is not installed or not in PATH

```bash
# Try pip3 instead
pip3 install streamlit

# Or use python -m
python -m pip install streamlit

# Then run app with:
python -m streamlit run app.py
```

### Problem: "Module not found" errors

**Solution:** Install missing packages

```bash
pip install google-generativeai python-dotenv
```

### Problem: API key still not working

**Solution:** Verify your key format

Your API key MUST:
- Start with `AIzaSy`
- Be exactly 39 characters
- Have no spaces or quotes around it
- Be on a single line in .env

Example of CORRECT .env format:
```
GEMINI_API_KEY=AIzaSyDaB1CdE2FgH3IjK4LmN5OpQ6RsT7UvW8X
```

Example of WRONG formats:
```
GEMINI_API_KEY="AIzaSyDaB1CdE2FgH3IjK4LmN5OpQ6RsT7UvW8X"  # NO quotes
GEMINI_API_KEY = AIzaSyDaB1CdE2FgH3IjK4LmN5OpQ6RsT7UvW8X  # NO spaces
GEMINI_API_KEY=AQ.Ab8RN6Jm0iyyKOos_BU...  # WRONG key type
```

### Problem: Console still shows nothing

**Solution:** Check Python environment

1. Verify Python is installed:
   ```bash
   python --version
   ```

2. Check if packages are installed:
   ```bash
   pip list | findstr streamlit
   pip list | findstr google-generativeai
   ```

3. If packages not found, you might have multiple Python installations. Use:
   ```bash
   python -m pip install streamlit google-generativeai python-dotenv
   ```

### Problem: "API_KEY_INVALID" error

**Causes:**
- Key is expired or revoked
- Key is from wrong Google project
- Key doesn't have Gemini API access

**Solution:**
1. Go back to https://aistudio.google.com/app/apikey
2. Create a BRAND NEW key
3. Replace in .env file
4. Restart the app

---

## ✅ VERIFICATION STEPS

### 1. Check Python & Packages
```bash
python --version
pip list | findstr "streamlit google-generativeai python-dotenv"
```

### 2. Check .env File Format
Open `.env` and verify:
- File exists in project root
- API key starts with `AIzaSy`
- No quotes, no extra spaces
- File is saved (not just edited)

### 3. Test API Connection
```bash
python check_setup.py
```

### 4. Run Application
```bash
streamlit run app.py
```

---

## 📞 STILL HAVING ISSUES?

If problems persist:

1. **Delete .env file completely** and create new one:
   ```
   GEMINI_API_KEY=AIzaSyYOUR_NEW_KEY_HERE
   ```

2. **Restart your computer** (sometimes environment variables need refresh)

3. **Try a different terminal** (Command Prompt vs PowerShell vs Git Bash)

4. **Check Google AI Studio** to ensure API is enabled:
   - Go to https://aistudio.google.com/app/apikey
   - Verify your key is listed and active

---

## 🎯 QUICK START (TL;DR)

```bash
# 1. Install packages
cd "c:\Users\Saurav\Downloads\Foodmind AI .py"
pip install streamlit google-generativeai python-dotenv

# 2. Get API key from: https://aistudio.google.com/app/apikey

# 3. Edit .env file:
# GEMINI_API_KEY=AIzaSyYOUR_KEY_HERE

# 4. Run app
streamlit run app.py

# 5. Open browser to http://localhost:8501
# 6. Go to AI Assistant page
```

---

## 🌟 Features That Work Without API Key

The following features work perfectly WITHOUT a Gemini API key:
- ✅ Dashboard
- ✅ Food Analysis
- ✅ Meal Tracking
- ✅ Nutrition Reports
- ✅ Profile & Goals
- ❌ AI Assistant (requires API key)

So even if you can't get the API key working immediately, you can still use 95% of the app!

---

**Last Updated:** Based on your error where:
- Invalid API key format detected (starts with `AQ.Ab...`)
- Console shows no output
- Streamlit app may not be starting
