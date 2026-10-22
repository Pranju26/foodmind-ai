"""
AI nutrition assistant module for FoodMind AI
Provides AI-powered nutrition guidance using Gemini API
"""

import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv


# Load .env from project directory
PROJECT_ROOT = Path(__file__).parent.parent
ENV_PATH = PROJECT_ROOT / '.env'


def show_ai_assistant(db):
    """Display AI nutrition assistant interface"""
    st.title("🤖 AI Nutrition Assistant")
    
    st.markdown("""
    Get personalized nutrition guidance and answers to your food-related questions.
    """)
    
    # Check if API is configured
    api_configured, error_msg = check_gemini_api()
    
    if not api_configured:
        show_api_setup_instructions(error_msg)
        return
    
    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about nutrition, meals, or dietary advice..."):
        # Add user message to chat
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_ai_response(prompt, db)
                st.markdown(response)
        
        # Add assistant response to chat
        st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Sidebar with suggestions
    with st.sidebar:
        st.markdown("### 💡 Suggested Questions")
        
        suggestions = [
            "What are good sources of protein?",
            "How can I increase my fiber intake?",
            "Suggest a balanced vegetarian meal plan",
            "What foods are rich in iron?",
            "How much water should I drink daily?",
            "Explain the difference between simple and complex carbs",
            "What are healthy snack options?",
            "Tips for meal prep for the week"
        ]
        
        for suggestion in suggestions:
            if st.button(suggestion, key=f"sug_{suggestion[:20]}"):
                st.session_state.chat_history.append({"role": "user", "content": suggestion})
                st.rerun()
        
        st.markdown("---")
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()


def check_gemini_api():
    """Check if Gemini API is configured and return status with error message"""
    try:
        # Load .env from project directory explicitly
        load_dotenv(dotenv_path=ENV_PATH, override=True)
        api_key = os.getenv('GEMINI_API_KEY')
        
        # Check if key exists
        if not api_key or api_key == 'your_gemini_api_key_here':
            return False, "No API key found in .env file"
        
        # Check key length
        if len(api_key) < 30:
            return False, f"API key too short ({len(api_key)} characters)"
        
        # Check key format
        if not api_key.startswith('AIzaSy'):
            key_start = api_key[:7] if len(api_key) >= 7 else api_key
            return False, f"Invalid API key format. Key starts with '{key_start}...' but should start with 'AIzaSy'"
        
        # Test if google.generativeai is available
        try:
            import google.generativeai as genai
        except ImportError:
            return False, "google-generativeai library not installed. Run: pip install google-generativeai"
        
        # Test API key validity with actual API call
        try:
            genai.configure(api_key=api_key)
            # Try to list models as a validation test
            list(genai.list_models())
            return True, None
        except Exception as api_error:
            error_str = str(api_error)
            # Return sanitized error without exposing the key
            if "API_KEY_INVALID" in error_str:
                return False, "API key is invalid or has been revoked"
            elif "403" in error_str or "permission" in error_str.lower():
                return False, "API key lacks required permissions"
            elif "404" in error_str:
                return False, "API endpoint not found - service may be unavailable"
            elif "quota" in error_str.lower() or "limit" in error_str.lower():
                return False, "API quota exceeded"
            else:
                return False, f"API connection failed: {error_str[:100]}"
                
    except Exception as e:
        return False, f"Configuration error: {str(e)[:100]}"


def show_api_setup_instructions(error_msg=None):
    """Display setup instructions for Gemini API"""
    
    if error_msg:
        st.error(f"🔍 **Issue Detected:** {error_msg}")
    
    st.info("""
    ### 🤖 AI Assistant Setup Required
    
    The AI nutrition assistant needs a valid Gemini API key to work.
    """)
    
    st.markdown("""
    ### 📋 How to Get a Valid API Key:
    
    #### Step 1: Visit Google AI Studio
    🔗 **Go to:** https://aistudio.google.com/app/apikey
    
    #### Step 2: Create API Key
    1. Sign in with your Google account
    2. Click **"Create API Key"**
    3. Select "Create API key in new project" (recommended)
    4. **Copy the key** - it should look like: `AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
    
    #### Step 3: Update Your .env File
    1. Open: `c:\\Users\\Saurav\\Downloads\\Foodmind AI .py\\.env`
    2. Find the line: `GEMINI_API_KEY=...`
    3. Replace with your new key (no quotes, no spaces):
       ```
       GEMINI_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
       ```
    4. **Save the file**
    5. **Restart the app**
    
    ---
    
    ### ⚠️ Common Issues:
    
    **❌ Wrong Key Format (Your Current Issue)**
    - Your key starts with `AQ.Ab...` but should start with `AIzaSy...`
    - This is NOT a valid Gemini API key format
    - You need to create a NEW key from Google AI Studio
    
    **✅ Valid Key Format:**
    - Starts with: `AIzaSy`
    - Length: 39 characters
    - Example: `AIzaSyDaB1CdE2FgH3IjK4LmN5OpQ6RsT`
    
    **Other Common Issues:**
    - Spaces around `=` in .env file
    - Quotes around the key
    - Old/expired key
    - Wrong URL (use aistudio.google.com, not makersuite)
    """)
    
    with st.expander("📝 Correct .env File Format"):
        st.code("""# FoodMind AI Configuration
GEMINI_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Important:
# - No spaces around =
# - No quotes around key
# - Key starts with AIzaSy
# - 39 characters long
""", language="bash")
    
    st.success("""
    **Note:** All other features of FoodMind AI work without the API key. 
    Only the AI Assistant requires it.
    """)
    
    # Add a test button
    st.markdown("---")
    st.markdown("### 🧪 Test Your Configuration")
    
    if st.button("🔄 Reload and Validate API Key", type="primary"):
        api_configured, test_error = check_gemini_api()
        
        if api_configured:
            st.success("✅ API key is valid and working!")
            st.balloons()
            st.info("Refresh the page or navigate away and back to use the AI Assistant.")
        else:
            st.error(f"❌ Validation failed: {test_error}")
            st.warning("Please follow the instructions above to get a valid API key.")


def get_ai_response(user_message, db):
    """Get AI response from Gemini API with comprehensive error handling"""
    try:
        import google.generativeai as genai
        from database import db as db_module
        
        # Load .env from project directory explicitly
        load_dotenv(dotenv_path=ENV_PATH, override=True)
        api_key = os.getenv('GEMINI_API_KEY')
        
        # Validate API key
        if not api_key or api_key == 'your_gemini_api_key_here':
            return "❌ API key not configured. Please set up your Gemini API key in the .env file."
        
        if not api_key.startswith('AIzaSy'):
            return f"""❌ Invalid API key format detected.

**Issue:** Your API key starts with '{api_key[:7]}...' but should start with 'AIzaSy'

**Solution:**
1. Visit: https://aistudio.google.com/app/apikey
2. Create a NEW API key
3. Update your .env file with the new key
4. Restart the app

Current key format is not compatible with Gemini API."""
        
        # Configure Gemini
        try:
            genai.configure(api_key=api_key)
        except Exception as config_error:
            return f"❌ API configuration failed: {str(config_error)[:150]}"
        
        # Find available model
        model_to_use = 'gemini-pro'  # Default fallback
        
        try:
            # List available models
            available_models = list(genai.list_models())
            
            if available_models:
                # Find a suitable model with generateContent support
                for m in available_models:
                    if 'generateContent' in [method.name for method in m.supported_generation_methods]:
                        # Prefer newer models
                        if 'gemini-1.5' in m.name or 'gemini-pro' in m.name:
                            model_to_use = m.name.replace('models/', '')
                            break
        except Exception as list_error:
            # Log error but continue with default model
            error_str = str(list_error)
            if "API_KEY_INVALID" in error_str:
                return """❌ API Key Authentication Failed

Your API key is invalid or has been revoked.

**Steps to fix:**
1. Go to: https://aistudio.google.com/app/apikey
2. Check if your key is still active
3. If not, create a new API key
4. Update GEMINI_API_KEY in your .env file
5. Restart the app"""
            elif "403" in error_str or "permission" in error_str.lower():
                return """❌ API Permission Error

Your API key doesn't have permission to access Gemini models.

**Steps to fix:**
1. Go to: https://aistudio.google.com/app/apikey
2. Create a new API key with proper permissions
3. Update your .env file
4. Restart the app"""
            elif "quota" in error_str.lower():
                return """❌ API Quota Exceeded

You've reached your free tier limit.

**Options:**
- Wait 24 hours for quota reset
- Upgrade to paid tier in Google AI Studio"""
            # Continue with default model despite list error
        
        # Create model instance
        try:
            model = genai.GenerativeModel(model_to_use)
        except Exception as model_error:
            return f"❌ Model initialization failed: {str(model_error)[:150]}"
        
        # Get user context
        context = get_user_context(db)
        
        # Build prompt with context
        system_prompt = f"""You are FoodMind AI, a friendly and knowledgeable nutrition assistant.

User Context:
{context}

Guidelines:
- Provide accurate, evidence-based nutrition information
- Be encouraging and supportive
- Tailor advice to the user's profile and goals when available
- For meal suggestions, consider their dietary preferences
- Remind users to consult healthcare professionals for medical advice
- Keep responses conversational and easy to understand
- Use emojis appropriately to make responses engaging
- Keep responses concise but informative (2-4 paragraphs max)

User question: {user_message}

Please provide a helpful, friendly response:"""
        
        # Generate response
        try:
            response = model.generate_content(system_prompt)
            
            # Check if response was blocked or empty
            if not response or not hasattr(response, 'text'):
                return "⚠️ No response generated. Please try rephrasing your question."
            
            if not response.text:
                # Check feedback for reason
                if hasattr(response, 'prompt_feedback'):
                    feedback = str(response.prompt_feedback)
                    if 'SAFETY' in feedback or 'BLOCK' in feedback:
                        return "⚠️ Response blocked by safety filters. Please rephrase your question."
                return "⚠️ Empty response received. Please try again."
            
            return response.text
        
        except Exception as generation_error:
            error_str = str(generation_error)
            
            # Provide specific error messages based on error type
            if "404" in error_str or "not found" in error_str.lower():
                return f"""❌ Model Not Found Error

The model '{model_to_use}' is not accessible.

**Actual error:** {error_str[:200]}

**Try:**
1. Verify your API key at: https://aistudio.google.com/app/apikey
2. Create a new API key if needed
3. Update your .env file
4. Restart the app"""
            
            elif "API_KEY_INVALID" in error_str or "invalid" in error_str.lower():
                return f"""❌ Invalid API Key

**Error:** {error_str[:200]}

Your API key is not valid or has expired.

**Solution:**
1. Get a new key from: https://aistudio.google.com/app/apikey
2. Update GEMINI_API_KEY in .env
3. Restart the app"""
            
            elif "quota" in error_str.lower() or "limit" in error_str.lower():
                return f"""❌ API Quota Exceeded

**Error:** {error_str[:200]}

You've hit your API usage limit.

**Options:**
- Wait for quota reset (usually 24 hours)
- Check quota at: https://aistudio.google.com"""
            
            elif "safety" in error_str.lower() or "block" in error_str.lower():
                return "⚠️ Response blocked by safety filters. Please rephrase your question in a different way."
            
            else:
                # Return actual error for debugging
                return f"""❌ API Error

**Error details:** {error_str[:300]}

If this persists:
1. Check your internet connection
2. Verify API key at: https://aistudio.google.com/app/apikey
3. Try creating a new API key"""
    
    except ImportError:
        return """❌ Google Generative AI library not installed.

Run this command:
```
pip install google-generativeai
```

Then restart the application."""
    
    except Exception as e:
        error_str = str(e)
        return f"""❌ Unexpected Error

**Error:** {error_str[:300]}

**Troubleshooting:**
1. Check your .env file exists
2. Verify API key format (starts with AIzaSy)
3. Check internet connection
4. Try restarting the app

If issue persists, create a new API key from:
https://aistudio.google.com/app/apikey"""


def get_user_context(db):
    """Get user context for AI assistant"""
    from database import db as db_module
    from datetime import date
    
    try:
        context_parts = []
        
        # Get profile
        profile = db_module.get_user_profile(db)
        if profile:
            context_parts.append(f"""
Profile:
- Name: {profile['name']}
- Age: {profile['age']} years
- Weight: {profile['weight']} kg
- Height: {profile['height']} cm
- Activity Level: {profile['activity_level']}
- Dietary Preference: {profile['dietary_preference']}
- Nutrition Goal: {profile['nutrition_goal']}
""")
        
        # Get nutrition goals
        goals = db_module.get_nutrition_goals(db)
        if goals:
            context_parts.append(f"""
Daily Nutrition Goals:
- Calories: {goals['daily_calories']:.0f} kcal
- Protein: {goals['daily_protein']:.0f}g
- Carbohydrates: {goals['daily_carbs']:.0f}g
- Fat: {goals['daily_fat']:.0f}g
- Water: {goals['daily_water']:.1f} liters
""")
        
        # Get today's intake
        today = date.today().strftime("%Y-%m-%d")
        summary = db_module.get_daily_nutrition_summary(db, today)
        if summary and summary['meal_count'] > 0:
            context_parts.append(f"""
Today's Intake:
- Calories consumed: {summary['total_calories']:.0f} kcal
- Protein: {summary['total_protein']:.1f}g
- Carbohydrates: {summary['total_carbs']:.1f}g
- Fat: {summary['total_fat']:.1f}g
- Meals logged: {summary['meal_count']}
""")
        
        # Get recent meals
        recent_meals = db_module.get_recent_meals(db, limit=5)
        if recent_meals:
            meals_text = "\n".join([f"- {meal['food_name']} ({meal['meal_type']}): {meal['calories']:.0f} cal" 
                                   for meal in recent_meals[:3]])
            context_parts.append(f"\nRecent Meals:\n{meals_text}")
        
        if context_parts:
            return "\n".join(context_parts)
        else:
            return "No user data available yet. User is new to the platform."
    
    except Exception as e:
        return "Unable to retrieve user context."
