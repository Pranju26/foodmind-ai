"""
Unit tests for database operations
Tests database initialization, CRUD operations, and data integrity
"""

import pytest
import sys
from pathlib import Path
from datetime import date
import tempfile
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db import Database
from database import db as db_module


@pytest.fixture
def test_db():
    """Create a temporary database for testing"""
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db')
    temp_file.close()
    
    # Create database instance
    db = Database(db_path=temp_file.name)
    
    yield db
    
    # Cleanup
    db.close()
    try:
        os.unlink(temp_file.name)
    except:
        pass


class TestDatabaseInitialization:
    """Test database initialization"""
    
    def test_database_creation(self, test_db):
        """Test that database is created successfully"""
        assert test_db is not None
        assert test_db.conn is not None
    
    def test_tables_exist(self, test_db):
        """Test that all required tables are created"""
        cursor = test_db.get_connection().cursor()
        
        # Check for required tables
        tables = ['user_profile', 'meal_records', 'nutrition_goals', 'water_intake']
        
        for table in tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            result = cursor.fetchone()
            assert result is not None, f"Table {table} does not exist"


class TestProfileOperations:
    """Test user profile operations"""
    
    def test_create_profile(self, test_db):
        """Test creating a user profile"""
        profile_data = {
            'name': 'Test User',
            'age': 30,
            'height': 175.0,
            'weight': 70.0,
            'activity_level': 'moderately_active',
            'dietary_preference': 'vegetarian',
            'nutrition_goal': 'maintain'
        }
        
        db_module.create_or_update_profile(test_db, profile_data)
        
        # Retrieve profile
        profile = db_module.get_user_profile(test_db)
        
        assert profile is not None
        assert profile['name'] == 'Test User'
        assert profile['age'] == 30
        assert profile['weight'] == 70.0
    
    def test_update_profile(self, test_db):
        """Test updating an existing profile"""
        # Create initial profile
        profile_data = {
            'name': 'Test User',
            'age': 30,
            'height': 175.0,
            'weight': 70.0,
            'activity_level': 'moderately_active',
            'dietary_preference': 'vegetarian',
            'nutrition_goal': 'maintain'
        }
        db_module.create_or_update_profile(test_db, profile_data)
        
        # Update profile
        profile_data['weight'] = 72.0
        profile_data['nutrition_goal'] = 'lose'
        db_module.create_or_update_profile(test_db, profile_data)
        
        # Verify update
        profile = db_module.get_user_profile(test_db)
        assert profile['weight'] == 72.0
        assert profile['nutrition_goal'] == 'lose'


class TestMealOperations:
    """Test meal record operations"""
    
    def test_add_meal(self, test_db):
        """Test adding a meal record"""
        meal_data = {
            'date': '2024-01-15',
            'meal_type': 'breakfast',
            'food_name': 'Oatmeal',
            'serving_size': '1 cup',
            'quantity': 1.0,
            'calories': 150,
            'protein': 5.0,
            'carbohydrates': 27.0,
            'fat': 3.0,
            'fiber': 4.0
        }
        
        db_module.add_meal_record(test_db, meal_data)
        
        # Retrieve meals
        meals = db_module.get_meals_by_date(test_db, '2024-01-15')
        
        assert len(meals) == 1
        assert meals[0]['food_name'] == 'Oatmeal'
        assert meals[0]['calories'] == 150
    
    def test_delete_meal(self, test_db):
        """Test deleting a meal record"""
        # Add a meal
        meal_data = {
            'date': '2024-01-15',
            'meal_type': 'lunch',
            'food_name': 'Rice',
            'serving_size': '1 cup',
            'quantity': 1.0,
            'calories': 200,
            'protein': 4.0,
            'carbohydrates': 45.0,
            'fat': 0.5,
            'fiber': 1.0
        }
        db_module.add_meal_record(test_db, meal_data)
        
        # Get the meal ID
        meals = db_module.get_meals_by_date(test_db, '2024-01-15')
        meal_id = meals[0]['id']
        
        # Delete the meal
        db_module.delete_meal_record(test_db, meal_id)
        
        # Verify deletion
        meals = db_module.get_meals_by_date(test_db, '2024-01-15')
        assert len(meals) == 0
    
    def test_daily_summary(self, test_db):
        """Test daily nutrition summary"""
        # Add multiple meals
        meals = [
            {
                'date': '2024-01-15',
                'meal_type': 'breakfast',
                'food_name': 'Eggs',
                'serving_size': '2 eggs',
                'quantity': 1.0,
                'calories': 150,
                'protein': 12.0,
                'carbohydrates': 1.0,
                'fat': 10.0,
                'fiber': 0.0
            },
            {
                'date': '2024-01-15',
                'meal_type': 'lunch',
                'food_name': 'Chicken',
                'serving_size': '100g',
                'quantity': 1.0,
                'calories': 165,
                'protein': 31.0,
                'carbohydrates': 0.0,
                'fat': 3.6,
                'fiber': 0.0
            }
        ]
        
        for meal in meals:
            db_module.add_meal_record(test_db, meal)
        
        # Get summary
        summary = db_module.get_daily_nutrition_summary(test_db, '2024-01-15')
        
        assert summary['total_calories'] == 315
        assert summary['total_protein'] == 43.0
        assert summary['meal_count'] == 2


class TestNutritionGoals:
    """Test nutrition goals operations"""
    
    def test_save_goals(self, test_db):
        """Test saving nutrition goals"""
        goals_data = {
            'daily_calories': 2000,
            'daily_protein': 150,
            'daily_carbs': 250,
            'daily_fat': 67,
            'daily_water': 2.5
        }
        
        db_module.save_nutrition_goals(test_db, goals_data)
        
        # Retrieve goals
        goals = db_module.get_nutrition_goals(test_db)
        
        assert goals is not None
        assert goals['daily_calories'] == 2000
        assert goals['daily_protein'] == 150


class TestWaterIntake:
    """Test water intake operations"""
    
    def test_log_water(self, test_db):
        """Test logging water intake"""
        today = date.today().strftime("%Y-%m-%d")
        
        db_module.add_water_intake(test_db, today, 0.5)
        db_module.add_water_intake(test_db, today, 0.75)
        
        # Get total
        total = db_module.get_daily_water_intake(test_db, today)
        
        assert total == 1.25


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
