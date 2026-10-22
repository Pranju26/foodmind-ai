"""
Authentication module for FoodMind AI
Handles user login, registration, and session management
"""

import streamlit as st
import hashlib
import sqlite3
from pathlib import Path
from datetime import datetime
import re


def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    if not any(c.isalpha() for c in password):
        return False, "Password must contain at least one letter"
    return True, "Password is valid"


def init_auth_db():
    """Initialize authentication database"""
    db_path = Path(__file__).parent.parent / "database" / "users.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def register_user(username, email, password, full_name):
    """Register a new user"""
    try:
        # Validate inputs
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if not validate_email(email):
            return False, "Invalid email format"
        
        is_valid, msg = validate_password(password)
        if not is_valid:
            return False, msg
        
        # Hash password
        password_hash = hash_password(password)
        
        # Insert into database
        db_path = Path(__file__).parent.parent / "database" / "users.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, full_name))
            
            conn.commit()
            conn.close()
            return True, "Registration successful!"
        
        except sqlite3.IntegrityError:
            conn.close()
            return False, "Username or email already exists"
    
    except Exception as e:
        return False, f"Error during registration: {str(e)}"


def login_user(username, password):
    """Authenticate user login"""
    try:
        password_hash = hash_password(password)
        
        db_path = Path(__file__).parent.parent / "database" / "users.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check credentials
        cursor.execute('''
            SELECT id, username, email, full_name
            FROM users
            WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        
        user = cursor.fetchone()
        
        if user:
            # Update last login
            cursor.execute('''
                UPDATE users
                SET last_login = ?
                WHERE id = ?
            ''', (datetime.now(), user[0]))
            
            conn.commit()
            conn.close()
            
            # Return user data
            return True, {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'full_name': user[3]
            }
        else:
            conn.close()
            return False, "Invalid username or password"
    
    except Exception as e:
        return False, f"Error during login: {str(e)}"


def logout_user():
    """Logout current user"""
    for key in list(st.session_state.keys()):
        if key.startswith('user_') or key == 'authenticated':
            del st.session_state[key]


def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)


def get_current_user():
    """Get current logged in user"""
    if is_authenticated():
        return {
            'id': st.session_state.get('user_id'),
            'username': st.session_state.get('user_username'),
            'email': st.session_state.get('user_email'),
            'full_name': st.session_state.get('user_full_name')
        }
    return None


def show_login_page():
    """Display login page"""
    # Use white text for dark mode compatibility
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='color: #ffffff; font-size: 3rem;'>🥗 FoodMind AI</h1>
            <p style='color: #ffffff; font-size: 1.2rem; opacity: 0.9;'>Your AI-Powered Nutrition Companion</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for Login and Register
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        show_login_form()
    
    with tab2:
        show_register_form()


def show_login_form():
    """Display login form"""
    st.subheader("Welcome Back!")
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        
        with col1:
            submit = st.form_submit_button("🔓 Login", use_container_width=True, type="primary")
        
        with col2:
            demo = st.form_submit_button("👤 Demo Mode", use_container_width=True)
        
        if submit:
            if not username or not password:
                st.error("Please enter both username and password")
            else:
                success, result = login_user(username, password)
                
                if success:
                    # Set session state
                    st.session_state.authenticated = True
                    st.session_state.user_id = result['id']
                    st.session_state.user_username = result['username']
                    st.session_state.user_email = result['email']
                    st.session_state.user_full_name = result['full_name']
                    
                    st.success(f"Welcome back, {result['full_name'] or result['username']}!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(result)
        
        if demo:
            # Demo mode - skip authentication
            st.session_state.authenticated = True
            st.session_state.user_id = 0
            st.session_state.user_username = "demo_user"
            st.session_state.user_email = "demo@foodmind.ai"
            st.session_state.user_full_name = "Demo User"
            
            st.info("Logged in as Demo User. Your data won't be saved permanently.")
            st.rerun()


def show_register_form():
    """Display registration form"""
    st.subheader("Create Your Account")
    
    with st.form("register_form"):
        full_name = st.text_input("Full Name", placeholder="Enter your full name")
        username = st.text_input("Username", placeholder="Choose a username (min 3 characters)")
        email = st.text_input("Email", placeholder="your.email@example.com")
        
        col1, col2 = st.columns(2)
        
        with col1:
            password = st.text_input("Password", type="password", placeholder="Min 6 characters")
        
        with col2:
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
        
        st.markdown("**Password Requirements:**")
        st.caption("• At least 6 characters\n• Contains letters and numbers")
        
        agree = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        
        submit = st.form_submit_button("🚀 Create Account", use_container_width=True, type="primary")
        
        if submit:
            if not all([full_name, username, email, password, confirm_password]):
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif not agree:
                st.error("Please agree to the Terms of Service")
            else:
                success, message = register_user(username, email, password, full_name)
                
                if success:
                    st.success(message)
                    st.balloons()
                    st.info("✅ Account created! Please login with your credentials.")
                else:
                    st.error(message)


def show_user_profile_card():
    """Show user profile card in sidebar - at top, logout at bottom"""
    if is_authenticated():
        user = get_current_user()
        
        with st.sidebar:
            # Show profile card at current position (will be at top via main())
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, rgb(67, 160, 71) 0%, rgb(56, 142, 60) 100%); 
                            padding: 1rem; border-radius: 10px; text-align: center; margin-bottom: 1rem;'>
                    <h3 style='color: white; margin: 0;'>👤 {user['full_name'] or user['username']}</h3>
                    <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 0.9rem;'>
                        @{user['username']}
                    </p>
                </div>
            """, unsafe_allow_html=True)


def show_logout_button():
    """Show logout button at the bottom of sidebar"""
    if is_authenticated():
        with st.sidebar:
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
                logout_user()
                st.success("Logged out successfully!")
                st.rerun()


def require_auth(func):
    """Decorator to require authentication"""
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            show_login_page()
            return None
        return func(*args, **kwargs)
    return wrapper


# Initialize database on import
init_auth_db()
