"""
Database migration script to add user_id support
Migrates existing database to multi-user schema
"""

import sqlite3
from pathlib import Path


def migrate_database():
    """Migrate existing database to add user_id columns"""
    
    db_path = Path(__file__).parent / "foodmind.db"
    
    if not db_path.exists():
        print("No existing database found. Will create new one with user_id support.")
        return
    
    print(f"Migrating database: {db_path}")
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # Check if user_id already exists
        cursor.execute("PRAGMA table_info(user_profile)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'user_id' in columns:
            print("✅ Database already migrated!")
            conn.close()
            return
        
        print("Adding user_id columns to tables...")
        
        # Add user_id to user_profile
        try:
            cursor.execute("ALTER TABLE user_profile ADD COLUMN user_id INTEGER DEFAULT 0")
            print("✅ Added user_id to user_profile")
        except sqlite3.OperationalError as e:
            if "duplicate column" not in str(e).lower():
                print(f"⚠️ user_profile: {e}")
        
        # Add user_id to meal_records
        try:
            cursor.execute("ALTER TABLE meal_records ADD COLUMN user_id INTEGER DEFAULT 0")
            print("✅ Added user_id to meal_records")
        except sqlite3.OperationalError as e:
            if "duplicate column" not in str(e).lower():
                print(f"⚠️ meal_records: {e}")
        
        # Add user_id to nutrition_goals
        try:
            cursor.execute("ALTER TABLE nutrition_goals ADD COLUMN user_id INTEGER DEFAULT 0")
            print("✅ Added user_id to nutrition_goals")
        except sqlite3.OperationalError as e:
            if "duplicate column" not in str(e).lower():
                print(f"⚠️ nutrition_goals: {e}")
        
        # Add user_id to water_intake
        try:
            cursor.execute("ALTER TABLE water_intake ADD COLUMN user_id INTEGER DEFAULT 0")
            print("✅ Added user_id to water_intake")
        except sqlite3.OperationalError as e:
            if "duplicate column" not in str(e).lower():
                print(f"⚠️ water_intake: {e}")
        
        # Create indexes
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_profile_user_id ON user_profile(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_meal_records_user_id ON meal_records(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_nutrition_goals_user_id ON nutrition_goals(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_water_intake_user_id ON water_intake(user_id)")
            print("✅ Created indexes")
        except Exception as e:
            print(f"⚠️ Indexes: {e}")
        
        conn.commit()
        print("\n🎉 Migration completed successfully!")
        print("📝 All existing data preserved with user_id = 0 (demo mode)")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    
    finally:
        conn.close()


if __name__ == "__main__":
    migrate_database()
