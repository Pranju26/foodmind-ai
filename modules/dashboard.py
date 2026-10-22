"""
Dashboard module for FoodMind AI
Displays personalized nutrition overview and daily progress
"""

import streamlit as st
from datetime import date, timedelta
import pandas as pd
from database import db as db_module
from utils import nutrition as nutr


def show_dashboard(db):
    """Display the main dashboard"""
    st.title("🏠 Dashboard")
    
    # Get user profile
    profile = db_module.get_user_profile(db)
    
    if not profile:
        show_welcome_state()
        return
    
    # Get nutrition goals
    goals = db_module.get_nutrition_goals(db)
    
    if not goals:
        # Calculate and save initial goals
        goals = calculate_initial_goals(db, profile)
    
    # Get today's data
    today = date.today()
    today_summary = db_module.get_daily_nutrition_summary(db, today)
    today_water = db_module.get_daily_water_intake(db, today)
    
    # Display greeting
    st.markdown(f"### Welcome back, {profile['name']}! 👋")
    st.markdown("---")
    
    # Daily overview cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        calories_consumed = today_summary['total_calories'] if today_summary else 0
        calories_goal = goals['daily_calories']
        calories_remaining = max(0, calories_goal - calories_consumed)
        
        st.metric(
            label="🔥 Calories Goal",
            value=f"{int(calories_goal)}",
            delta=f"{int(calories_remaining)} remaining"
        )
    
    with col2:
        st.metric(
            label="🍽️ Meals Logged",
            value=today_summary['meal_count'] if today_summary else 0
        )
    
    with col3:
        water_goal = goals['daily_water']
        water_percent = (today_water / water_goal * 100) if water_goal > 0 else 0
        st.metric(
            label="💧 Water Intake",
            value=f"{today_water:.1f}L / {water_goal:.1f}L",
            delta=f"{min(100, water_percent):.0f}%"
        )
    
    st.markdown("---")
    
    # Macronutrients progress
    st.subheader("📊 Today's Nutrition")
    
    macro_col1, macro_col2, macro_col3 = st.columns(3)
    
    with macro_col1:
        protein_consumed = today_summary['total_protein'] if today_summary else 0
        protein_goal = goals['daily_protein']
        protein_percent = min(100, (protein_consumed / protein_goal * 100)) if protein_goal > 0 else 0
        
        st.markdown("**Protein**")
        st.progress(protein_percent / 100)
        st.write(f"{protein_consumed:.1f}g / {protein_goal:.1f}g")
    
    with macro_col2:
        carbs_consumed = today_summary['total_carbs'] if today_summary else 0
        carbs_goal = goals['daily_carbs']
        carbs_percent = min(100, (carbs_consumed / carbs_goal * 100)) if carbs_goal > 0 else 0
        
        st.markdown("**Carbohydrates**")
        st.progress(carbs_percent / 100)
        st.write(f"{carbs_consumed:.1f}g / {carbs_goal:.1f}g")
    
    with macro_col3:
        fat_consumed = today_summary['total_fat'] if today_summary else 0
        fat_goal = goals['daily_fat']
        fat_percent = min(100, (fat_consumed / fat_goal * 100)) if fat_goal > 0 else 0
        
        st.markdown("**Fat**")
        st.progress(fat_percent / 100)
        st.write(f"{fat_consumed:.1f}g / {fat_goal:.1f}g")
    
    st.markdown("---")
    
    # Recent meals
    st.subheader("🍴 Recent Meals")
    recent_meals = db_module.get_recent_meals(db, limit=5)
    
    if recent_meals:
        for meal in recent_meals:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                
                with col1:
                    st.write(f"**{meal['food_name']}**")
                
                with col2:
                    st.write(f"{meal['meal_type'].capitalize()}")
                
                with col3:
                    st.write(f"{meal['calories']:.0f} cal")
                
                with col4:
                    st.write(meal['date'])
        
        st.markdown("") # Add spacing
        if st.button("📋 View All Meals", type="primary", use_container_width=True):
            st.session_state.page = "Meal Tracking"
            st.rerun()
    else:
        st.info("No meals logged yet. Start by logging your first meal!")
    
    st.markdown("---")
    
    # Weekly calorie trends
    st.subheader("📈 Weekly Calorie Trends")
    show_weekly_trends(db, goals['daily_calories'])
    
    # Quick actions
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    st.markdown("") # Add spacing
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("🍽️ Log Food", use_container_width=True, type="primary"):
            st.session_state.page = "Meal Tracking"
            st.rerun()
    
    with action_col2:
        if st.button("🔍 Analyze Food", use_container_width=True, type="primary"):
            st.session_state.page = "Food Analysis"
            st.rerun()
    
    with action_col3:
        if st.button("💧 Log Water", use_container_width=True, type="primary"):
            log_water_intake(db, today)


def show_welcome_state():
    """Show welcome message for new users"""
    st.markdown("""
    ## Welcome to FoodMind AI! 🎉
    
    Your AI-powered nutrition companion for tracking food intake, 
    analyzing nutritional values, and achieving your health goals.
    
    ### Get Started:
    1. **Set up your profile** - Tell us about yourself
    2. **Log your meals** - Track what you eat
    3. **View insights** - See your nutrition progress
    4. **Get AI guidance** - Ask nutrition questions
    
    """)
    
    st.info("👉 Navigate to **Profile & Goals** in the sidebar to create your profile and start your nutrition journey!")
    
    if st.button("Go to Profile Setup", type="primary"):
        st.session_state.page = "Profile & Goals"
        st.rerun()


def calculate_initial_goals(db, profile):
    """Calculate and save initial nutrition goals based on profile"""
    # Calculate BMR
    bmr = nutr.calculate_bmr(
        profile['weight'],
        profile['height'],
        profile['age'],
        'male'  # Default, can be enhanced
    )
    
    # Calculate TDEE
    tdee = nutr.calculate_tdee(bmr, profile['activity_level'])
    
    # Calculate calorie target
    calorie_target = nutr.calculate_calorie_target(tdee, profile['nutrition_goal'])
    
    # Calculate macronutrient targets
    macros = nutr.calculate_macronutrient_targets(calorie_target, profile['nutrition_goal'])
    
    # Calculate water target
    water_target = nutr.calculate_water_target(profile['weight'], profile['activity_level'])
    
    # Save goals
    goals_data = {
        'daily_calories': calorie_target,
        'daily_protein': macros['protein'],
        'daily_carbs': macros['carbs'],
        'daily_fat': macros['fat'],
        'daily_water': water_target
    }
    
    db_module.save_nutrition_goals(db, goals_data)
    
    # Fetch and return saved goals
    return db_module.get_nutrition_goals(db)


def show_weekly_trends(db, daily_calorie_goal):
    """Display weekly calorie trends chart"""
    import matplotlib.pyplot as plt
    
    # Get data for last 7 days
    end_date = date.today()
    start_date = end_date - timedelta(days=6)
    
    weekly_data = db_module.get_weekly_nutrition_data(db, start_date, end_date)
    
    if not weekly_data:
        st.info("Log meals for at least one day to see trends")
        return
    
    # Prepare data
    dates = []
    calories = []
    
    # Create full date range
    for i in range(7):
        current_date = start_date + timedelta(days=i)
        dates.append(current_date.strftime("%a"))
        
        # Find data for this date
        date_str = current_date.strftime("%Y-%m-%d")
        found = False
        for record in weekly_data:
            if record['date'] == date_str:
                calories.append(record['total_calories'])
                found = True
                break
        
        if not found:
            calories.append(0)
    
    # Create chart
    fig, ax = plt.subplots(figsize=(10, 4))
    
    bars = ax.bar(dates, calories, color='#2d6a4f', alpha=0.8)
    ax.axhline(y=daily_calorie_goal, color='#d62828', linestyle='--', 
               linewidth=2, label=f'Goal: {daily_calorie_goal:.0f} cal')
    
    ax.set_ylabel('Calories', fontsize=12)
    ax.set_xlabel('Day', fontsize=12)
    ax.set_title('Weekly Calorie Intake', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=9)
    
    st.pyplot(fig)
    plt.close()


def log_water_intake(db, date_value):
    """Quick water logging"""
    with st.form("water_form"):
        st.subheader("💧 Log Water Intake")
        
        amount = st.number_input(
            "Amount (liters)",
            min_value=0.1,
            max_value=5.0,
            value=0.25,
            step=0.25
        )
        
        submitted = st.form_submit_button("Log Water")
        
        if submitted:
            db_module.add_water_intake(db, date_value, amount)
            st.success(f"✅ Logged {amount}L of water!")
            st.rerun()
