"""
Database management module for FoodMind AI
Handles SQLite database connections, initialization, and operations
"""

import sqlite3
import os
from datetime import datetime
from pathlib import Path


class Database:
    """Database manager class for FoodMind AI"""
    
    def __init__(self, db_path=None):
        """Initialize database connection"""
        if db_path is None:
            # Use default path inside project directory
            project_root = Path(__file__).parent.parent
            db_path = project_root / "database" / "foodmind.db"
        
        self.db_path = db_path
        self.conn = None
        self.initialize_database()
    
    def get_connection(self):
        """Get database connection"""
        if self.conn is None:
            self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def initialize_database(self):
        """Create database tables if they don't exist"""
        conn = self.get_connection()
        schema_path = Path(__file__).parent / "schema.sql"
        
        try:
            # First, check if we need to migrate existing database
            cursor = conn.cursor()
            
            # Check if tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0] for row in cursor.fetchall()]
            
            if existing_tables and 'user_profile' in existing_tables:
                # Database exists, check if it needs migration
                cursor.execute("PRAGMA table_info(user_profile)")
                columns = [col[1] for col in cursor.fetchall()]
                
                if 'user_id' not in columns:
                    # Need to migrate
                    print("Migrating existing database to add user_id support...")
                    self.migrate_database(conn)
                    print("Migration complete!")
            
            # Now create/update schema
            with open(schema_path, 'r') as f:
                schema = f.read()
            
            # Execute schema (will create tables if they don't exist)
            conn.executescript(schema)
            conn.commit()
            
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise
    
    def migrate_database(self, conn):
        """Migrate existing database to add user_id columns"""
        cursor = conn.cursor()
        
        # Add user_id to each table if it doesn't exist
        tables = ['user_profile', 'meal_records', 'nutrition_goals', 'water_intake']
        
        for table in tables:
            try:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN user_id INTEGER DEFAULT 0")
                print(f"  ✅ Added user_id to {table}")
            except Exception as e:
                if "duplicate column" not in str(e).lower():
                    print(f"  ⚠️ {table}: {e}")
        
        # Create indexes
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_profile_user_id ON user_profile(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_meal_records_user_id ON meal_records(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_nutrition_goals_user_id ON nutrition_goals(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_water_intake_user_id ON water_intake(user_id)")
        except Exception as e:
            print(f"  ⚠️ Creating indexes: {e}")
        
        conn.commit()
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor
        except Exception as e:
            conn.rollback()
            raise e
    
    def fetch_one(self, query, params=None):
        """Fetch single row"""
        cursor = self.execute_query(query, params)
        return cursor.fetchone()
    
    def fetch_all(self, query, params=None):
        """Fetch all rows"""
        cursor = self.execute_query(query, params)
        return cursor.fetchall()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None


# User Profile Operations
def get_user_profile(db, user_id=0):
    """Get user profile (returns profile for specific user)"""
    query = "SELECT * FROM user_profile WHERE user_id = ? ORDER BY id DESC LIMIT 1"
    return db.fetch_one(query, (user_id,))


def create_or_update_profile(db, profile_data, user_id=0):
    """Create or update user profile"""
    existing = get_user_profile(db, user_id)
    
    if existing:
        # Update existing profile
        query = """
            UPDATE user_profile 
            SET name=?, age=?, height=?, weight=?, activity_level=?, 
                dietary_preference=?, nutrition_goal=?, updated_at=?
            WHERE user_id=?
        """
        params = (
            profile_data['name'],
            profile_data['age'],
            profile_data['height'],
            profile_data['weight'],
            profile_data['activity_level'],
            profile_data['dietary_preference'],
            profile_data['nutrition_goal'],
            datetime.now(),
            user_id
        )
    else:
        # Create new profile
        query = """
            INSERT INTO user_profile 
            (user_id, name, age, height, weight, activity_level, dietary_preference, nutrition_goal)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            user_id,
            profile_data['name'],
            profile_data['age'],
            profile_data['height'],
            profile_data['weight'],
            profile_data['activity_level'],
            profile_data['dietary_preference'],
            profile_data['nutrition_goal']
        )
    
    db.execute_query(query, params)


# Meal Records Operations
def add_meal_record(db, meal_data, user_id=0):
    """Add a meal record"""
    query = """
        INSERT INTO meal_records 
        (user_id, date, meal_type, food_name, serving_size, quantity, calories, protein, carbohydrates, fat, fiber)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        user_id,
        meal_data['date'],
        meal_data['meal_type'],
        meal_data['food_name'],
        meal_data['serving_size'],
        meal_data['quantity'],
        meal_data['calories'],
        meal_data['protein'],
        meal_data['carbohydrates'],
        meal_data['fat'],
        meal_data.get('fiber', 0)
    )
    db.execute_query(query, params)


def get_meals_by_date(db, date, user_id=0):
    """Get all meals for a specific date and user"""
    query = """
        SELECT * FROM meal_records 
        WHERE date = ? AND user_id = ?
        ORDER BY created_at DESC
    """
    return db.fetch_all(query, (date, user_id))


def get_recent_meals(db, limit=10, user_id=0):
    """Get recent meal records for a user"""
    query = """
        SELECT * FROM meal_records 
        WHERE user_id = ?
        ORDER BY date DESC, created_at DESC 
        LIMIT ?
    """
    return db.fetch_all(query, (user_id, limit))


def delete_meal_record(db, meal_id):
    """Delete a meal record"""
    query = "DELETE FROM meal_records WHERE id = ?"
    db.execute_query(query, (meal_id,))


def get_daily_nutrition_summary(db, date, user_id=0):
    """Get nutrition summary for a specific date and user"""
    query = """
        SELECT 
            COALESCE(SUM(calories), 0) as total_calories,
            COALESCE(SUM(protein), 0) as total_protein,
            COALESCE(SUM(carbohydrates), 0) as total_carbs,
            COALESCE(SUM(fat), 0) as total_fat,
            COALESCE(SUM(fiber), 0) as total_fiber,
            COUNT(*) as meal_count
        FROM meal_records 
        WHERE date = ? AND user_id = ?
    """
    return db.fetch_one(query, (date, user_id))


def get_weekly_nutrition_data(db, start_date, end_date, user_id=0):
    """Get nutrition data for a date range and user"""
    query = """
        SELECT 
            date,
            COALESCE(SUM(calories), 0) as total_calories,
            COALESCE(SUM(protein), 0) as total_protein,
            COALESCE(SUM(carbohydrates), 0) as total_carbs,
            COALESCE(SUM(fat), 0) as total_fat
        FROM meal_records 
        WHERE date BETWEEN ? AND ? AND user_id = ?
        GROUP BY date
        ORDER BY date
    """
    return db.fetch_all(query, (start_date, end_date, user_id))


# Nutrition Goals Operations
def get_nutrition_goals(db, user_id=0):
    """Get nutrition goals for user"""
    query = "SELECT * FROM nutrition_goals WHERE user_id = ? ORDER BY id DESC LIMIT 1"
    return db.fetch_one(query, (user_id,))


def save_nutrition_goals(db, goals_data, user_id=0):
    """Save or update nutrition goals"""
    existing = get_nutrition_goals(db, user_id)
    
    if existing:
        query = """
            UPDATE nutrition_goals 
            SET daily_calories=?, daily_protein=?, daily_carbs=?, 
                daily_fat=?, daily_water=?, updated_at=?
            WHERE user_id=?
        """
        params = (
            goals_data['daily_calories'],
            goals_data['daily_protein'],
            goals_data['daily_carbs'],
            goals_data['daily_fat'],
            goals_data['daily_water'],
            datetime.now(),
            user_id
        )
    else:
        query = """
            INSERT INTO nutrition_goals 
            (user_id, daily_calories, daily_protein, daily_carbs, daily_fat, daily_water)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            user_id,
            goals_data['daily_calories'],
            goals_data['daily_protein'],
            goals_data['daily_carbs'],
            goals_data['daily_fat'],
            goals_data['daily_water']
        )
    
    db.execute_query(query, params)


# Water Intake Operations
def add_water_intake(db, date, amount, user_id=0):
    """Add water intake record"""
    query = "INSERT INTO water_intake (user_id, date, amount) VALUES (?, ?, ?)"
    db.execute_query(query, (user_id, date, amount))


def get_daily_water_intake(db, date, user_id=0):
    """Get total water intake for a date and user"""
    query = """
        SELECT COALESCE(SUM(amount), 0) as total_water 
        FROM water_intake 
        WHERE date = ? AND user_id = ?
    """
    result = db.fetch_one(query, (date, user_id))
    return result['total_water'] if result else 0


# Export Operations
def export_meal_history(db, output_path, user_id=0):
    """Export all meal records to CSV for a user"""
    import pandas as pd
    
    query = """
        SELECT date, meal_type, food_name, serving_size, quantity, 
               calories, protein, carbohydrates, fat, fiber 
        FROM meal_records 
        WHERE user_id = ?
        ORDER BY date DESC, created_at DESC
    """
    meals = db.fetch_all(query, (user_id,))
    
    if meals:
        df = pd.DataFrame([dict(meal) for meal in meals])
        df.to_csv(output_path, index=False)
        return True
    return False
