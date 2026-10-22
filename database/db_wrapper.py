"""
Database wrapper with automatic user_id injection
"""

from utils.session import get_current_user_id


def wrap_db_functions(db_module):
    """Wrap database functions to automatically inject user_id"""
    
    def get_user_profile(db):
        user_id = get_current_user_id()
        return db_module.get_user_profile(db, user_id)
    
    def create_or_update_profile(db, profile_data):
        user_id = get_current_user_id()
        return db_module.create_or_update_profile(db, profile_data, user_id)
    
    def add_meal_record(db, meal_data):
        user_id = get_current_user_id()
        return db_module.add_meal_record(db, meal_data, user_id)
    
    def get_meals_by_date(db, date):
        user_id = get_current_user_id()
        return db_module.get_meals_by_date(db, date, user_id)
    
    def get_recent_meals(db, limit=10):
        user_id = get_current_user_id()
        return db_module.get_recent_meals(db, limit, user_id)
    
    def get_daily_nutrition_summary(db, date):
        user_id = get_current_user_id()
        return db_module.get_daily_nutrition_summary(db, date, user_id)
    
    def get_weekly_nutrition_data(db, start_date, end_date):
        user_id = get_current_user_id()
        return db_module.get_weekly_nutrition_data(db, start_date, end_date, user_id)
    
    def get_nutrition_goals(db):
        user_id = get_current_user_id()
        return db_module.get_nutrition_goals(db, user_id)
    
    def save_nutrition_goals(db, goals_data):
        user_id = get_current_user_id()
        return db_module.save_nutrition_goals(db, goals_data, user_id)
    
    def add_water_intake(db, date, amount):
        user_id = get_current_user_id()
        return db_module.add_water_intake(db, date, amount, user_id)
    
    def get_daily_water_intake(db, date):
        user_id = get_current_user_id()
        return db_module.get_daily_water_intake(db, date, user_id)
    
    def export_meal_history(db, output_path):
        user_id = get_current_user_id()
        return db_module.export_meal_history(db, output_path, user_id)
    
    # Return wrapped functions
    return {
        'get_user_profile': get_user_profile,
        'create_or_update_profile': create_or_update_profile,
        'add_meal_record': add_meal_record,
        'get_meals_by_date': get_meals_by_date,
        'get_recent_meals': get_recent_meals,
        'delete_meal_record': db_module.delete_meal_record,  # No user_id needed
        'get_daily_nutrition_summary': get_daily_nutrition_summary,
        'get_weekly_nutrition_data': get_weekly_nutrition_data,
        'get_nutrition_goals': get_nutrition_goals,
        'save_nutrition_goals': save_nutrition_goals,
        'add_water_intake': add_water_intake,
        'get_daily_water_intake': get_daily_water_intake,
        'export_meal_history': export_meal_history
    }
