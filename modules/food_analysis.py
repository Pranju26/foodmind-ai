"""
Food analysis module for FoodMind AI
Allows users to search foods, analyze nutrition, and process food images
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from utils import image_processing as img_proc
from utils import nutrition as nutr
from utils import validators
from database import db as db_module
from datetime import date
import os
import json
import re


def show_food_analysis(db):
    """Display food analysis page"""
    st.title("🔍 Food Analysis")
    
    st.markdown("""
    Search for foods, view nutritional information, and analyze food images.
    """)
    
    # Tabs for different analysis methods
    tab1, tab2 = st.tabs(["📝 Search Food Database", "📸 Analyze Food Image"])
    
    with tab1:
        show_food_search()
    
    with tab2:
        show_image_analysis(db)


def show_food_search():
    """Food database search interface"""
    st.subheader("Search Food Database")
    
    # Load food database
    food_df = load_food_database()
    
    if food_df is None or food_df.empty:
        st.error("Food database not found or empty")
        return
    
    # Search interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Search for a food item",
            placeholder="e.g., rice, chicken, apple"
        )
    
    with col2:
        category_filter = st.selectbox(
            "Category",
            ["All"] + sorted(food_df['category'].unique().tolist())
        )
    
    # Filter foods
    filtered_df = food_df.copy()
    
    if search_query:
        filtered_df = filtered_df[
            filtered_df['food_name'].str.contains(search_query, case=False, na=False)
        ]
    
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df['category'] == category_filter]
    
    # Display results
    if not filtered_df.empty:
        st.write(f"Found {len(filtered_df)} items")
        
        # Display as cards
        for idx, row in filtered_df.iterrows():
            with st.expander(f"**{row['food_name']}** - {row['category']}"):
                display_food_nutrition(row)
    else:
        st.info("No foods found. Try a different search term.")


def display_food_nutrition(food_data):
    """Display detailed nutrition information for a food item"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Serving Size**")
        st.write(food_data['serving_size'])
        
        st.markdown("**Calories**")
        st.write(f"{food_data['calories']} kcal")
        
        st.markdown("**Protein**")
        st.write(f"{food_data['protein']}g")
    
    with col2:
        st.markdown("**Carbohydrates**")
        st.write(f"{food_data['carbohydrates']}g")
        
        st.markdown("**Fat**")
        st.write(f"{food_data['fat']}g")
        
        st.markdown("**Fiber**")
        st.write(f"{food_data['fiber']}g")
    
    # Serving calculator
    st.markdown("---")
    st.markdown("**Calculate for different serving**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        multiplier = st.number_input(
            "Quantity",
            min_value=0.1,
            max_value=20.0,
            value=1.0,
            step=0.5,
            key=f"qty_{food_data['food_name']}"
        )
    
    with col2:
        st.markdown("**Adjusted Values:**")
        st.write(f"Calories: {food_data['calories'] * multiplier:.1f} kcal")
        st.write(f"Protein: {food_data['protein'] * multiplier:.1f}g")
        st.write(f"Carbs: {food_data['carbohydrates'] * multiplier:.1f}g")
        st.write(f"Fat: {food_data['fat'] * multiplier:.1f}g")


def init_food_entry_state():
    """Initialize session state defaults for food entry form"""
    if 'manual_food_name' not in st.session_state:
        st.session_state.manual_food_name = ""
    if 'manual_calories' not in st.session_state:
        st.session_state.manual_calories = 0.0
    if 'manual_protein' not in st.session_state:
        st.session_state.manual_protein = 0.0
    if 'manual_carbs' not in st.session_state:
        st.session_state.manual_carbs = 0.0
    if 'manual_fat' not in st.session_state:
        st.session_state.manual_fat = 0.0
    if 'manual_fiber' not in st.session_state:
        st.session_state.manual_fiber = 0.0
    if 'manual_serving' not in st.session_state:
        st.session_state.manual_serving = "1 serving"
    if 'ai_analysis_text' not in st.session_state:
        st.session_state.ai_analysis_text = None
    if 'ai_autofilled' not in st.session_state:
        st.session_state.ai_autofilled = False


def extract_nutrition_from_ai(text):
    """
    Extract structured food name, calories, macros, and serving from Gemini text.
    Handles JSON code blocks, inline JSON objects, and regex patterns.
    """
    extracted = {
        'food_name': '',
        'calories': 0.0,
        'protein': 0.0,
        'carbohydrates': 0.0,
        'fat': 0.0,
        'fiber': 0.0,
        'serving_size': '1 serving'
    }
    
    # 1. Attempt fenced JSON block: ```json { ... } ```
    json_match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', text)
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            for k in extracted:
                if k in data and data[k] is not None:
                    try:
                        if k in ['calories', 'protein', 'carbohydrates', 'fat', 'fiber']:
                            extracted[k] = float(data[k])
                        else:
                            extracted[k] = str(data[k])
                    except (ValueError, TypeError):
                        pass
            if extracted['food_name'] or extracted['calories'] > 0:
                return extracted
        except Exception:
            pass

    # 2. Attempt raw JSON object containing calories or food_name
    raw_match = re.search(r'\{[\s\S]*?"(?:calories|food_name)"[\s\S]*?\}', text)
    if raw_match:
        try:
            data = json.loads(raw_match.group(0))
            for k in extracted:
                if k in data and data[k] is not None:
                    try:
                        if k in ['calories', 'protein', 'carbohydrates', 'fat', 'fiber']:
                            extracted[k] = float(data[k])
                        else:
                            extracted[k] = str(data[k])
                    except (ValueError, TypeError):
                        pass
            if extracted['food_name'] or extracted['calories'] > 0:
                return extracted
        except Exception:
            pass

    # 3. Regex Fallback
    name_m = re.search(r'(?:food(?:\s+items?)?(?:\s+identified)?|dish(?:\s+name)?):\s*[*_]*([A-Za-z0-9\s,\-\(\)]+?)[*_\n]', text, re.IGNORECASE)
    if name_m:
        extracted['food_name'] = name_m.group(1).strip()
    
    cal_m = re.search(r'(?:calories|total calories|energy)[:\s*]+([0-9]+(?:\.[0-9]+)?)\s*(?:kcal|cal)?', text, re.IGNORECASE)
    if cal_m:
        try:
            extracted['calories'] = float(cal_m.group(1))
        except:
            pass
            
    prot_m = re.search(r'protein[:\s*]+([0-9]+(?:\.[0-9]+)?)\s*g?', text, re.IGNORECASE)
    if prot_m:
        try:
            extracted['protein'] = float(prot_m.group(1))
        except:
            pass
            
    carb_m = re.search(r'(?:carbohydrates|carbs)[:\s*]+([0-9]+(?:\.[0-9]+)?)\s*g?', text, re.IGNORECASE)
    if carb_m:
        try:
            extracted['carbohydrates'] = float(carb_m.group(1))
        except:
            pass
            
    fat_m = re.search(r'\bfat[:\s*]+([0-9]+(?:\.[0-9]+)?)\s*g?', text, re.IGNORECASE)
    if fat_m:
        try:
            extracted['fat'] = float(fat_m.group(1))
        except:
            pass
            
    fiber_m = re.search(r'fiber[:\s*]+([0-9]+(?:\.[0-9]+)?)\s*g?', text, re.IGNORECASE)
    if fiber_m:
        try:
            extracted['fiber'] = float(fiber_m.group(1))
        except:
            pass
            
    serv_m = re.search(r'serving(?:\s+size)?[:\s*]+([^\n\r*]+)', text, re.IGNORECASE)
    if serv_m:
        extracted['serving_size'] = serv_m.group(1).strip()

    return extracted


def show_image_analysis(db=None):
    """Food image analysis interface with AI auto-fill into Manual Food Entry"""
    init_food_entry_state()
    st.subheader("Analyze Food from Image")
    
    st.info("""
    **Image Analysis Features:**
    - Upload a photo of your food.
    - AI analyzes the dish and identifies nutrition content.
    - **AI automatically pre-fills the food entry table below** so you can review, adjust, and log your meal with one click!
    """)
    
    gemini_available = check_gemini_api()
    if not gemini_available:
        st.warning("⚠️ Gemini API key is not configured in `.env`. You can still enter food details manually below.")
    
    # Image upload
    uploaded_file = st.file_uploader(
        "Upload food image",
        type=['jpg', 'jpeg', 'png', 'webp'],
        help="Maximum file size: 5MB"
    )
    
    if uploaded_file is not None:
        # Validate image
        is_valid, error_msg = img_proc.validate_image(uploaded_file)
        if not is_valid:
            st.error(f"❌ {error_msg}")
            return
        
        # Process image
        uploaded_file.seek(0)
        processed_image = img_proc.process_food_image(uploaded_file)
        
        if processed_image is None:
            st.error("Failed to process image")
            return
        
        # Display processed image
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(processed_image, caption="Uploaded Food Image", width=400)
        
        img_info = img_proc.get_image_info(processed_image)
        st.caption(f"Image size: {img_info['width']}x{img_info['height']}px")
        
        # AI analysis button
        if gemini_available:
            st.markdown("---")
            if st.button("🤖 Analyze with AI & Auto-Fill Table", type="primary", use_container_width=True):
                analyze_image_with_ai(uploaded_file)
    
    # Display AI analysis results expander if available
    if st.session_state.get('ai_analysis_text'):
        st.markdown("---")
        with st.expander("📋 **Detailed AI Nutritional Analysis**", expanded=True):
            st.markdown(st.session_state.ai_analysis_text)
            
    if st.session_state.get('ai_autofilled'):
        st.success("✨ **AI Analysis Complete!** Food details have been automatically populated in the table below. You can review and log this meal.")

    st.markdown("---")
    st.subheader("Manual Food Entry")
    show_manual_food_entry(db)


def get_gemini_api_key():
    """Retrieve Gemini API key from environment variable or Streamlit secrets"""
    from dotenv import load_dotenv
    load_dotenv()
    key = os.getenv('GEMINI_API_KEY')
    if not key or key == 'your_gemini_api_key_here':
        try:
            if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
                key = st.secrets['GEMINI_API_KEY']
        except Exception:
            pass
    return key.strip().strip("'\"") if key else None


def check_gemini_api():
    """Check if Gemini API is configured"""
    try:
        api_key = get_gemini_api_key()
        return api_key is not None and len(api_key) > 10
    except:
        return False


def analyze_image_with_ai(image_file):
    """Analyze food image using Gemini AI and autofill the Manual Food Entry form"""
    try:
        import google.generativeai as genai
        
        api_key = get_gemini_api_key()
        
        if not api_key:
            st.error("Gemini API key not configured. Please add GEMINI_API_KEY to your .env file or Streamlit Secrets.")
            return
        
        genai.configure(api_key=api_key)
        
        with st.spinner("🤖 Analyzing food image with AI..."):
            preferred_models = [
                'gemini-3.5-flash-lite',
                'gemini-3.8-flash',
                'gemini-flash-latest',
                'gemini-3.1-flash-lite',
                'gemini-2.5-flash-lite',
                'gemini-1.5-flash'
            ]
            model_to_use = 'gemini-3.5-flash-lite'
            try:
                available = list(genai.list_models())
                supported = [
                    m.name.replace('models/', '') 
                    for m in available 
                    if 'generateContent' in [method.name for method in m.supported_generation_methods]
                ]
                for pref in preferred_models:
                    if pref in supported:
                        model_to_use = pref
                        break
            except Exception:
                pass
            
            try:
                model = genai.GenerativeModel(model_to_use)
            except Exception as model_error:
                st.error(f"Failed to initialize model: {str(model_error)}")
                return
            
            image_file.seek(0)
            image_data = image_file.read()
            
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_data))
            
            prompt = """Analyze this food image in detail.
Provide:
1. **Food Items Identified:** Name and description of visible food items
2. **Estimated Portion & Serving Size**
3. **Nutritional Breakdown:** Calories (kcal), Protein (g), Carbohydrates (g), Fat (g), and Dietary Fiber (g)

CRITICAL: At the very end of your response, output a single JSON code block with the exact estimated totals formatted like this:
```json
{
  "food_name": "Main dish or food name",
  "calories": 350.0,
  "protein": 28.0,
  "carbohydrates": 12.0,
  "fat": 15.0,
  "fiber": 3.0,
  "serving_size": "1 serving (approx 250g)"
}
```
"""
            try:
                response = model.generate_content([prompt, image])
                if not response or not hasattr(response, 'text') or not response.text:
                    st.warning("⚠️ No response generated. Please try again.")
                    return
                
                raw_text = response.text
                extracted = extract_nutrition_from_ai(raw_text)
                
                if extracted['food_name']:
                    st.session_state.manual_food_name = extracted['food_name']
                st.session_state.manual_calories = float(extracted['calories'])
                st.session_state.manual_protein = float(extracted['protein'])
                st.session_state.manual_carbs = float(extracted['carbohydrates'])
                st.session_state.manual_fat = float(extracted['fat'])
                st.session_state.manual_fiber = float(extracted['fiber'])
                if extracted['serving_size']:
                    st.session_state.manual_serving = extracted['serving_size']
                
                clean_text = re.sub(r'```(?:json)?\s*\{[\s\S]*?\}\s*```', '', raw_text).strip()
                st.session_state.ai_analysis_text = clean_text if clean_text else raw_text
                st.session_state.ai_autofilled = True
                
                st.rerun()
                
            except Exception as gen_error:
                error_str = str(gen_error)
                if "quota" in error_str.lower():
                    st.error("❌ API quota exceeded. Please wait a minute and try again.")
                elif "404" in error_str:
                    st.error("❌ Model endpoint not available.")
                else:
                    st.error(f"❌ Generation failed: {error_str[:200]}")
                return
            
    except Exception as e:
        st.error(f"AI analysis failed: {str(e)}")
        st.info("You can use manual food entry below instead.")


def show_manual_food_entry(db=None):
    """Manual food entry form with support for AI auto-population and direct meal logging"""
    init_food_entry_state()
    st.write("Can't identify the food? Enter the details manually:")
    
    with st.form("manual_food_entry"):
        food_name = st.text_input(
            "Food name", 
            value=st.session_state.manual_food_name, 
            placeholder="e.g., Chicken Curry"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            calories = st.number_input(
                "Calories (kcal)", 
                min_value=0.0, 
                value=float(st.session_state.manual_calories), 
                step=1.0
            )
            protein = st.number_input(
                "Protein (g)", 
                min_value=0.0, 
                value=float(st.session_state.manual_protein), 
                step=0.1
            )
            carbs = st.number_input(
                "Carbohydrates (g)", 
                min_value=0.0, 
                value=float(st.session_state.manual_carbs), 
                step=0.1
            )
        
        with col2:
            fat = st.number_input(
                "Fat (g)", 
                min_value=0.0, 
                value=float(st.session_state.manual_fat), 
                step=0.1
            )
            fiber = st.number_input(
                "Fiber (g)", 
                min_value=0.0, 
                value=float(st.session_state.manual_fiber), 
                step=0.1
            )
            serving = st.text_input(
                "Serving size", 
                value=st.session_state.manual_serving
            )
            
        st.markdown("##### 📅 Meal Logging Options")
        opt_col1, opt_col2 = st.columns(2)
        with opt_col1:
            meal_date = st.date_input("Date", value=date.today())
        with opt_col2:
            meal_type = st.selectbox(
                "Meal Type",
                ["lunch", "breakfast", "dinner", "snack"],
                format_func=lambda x: x.capitalize()
            )
        
        btn_col1, btn_col2 = st.columns([2, 1])
        with btn_col1:
            submitted = st.form_submit_button("🍽️ Save Food & Log Meal", type="primary", use_container_width=True)
        with btn_col2:
            cleared = st.form_submit_button("🔄 Reset Fields", use_container_width=True)
            
        if cleared:
            st.session_state.manual_food_name = ""
            st.session_state.manual_calories = 0.0
            st.session_state.manual_protein = 0.0
            st.session_state.manual_carbs = 0.0
            st.session_state.manual_fat = 0.0
            st.session_state.manual_fiber = 0.0
            st.session_state.manual_serving = "1 serving"
            st.session_state.ai_analysis_text = None
            st.session_state.ai_autofilled = False
            st.rerun()
        
        if submitted:
            if not food_name or len(food_name.strip()) < 2:
                st.error("Please enter a valid food name (at least 2 characters).")
            else:
                meal_data = {
                    'date': meal_date.strftime("%Y-%m-%d"),
                    'meal_type': meal_type,
                    'food_name': food_name.strip(),
                    'serving_size': serving.strip() if serving else "1 serving",
                    'quantity': 1.0,
                    'calories': float(calories),
                    'protein': float(protein),
                    'carbohydrates': float(carbs),
                    'fat': float(fat),
                    'fiber': float(fiber)
                }
                
                if db is not None:
                    try:
                        db_module.add_meal_record(db, meal_data)
                        st.success(f"✅ Successfully logged **{food_name}** ({calories:.0f} kcal) to today's {meal_type.capitalize()}!")
                        st.balloons()
                    except Exception as err:
                        st.error(f"Error saving meal: {err}")
                else:
                    st.success(f"✅ Food information saved for **{food_name}**!")
                    st.info("You can now view or log this food in the Meal Tracking section.")


def load_food_database():
    """Load food database from CSV"""
    try:
        db_path = Path(__file__).parent.parent / "data" / "food_database.csv"
        df = pd.read_csv(db_path)
        return df
    except Exception as e:
        st.error(f"Error loading food database: {e}")
        return None
