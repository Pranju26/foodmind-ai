"""
Database module for FoodMind AI
Automatically handles user_id injection for multi-user support
"""

from database import db as db_core
from database.db_wrapper import wrap_db_functions

# Export wrapped functions that auto-inject user_id
wrapped = wrap_db_functions(db_core)

get_user_profile = wrapped['get_user_profile']
create_or_update_profile = wrapped['create_or_update_profile']
add_meal_record = wrapped['add_meal_record']
get_meals_by_date = wrapped['get_meals_by_date']
get_recent_meals = wrapped['get_recent_meals']
delete_meal_record = wrapped['delete_meal_record']
get_daily_nutrition_summary = wrapped['get_daily_nutrition_summary']
get_weekly_nutrition_data = wrapped['get_weekly_nutrition_data']
get_nutrition_goals = wrapped['get_nutrition_goals']
save_nutrition_goals = wrapped['save_nutrition_goals']
add_water_intake = wrapped['add_water_intake']
get_daily_water_intake = wrapped['get_daily_water_intake']
export_meal_history = wrapped['export_meal_history']
