"""
Meal tracking module for FoodMind AI
Allows users to log, edit, and view meal records
"""

import streamlit as st
from datetime import date, datetime
import pandas as pd
from pathlib import Path
from database import db as db_module
from utils import validators, nutrition as nutr


def show_meal_tracking(db):
    """Display meal tracking interface"""
    st.title("🍽️ Meal Tracking")
    
    st.markdown("""
    Log your meals and track your daily nutrition intake.
    """)
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["➕ Log Meal", "📋 View Meals", "📅 Meal History"])
    
    with tab1:
        show_log_meal(db)
    
    with tab2:
        show_today_meals(db)
    
    with tab3:
        show_meal_history(db)


def show_log_meal(db):
    """Meal logging form"""
    st.subheader("Log a New Meal")
    
    # Load food database
    food_df = load_food_database()
    
    with st.form("meal_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            meal_date = st.date_input(
                "Date",
                value=date.today(),
                max_value=date.today()
            )
            
            meal_type = st.selectbox(
                "Meal Type",
                ["breakfast", "lunch", "dinner", "snack"],
                format_func=lambda x: x.capitalize()
            )
        
        with col2:
            # Quick selection from database or manual entry
            entry_method = st.radio(
                "Entry Method",
                ["Select from Database", "Enter Manually"],
                horizontal=True
            )
        
        if entry_method == "Select from Database":
            if food_df is not None and not food_df.empty:
                food_names = food_df['food_name'].tolist()
                selected_food = st.selectbox("Select Food", food_names)
                
                # Get food data
                food_data = food_df[food_df['food_name'] == selected_food].iloc[0]
                
                quantity = st.number_input(
                    "Quantity",
                    min_value=0.1,
                    max_value=20.0,
                    value=1.0,
                    step=0.5,
                    help="Multiplier for the standard serving"
                )
                
                # Display estimated nutrition
                st.markdown("**Estimated Nutrition:**")
                col_a, col_b, col_c, col_d = st.columns(4)
                
                with col_a:
                    st.write(f"🔥 {food_data['calories'] * quantity:.0f} cal")
                with col_b:
                    st.write(f"💪 {food_data['protein'] * quantity:.1f}g protein")
                with col_c:
                    st.write(f"🍞 {food_data['carbohydrates'] * quantity:.1f}g carbs")
                with col_d:
                    st.write(f"🥑 {food_data['fat'] * quantity:.1f}g fat")
                
                # Prepare meal data
                meal_data = {
                    'date': meal_date.strftime("%Y-%m-%d"),
                    'meal_type': meal_type,
                    'food_name': selected_food,
                    'serving_size': f"{quantity} × {food_data['serving_size']}",
                    'quantity': quantity,
                    'calories': food_data['calories'] * quantity,
                    'protein': food_data['protein'] * quantity,
                    'carbohydrates': food_data['carbohydrates'] * quantity,
                    'fat': food_data['fat'] * quantity,
                    'fiber': food_data['fiber'] * quantity
                }
            else:
                st.error("Food database not available")
                meal_data = None
        
        else:  # Manual entry
            food_name = st.text_input("Food Name", placeholder="e.g., Homemade Dal")
            serving_size = st.text_input("Serving Size", value="1 serving")
            quantity = st.number_input("Quantity", min_value=0.1, value=1.0, step=0.5)
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                calories = st.number_input("Calories (kcal)", min_value=0, value=0)
                protein = st.number_input("Protein (g)", min_value=0.0, value=0.0, step=0.1)
            
            with col_b:
                carbs = st.number_input("Carbohydrates (g)", min_value=0.0, value=0.0, step=0.1)
                fat = st.number_input("Fat (g)", min_value=0.0, value=0.0, step=0.1)
            
            fiber = st.number_input("Fiber (g)", min_value=0.0, value=0.0, step=0.1)
            
            meal_data = {
                'date': meal_date.strftime("%Y-%m-%d"),
                'meal_type': meal_type,
                'food_name': food_name,
                'serving_size': serving_size,
                'quantity': quantity,
                'calories': calories * quantity,
                'protein': protein * quantity,
                'carbohydrates': carbs * quantity,
                'fat': fat * quantity,
                'fiber': fiber * quantity
            }
        
        # Submit button
        submitted = st.form_submit_button("🍽️ Log Meal", type="primary", use_container_width=True)
        
        if submitted and meal_data:
            # Validate
            is_valid, errors = validators.validate_meal_data(meal_data)
            
            if is_valid:
                db_module.add_meal_record(db, meal_data)
                st.success(f"✅ Meal logged successfully: {meal_data['food_name']}")
                st.balloons()
            else:
                for error in errors:
                    st.error(error)


def show_today_meals(db):
    """Display today's meals"""
    st.subheader("Today's Meals")
    
    today = date.today()
    meals = db_module.get_meals_by_date(db, today.strftime("%Y-%m-%d"))
    
    if not meals:
        st.info("No meals logged today. Log your first meal above!")
        return
    
    # Group by meal type
    meal_groups = {'breakfast': [], 'lunch': [], 'dinner': [], 'snack': []}
    
    for meal in meals:
        meal_groups[meal['meal_type']].append(meal)
    
    # Display by meal type
    for meal_type, meal_list in meal_groups.items():
        if meal_list:
            st.markdown(f"### {meal_type.capitalize()}")
            
            for meal in meal_list:
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    
                    with col1:
                        st.markdown(f"**{meal['food_name']}**")
                        st.caption(f"{meal['serving_size']}")
                    
                    with col2:
                        st.write(f"🔥 {meal['calories']:.0f} cal")
                        st.caption(f"P: {meal['protein']:.1f}g | C: {meal['carbohydrates']:.1f}g | F: {meal['fat']:.1f}g")
                    
                    with col3:
                        if st.button("🗑️", key=f"delete_{meal['id']}", help="Delete meal"):
                            db_module.delete_meal_record(db, meal['id'])
                            st.success("Meal deleted")
                            st.rerun()
                
                st.markdown("---")
    
    # Show daily summary
    st.subheader("Daily Summary")
    summary = db_module.get_daily_nutrition_summary(db, today.strftime("%Y-%m-%d"))
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Calories", f"{summary['total_calories']:.0f} kcal")
    
    with col2:
        st.metric("Protein", f"{summary['total_protein']:.1f}g")
    
    with col3:
        st.metric("Carbs", f"{summary['total_carbs']:.1f}g")
    
    with col4:
        st.metric("Fat", f"{summary['total_fat']:.1f}g")


def show_meal_history(db):
    """Display meal history with date selector"""
    st.subheader("Meal History")
    
    # Date range selector
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=date.today() - pd.Timedelta(days=7),
            max_value=date.today()
        )
    
    with col2:
        end_date = st.date_input(
            "End Date",
            value=date.today(),
            max_value=date.today()
        )
    
    if start_date > end_date:
        st.error("Start date must be before end date")
        return
    
    # Get meals in range
    meals = db_module.get_recent_meals(db, limit=1000)
    
    if not meals:
        st.info("No meal records found")
        return
    
    # Filter by date range
    filtered_meals = []
    for meal in meals:
        meal_date = datetime.strptime(meal['date'], "%Y-%m-%d").date()
        if start_date <= meal_date <= end_date:
            filtered_meals.append(meal)
    
    if not filtered_meals:
        st.info(f"No meals found between {start_date} and {end_date}")
        return
    
    st.write(f"Found {len(filtered_meals)} meals")
    
    # Display as table
    df = pd.DataFrame([dict(meal) for meal in filtered_meals])
    df = df[['date', 'meal_type', 'food_name', 'calories', 'protein', 'carbohydrates', 'fat']]
    df = df.rename(columns={
        'date': 'Date',
        'meal_type': 'Meal',
        'food_name': 'Food',
        'calories': 'Calories',
        'protein': 'Protein (g)',
        'carbohydrates': 'Carbs (g)',
        'fat': 'Fat (g)'
    })
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Export option
    st.markdown("---")
    if st.button("📥 Export to CSV", type="secondary"):
        from pathlib import Path
        
        # Create exports directory if it doesn't exist
        exports_dir = Path(__file__).parent.parent / "exports"
        exports_dir.mkdir(exist_ok=True)
        
        output_path = exports_dir / f"meal_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        if db_module.export_meal_history(db, output_path):
            st.success(f"✅ Exported to: {output_path}")
        else:
            st.error("Export failed")


def load_food_database():
    """Load food database from CSV"""
    try:
        db_path = Path(__file__).parent.parent / "data" / "food_database.csv"
        df = pd.read_csv(db_path)
        return df
    except Exception as e:
        return None
