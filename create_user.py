"""
Script to create pre-registered user account for Pranjali Gadekar
"""

import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime


def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def create_pranjali_account():
    """Create pre-registered account for Pranjali Gadekar"""
    
    # User details
    username = "PranjaliGadekar"
    email = "pranjaligadekar6@gmail.com"
    full_name = "Pranjali Gadekar"
    password = "Pranjali@123"  # Default password - user can change later
    
    print("Creating account for Pranjali Gadekar...")
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print()
    
    # Hash password
    password_hash = hash_password(password)
    
    # Connect to database
    db_path = Path(__file__).parent / "database" / "users.db"
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", 
                      (username, email))
        existing = cursor.fetchone()
        
        if existing:
            print("❌ User already exists!")
            print("   Deleting existing user and creating new one...")
            cursor.execute("DELETE FROM users WHERE username = ? OR email = ?", 
                          (username, email))
        
        # Insert user
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, full_name, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, email, password_hash, full_name, datetime.now()))
        
        # Get the new user ID
        user_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        print("\n✅ Account created successfully!")
        print(f"   User ID: {user_id}")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Full Name: {full_name}")
        print(f"\n🔑 Login Credentials:")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        print(f"\n⚠️  Please share this password with Pranjali Gadekar")
        print(f"   They can change it after logging in.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error creating account: {str(e)}")
        return False


if __name__ == "__main__":
    create_pranjali_account()
