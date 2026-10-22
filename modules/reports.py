"""
Reports and visualizations module for FoodMind AI
Generates nutrition reports and charts using Matplotlib and Pandas
"""

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date, timedelta
from database import db as db_module


def show_reports(db):
    """Display nutrition reports and visualizations"""
    st.title("📊 Nutrition Reports")
    
    st.markdown("""
    Visualize your nutrition data and track your progress over time.
    """)
    
    # Check if there's data
    recent_meals = db_module.get_recent_meals(db, limit=1)
    
    if not recent_meals:
        st.info("""
        No nutrition data available yet. Start logging your meals to see reports!
        
        Reports will show:
        - Daily calorie trends
        - Macronutrient distribution
        - Weekly nutrition summary
        - Progress towards goals
        """)
        return
    
    # Date range selector
    st.subheader("📅 Select Report Period")
    
    col1, col2 = st.columns(2)
    
    with col1:
        days_back = st.selectbox(
            "Time Period",
            [7, 14, 30, 60, 90],
            format_func=lambda x: f"Last {x} days"
        )
    
    end_date = date.today()
    start_date = end_date - timedelta(days=days_back - 1)
    
    # Get data
    weekly_data = db_module.get_weekly_nutrition_data(db, start_date, end_date)
    
    if not weekly_data:
        st.warning(f"No data found for the selected period ({start_date} to {end_date})")
        return
    
    # Show reports
    st.markdown("---")
    
    # 1. Calorie Trends Chart
    show_calorie_trends_chart(weekly_data, start_date, end_date, db)
    
    st.markdown("---")
    
    # 2. Macronutrient Distribution
    show_macronutrient_distribution(weekly_data)
    
    st.markdown("---")
    
    # 3. Daily Averages
    show_daily_averages(weekly_data, db)
    
    st.markdown("---")
    
    # 4. Protein Intake Chart
    show_protein_chart(weekly_data, start_date, end_date, db)


def show_calorie_trends_chart(data, start_date, end_date, db):
    """Display calorie trends over time"""
    st.subheader("📈 Daily Calorie Trends")
    
    # Get calorie goal
    goals = db_module.get_nutrition_goals(db)
    calorie_goal = goals['daily_calories'] if goals else None
    
    # Prepare data
    dates = []
    calories = []
    
    # Create full date range
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        
        # Find data for this date
        date_str = current_date.strftime("%Y-%m-%d")
        found = False
        for record in data:
            if record['date'] == date_str:
                calories.append(record['total_calories'])
                found = True
                break
        
        if not found:
            calories.append(0)
        
        current_date += timedelta(days=1)
    
    # Create chart
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot calories
    ax.plot(dates, calories, marker='o', linewidth=2, markersize=6, 
            color='#2d6a4f', label='Daily Calories')
    
    # Plot goal line
    if calorie_goal:
        ax.axhline(y=calorie_goal, color='#d62828', linestyle='--', 
                  linewidth=2, label=f'Goal: {calorie_goal:.0f} cal')
    
    # Formatting
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Calories', fontsize=12, fontweight='bold')
    ax.set_title('Daily Calorie Intake Over Time', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    # Rotate date labels
    plt.xticks(rotation=45, ha='right')
    
    # Tight layout
    plt.tight_layout()
    
    st.pyplot(fig)
    plt.close()
    
    # Summary stats
    valid_calories = [c for c in calories if c > 0]
    if valid_calories:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Average Daily Calories", f"{sum(valid_calories) / len(valid_calories):.0f}")
        
        with col2:
            st.metric("Highest Day", f"{max(valid_calories):.0f}")
        
        with col3:
            st.metric("Days Logged", f"{len(valid_calories)}")


def show_macronutrient_distribution(data):
    """Display macronutrient distribution pie chart"""
    st.subheader("🥗 Macronutrient Distribution")
    
    # Calculate totals
    total_protein = sum(record['total_protein'] for record in data)
    total_carbs = sum(record['total_carbs'] for record in data)
    total_fat = sum(record['total_fat'] for record in data)
    
    if total_protein == 0 and total_carbs == 0 and total_fat == 0:
        st.info("Not enough data for macronutrient distribution")
        return
    
    # Calculate calories from each macro
    protein_cal = total_protein * 4  # 4 cal/g
    carbs_cal = total_carbs * 4      # 4 cal/g
    fat_cal = total_fat * 9           # 9 cal/g
    
    total_cal = protein_cal + carbs_cal + fat_cal
    
    if total_cal == 0:
        st.info("Not enough data for macronutrient distribution")
        return
    
    # Calculate percentages
    protein_pct = (protein_cal / total_cal) * 100
    carbs_pct = (carbs_cal / total_cal) * 100
    fat_pct = (fat_cal / total_cal) * 100
    
    # Create pie chart
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sizes = [protein_pct, carbs_pct, fat_pct]
    labels = [f'Protein\n{protein_pct:.1f}%', 
             f'Carbohydrates\n{carbs_pct:.1f}%', 
             f'Fat\n{fat_pct:.1f}%']
    colors = ['#e63946', '#f77f00', '#06d6a0']
    explode = (0.05, 0.05, 0.05)
    
    ax.pie(sizes, explode=explode, labels=labels, colors=colors,
           autopct='', startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
    
    ax.set_title('Macronutrient Distribution (by calories)', 
                fontsize=14, fontweight='bold', pad=20)
    
    ax.axis('equal')
    
    st.pyplot(fig)
    plt.close()
    
    # Show actual amounts
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Protein", f"{total_protein:.1f}g")
    
    with col2:
        st.metric("Total Carbohydrates", f"{total_carbs:.1f}g")
    
    with col3:
        st.metric("Total Fat", f"{total_fat:.1f}g")


def show_daily_averages(data, db):
    """Display daily nutrition averages"""
    st.subheader("📊 Daily Averages")
    
    # Calculate averages
    days_with_data = len([d for d in data if d['total_calories'] > 0])
    
    if days_with_data == 0:
        st.info("Not enough data for daily averages")
        return
    
    avg_calories = sum(d['total_calories'] for d in data) / days_with_data
    avg_protein = sum(d['total_protein'] for d in data) / days_with_data
    avg_carbs = sum(d['total_carbs'] for d in data) / days_with_data
    avg_fat = sum(d['total_fat'] for d in data) / days_with_data
    
    # Get goals
    goals = db_module.get_nutrition_goals(db)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        goal_val = goals['daily_calories'] if goals else None
        delta = f"{avg_calories - goal_val:.0f}" if goal_val else None
        st.metric("Avg Calories", f"{avg_calories:.0f} kcal", delta=delta)
    
    with col2:
        goal_val = goals['daily_protein'] if goals else None
        delta = f"{avg_protein - goal_val:.1f}g" if goal_val else None
        st.metric("Avg Protein", f"{avg_protein:.1f}g", delta=delta)
    
    with col3:
        goal_val = goals['daily_carbs'] if goals else None
        delta = f"{avg_carbs - goal_val:.1f}g" if goal_val else None
        st.metric("Avg Carbs", f"{avg_carbs:.1f}g", delta=delta)
    
    with col4:
        goal_val = goals['daily_fat'] if goals else None
        delta = f"{avg_fat - goal_val:.1f}g" if goal_val else None
        st.metric("Avg Fat", f"{avg_fat:.1f}g", delta=delta)
    
    st.caption(f"Based on {days_with_data} days with recorded meals")


def show_protein_chart(data, start_date, end_date, db):
    """Display protein intake chart"""
    st.subheader("💪 Protein Intake Tracking")
    
    # Get protein goal
    goals = db_module.get_nutrition_goals(db)
    protein_goal = goals['daily_protein'] if goals else None
    
    # Prepare data
    dates = []
    protein_values = []
    
    # Create full date range
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        
        # Find data for this date
        date_str = current_date.strftime("%Y-%m-%d")
        found = False
        for record in data:
            if record['date'] == date_str:
                protein_values.append(record['total_protein'])
                found = True
                break
        
        if not found:
            protein_values.append(0)
        
        current_date += timedelta(days=1)
    
    # Create chart
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot protein
    bars = ax.bar(dates, protein_values, color='#e63946', alpha=0.7, label='Daily Protein')
    
    # Plot goal line
    if protein_goal:
        ax.axhline(y=protein_goal, color='#2d6a4f', linestyle='--', 
                  linewidth=2, label=f'Goal: {protein_goal:.0f}g')
    
    # Formatting
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Protein (grams)', fontsize=12, fontweight='bold')
    ax.set_title('Daily Protein Intake', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.3)
    
    # Rotate date labels
    plt.xticks(rotation=45, ha='right')
    
    # Tight layout
    plt.tight_layout()
    
    st.pyplot(fig)
    plt.close()
