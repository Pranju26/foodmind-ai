-- FoodMind AI Database Schema
-- Multi-user support with user_id

-- User Profile Table
CREATE TABLE IF NOT EXISTS user_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER DEFAULT 0,
    name TEXT NOT NULL,
    age INTEGER,
    height REAL,
    weight REAL,
    activity_level TEXT,
    dietary_preference TEXT,
    nutrition_goal TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Meal Records Table
CREATE TABLE IF NOT EXISTS meal_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER DEFAULT 0,
    date DATE NOT NULL,
    meal_type TEXT NOT NULL,
    food_name TEXT NOT NULL,
    serving_size TEXT,
    quantity REAL NOT NULL DEFAULT 1.0,
    calories REAL,
    protein REAL,
    carbohydrates REAL,
    fat REAL,
    fiber REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Nutrition Goals Table
CREATE TABLE IF NOT EXISTS nutrition_goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER DEFAULT 0,
    daily_calories REAL,
    daily_protein REAL,
    daily_carbs REAL,
    daily_fat REAL,
    daily_water REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Water Intake Table
CREATE TABLE IF NOT EXISTS water_intake (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER DEFAULT 0,
    date DATE NOT NULL,
    amount REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_user_profile_user_id ON user_profile(user_id);
CREATE INDEX IF NOT EXISTS idx_meal_records_user_id ON meal_records(user_id);
CREATE INDEX IF NOT EXISTS idx_meal_records_date ON meal_records(date);
CREATE INDEX IF NOT EXISTS idx_meal_records_meal_type ON meal_records(meal_type);
CREATE INDEX IF NOT EXISTS idx_nutrition_goals_user_id ON nutrition_goals(user_id);
CREATE INDEX IF NOT EXISTS idx_water_intake_user_id ON water_intake(user_id);
CREATE INDEX IF NOT EXISTS idx_water_intake_date ON water_intake(date);
