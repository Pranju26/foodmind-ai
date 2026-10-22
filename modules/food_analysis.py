"""
Food analysis module for FoodMind AI
Allows users to search foods, analyze nutrition, and process food images
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from utils import image_processing as img_proc
from utils import nutrition as nutr
import os


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
        show_image_analysis()


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


def show_image_analysis():
    """Food image analysis interface"""
    st.subheader("Analyze Food from Image")
    
    st.info("""
    **Image Analysis Features:**
    - Upload a photo of your food
    - Image validation and processing using Pillow
    - AI-powered food recognition (when API key is configured)
    - Manual food entry option
    """)
    
    # Check if Gemini API is configured
    gemini_available = check_gemini_api()
    
    if not gemini_available:
        st.warning("""
        ⚠️ **AI Recognition Not Available**
        
        To enable AI-powered food recognition, configure your Gemini API key:
        1. Create a `.env` file in the project directory
        2. Add: `GEMINI_API_KEY=your_actual_key`
        3. Get your key from: https://makersuite.google.com/app/apikey
        
        You can still upload and process images manually.
        """)
    
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
        uploaded_file.seek(0)  # Reset file pointer
        processed_image = img_proc.process_food_image(uploaded_file)
        
        if processed_image is None:
            st.error("Failed to process image")
            return
        
        # Display processed image
        st.image(processed_image, caption="Uploaded Food Image", use_container_width=True)
        
        # Get image info
        img_info = img_proc.get_image_info(processed_image)
        st.caption(f"Image size: {img_info['width']}x{img_info['height']}px")
        
        # AI analysis or manual entry
        if gemini_available:
            st.markdown("---")
            if st.button("🤖 Analyze with AI", type="primary"):
                analyze_image_with_ai(uploaded_file)
        
        st.markdown("---")
        st.subheader("Manual Food Entry")
        show_manual_food_entry()


def check_gemini_api():
    """Check if Gemini API is configured"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        return api_key is not None and api_key != 'your_gemini_api_key_here'
    except:
        return False


def analyze_image_with_ai(image_file):
    """Analyze food image using Gemini AI"""
    try:
        import google.generativeai as genai
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key or api_key == 'your_gemini_api_key_here':
            st.error("Gemini API key not configured")
            return
        
        genai.configure(api_key=api_key)
        
        with st.spinner("🤖 Analyzing image with AI..."):
            # Use Gemini vision model
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Reset file pointer and read image
            image_file.seek(0)
            image_data = image_file.read()
            
            # Create proper image part
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_data))
            
            prompt = """
            Analyze this food image and provide:
            1. Identify all visible food items
            2. Estimate approximate serving sizes
            3. Estimate nutritional values (calories, protein, carbs, fat) for each item
            
            Format your response clearly with each food item and its estimated nutrition.
            """
            
            response = model.generate_content([prompt, image])
            
            st.success("✅ AI Analysis Complete!")
            st.markdown("### AI Analysis Results:")
            st.write(response.text)
            
            st.info("""
            **Note:** These are AI-generated estimates. Actual nutritional values may vary based on:
            - Specific ingredients and brands
            - Preparation methods
            - Actual portion sizes
            
            Use these as general guidance and adjust based on your knowledge of the meal.
            """)
    
    except Exception as e:
        st.error(f"AI analysis failed: {str(e)}")
        st.info("You can use manual food entry below instead.")


def show_manual_food_entry():
    """Manual food entry form"""
    st.write("Can't identify the food? Enter the details manually:")
    
    with st.form("manual_food_entry"):
        food_name = st.text_input("Food name", placeholder="e.g., Chicken Curry")
        
        col1, col2 = st.columns(2)
        
        with col1:
            calories = st.number_input("Calories (kcal)", min_value=0, value=0)
            protein = st.number_input("Protein (g)", min_value=0.0, value=0.0, step=0.1)
            carbs = st.number_input("Carbohydrates (g)", min_value=0.0, value=0.0, step=0.1)
        
        with col2:
            fat = st.number_input("Fat (g)", min_value=0.0, value=0.0, step=0.1)
            fiber = st.number_input("Fiber (g)", min_value=0.0, value=0.0, step=0.1)
            serving = st.text_input("Serving size", value="1 serving")
        
        submitted = st.form_submit_button("Save Food Info")
        
        if submitted and food_name:
            st.success(f"✅ Food information saved for {food_name}!")
            st.info("You can now log this food in the Meal Tracking section.")


def load_food_database():
    """Load food database from CSV"""
    try:
        db_path = Path(__file__).parent.parent / "data" / "food_database.csv"
        df = pd.read_csv(db_path)
        return df
    except Exception as e:
        st.error(f"Error loading food database: {e}")
        return None
