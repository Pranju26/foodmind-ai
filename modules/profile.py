"""
Profile and goals module for FoodMind AI
Allows users to manage their profile and nutrition goals
"""

import streamlit as st
from database import db as db_module
from utils import validators, nutrition as nutr


def show_profile_and_goals(db):
    """Display profile and goals interface"""
    st.title("👤 Profile & Goals")
    
    st.markdown("""
    Manage your personal profile and nutrition goals.
    """)
    
    # Get existing profile
    profile = db_module.get_user_profile(db)
    
    # Profile form
    with st.form("profile_form"):
        st.subheader("Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Name",
                value=profile['name'] if profile else "",
                placeholder="Enter your name"
            )
            
            age = st.number_input(
                "Age (years)",
                min_value=1,
                max_value=120,
                value=profile['age'] if profile else 25
            )
            
            height = st.number_input(
                "Height (cm)",
                min_value=50.0,
                max_value=300.0,
                value=float(profile['height']) if profile else 170.0,
                step=0.1
            )
        
        with col2:
            weight = st.number_input(
                "Weight (kg)",
                min_value=20.0,
                max_value=300.0,
                value=float(profile['weight']) if profile else 70.0,
                step=0.1
            )
            
            activity_level = st.selectbox(
                "Activity Level",
                ["sedentary", "lightly_active", "moderately_active", "very_active", "extremely_active"],
                index=["sedentary", "lightly_active", "moderately_active", "very_active", "extremely_active"].index(
                    profile['activity_level']
                ) if profile else 2,
                format_func=format_activity_level
            )
            
            dietary_preference = st.selectbox(
                "Dietary Preference",
                ["vegetarian", "non_vegetarian", "vegan", "no_preference"],
                index=["vegetarian", "non_vegetarian", "vegan", "no_preference"].index(
                    profile['dietary_preference']
                ) if profile and profile['dietary_preference'] in ["vegetarian", "non_vegetarian", "vegan", "no_preference"] else 3,
                format_func=lambda x: x.replace("_", " ").title()
            )
        
        st.markdown("---")
        st.subheader("Nutrition Goal")
        
        nutrition_goal = st.selectbox(
            "What is your primary goal?",
            ["maintain", "lose", "gain", "balanced"],
            index=["maintain", "lose", "gain", "balanced"].index(
                profile['nutrition_goal']
            ) if profile else 3,
            format_func=format_nutrition_goal
        )
        
        # Show goal description
        goal_descriptions = {
            "maintain": "Maintain your current weight with balanced nutrition",
            "lose": "Lose weight gradually (approximately 0.5kg per week)",
            "gain": "Gain weight gradually (approximately 0.5kg per week)",
            "balanced": "Focus on balanced nutrition without specific weight goals"
        }
        st.info(goal_descriptions[nutrition_goal])
        
        # Submit button
        submitted = st.form_submit_button("💾 Save Profile", type="primary", use_container_width=True)
        
        if submitted:
            # Prepare profile data
            profile_data = {
                'name': name,
                'age': age,
                'height': height,
                'weight': weight,
                'activity_level': activity_level,
                'dietary_preference': dietary_preference,
                'nutrition_goal': nutrition_goal
            }
            
            # Validate
            is_valid, errors = validators.validate_profile_data(profile_data)
            
            if is_valid:
                # Save profile
                db_module.create_or_update_profile(db, profile_data)
                
                # Calculate and save nutrition goals
                calculate_and_save_goals(db, profile_data)
                
                st.success("✅ Profile saved successfully!")
                st.balloons()
                st.rerun()
            else:
                for error in errors:
                    st.error(error)
    
    # Show current calculations if profile exists
    if profile:
        st.markdown("---")
        show_nutrition_calculations(profile)
        
        st.markdown("---")
        show_current_goals(db)
        
        st.markdown("---")
        show_disclaimer()


def format_activity_level(level):
    """Format activity level for display"""
    descriptions = {
        'sedentary': 'Sedentary (little or no exercise)',
        'lightly_active': 'Lightly Active (1-3 days/week)',
        'moderately_active': 'Moderately Active (3-5 days/week)',
        'very_active': 'Very Active (6-7 days/week)',
        'extremely_active': 'Extremely Active (physical job/training twice daily)'
    }
    return descriptions.get(level, level)


def format_nutrition_goal(goal):
    """Format nutrition goal for display"""
    goals = {
        'maintain': 'Maintain Weight',
        'lose': 'Lose Weight',
        'gain': 'Gain Weight',
        'balanced': 'Balanced Nutrition'
    }
    return goals.get(goal, goal)


def calculate_and_save_goals(db, profile_data):
    """Calculate nutrition goals based on profile"""
    # Calculate BMR (assuming male for simplicity; can be enhanced)
    bmr = nutr.calculate_bmr(
        profile_data['weight'],
        profile_data['height'],
        profile_data['age'],
        'male'
    )
    
    # Calculate TDEE
    tdee = nutr.calculate_tdee(bmr, profile_data['activity_level'])
    
    # Calculate calorie target
    calorie_target = nutr.calculate_calorie_target(tdee, profile_data['nutrition_goal'])
    
    # Calculate macronutrient targets
    macros = nutr.calculate_macronutrient_targets(calorie_target, profile_data['nutrition_goal'])
    
    # Calculate water target
    water_target = nutr.calculate_water_target(profile_data['weight'], profile_data['activity_level'])
    
    # Save goals
    goals_data = {
        'daily_calories': calorie_target,
        'daily_protein': macros['protein'],
        'daily_carbs': macros['carbs'],
        'daily_fat': macros['fat'],
        'daily_water': water_target
    }
    
    db_module.save_nutrition_goals(db, goals_data)


def show_nutrition_calculations(profile):
    """Display nutrition calculations"""
    st.subheader("📊 Your Nutrition Calculations")
    
    # Calculate BMI
    bmi = nutr.calculate_bmi(profile['weight'], profile['height'])
    bmi_category = nutr.get_bmi_category(bmi)
    
    # Calculate BMR
    bmr = nutr.calculate_bmr(profile['weight'], profile['height'], profile['age'])
    
    # Calculate TDEE
    tdee = nutr.calculate_tdee(bmr, profile['activity_level'])
    
    # Calculate calorie target
    calorie_target = nutr.calculate_calorie_target(tdee, profile['nutrition_goal'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("BMI", f"{bmi}")
        st.caption(bmi_category)
    
    with col2:
        st.metric("BMR", f"{bmr:.0f} cal/day")
        st.caption("Base metabolism")
    
    with col3:
        st.metric("TDEE", f"{tdee:.0f} cal/day")
        st.caption("With activity")
    
    with col4:
        st.metric("Target", f"{calorie_target:.0f} cal/day")
        st.caption("For your goal")
    
    # Show formulas used
    with st.expander("ℹ️ How are these calculated?"):
        st.markdown("""
        **BMI (Body Mass Index)**
        - Formula: weight(kg) / (height(m))²
        - Categories: Underweight (<18.5), Normal (18.5-24.9), Overweight (25-29.9), Obese (≥30)
        
        **BMR (Basal Metabolic Rate) - Mifflin-St Jeor Equation**
        - Men: 10 × weight(kg) + 6.25 × height(cm) - 5 × age + 5
        - Women: 10 × weight(kg) + 6.25 × height(cm) - 5 × age - 161
        - Represents calories burned at rest
        
        **TDEE (Total Daily Energy Expenditure)**
        - BMR × Activity Multiplier
        - Activity multipliers: Sedentary (1.2), Lightly Active (1.375), 
          Moderately Active (1.55), Very Active (1.725), Extremely Active (1.9)
        
        **Calorie Target**
        - Maintain: TDEE
        - Lose weight: TDEE - 500 (≈0.5kg/week loss)
        - Gain weight: TDEE + 500 (≈0.5kg/week gain)
        - Minimum: 1200 calories/day for safety
        """)


def show_current_goals(db):
    """Display current nutrition goals"""
    goals = db_module.get_nutrition_goals(db)
    
    if not goals:
        return
    
    st.subheader("🎯 Your Daily Nutrition Goals")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Calories", f"{goals['daily_calories']:.0f} kcal")
        st.metric("Protein", f"{goals['daily_protein']:.0f}g")
        st.metric("Carbohydrates", f"{goals['daily_carbs']:.0f}g")
    
    with col2:
        st.metric("Fat", f"{goals['daily_fat']:.0f}g")
        st.metric("Water", f"{goals['daily_water']:.1f} liters")


def show_disclaimer():
    """Show health disclaimer"""
    st.warning("""
    **⚠️ Important Notice:**
    
    FoodMind AI is an educational nutrition tracking tool. 
    
    - Calculations are estimates based on standard formulas
    - Individual needs vary based on health conditions, genetics, and lifestyle
    - This tool is NOT a substitute for professional medical or dietetic advice
    - Consult a healthcare provider or registered dietitian for personalized guidance
    - Do not use this tool if you have eating disorders or medical conditions without professional supervision
    """)
