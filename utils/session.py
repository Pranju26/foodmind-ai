"""
Session utilities for FoodMind AI
Helper functions to manage user sessions
"""

import streamlit as st


def get_current_user_id():
    """Get current user ID from session state"""
    if st.session_state.get('authenticated', False):
        return st.session_state.get('user_id', 0)
    return 0


def get_current_username():
    """Get current username from session state"""
    if st.session_state.get('authenticated', False):
        return st.session_state.get('user_username', 'Guest')
    return 'Guest'


def is_demo_mode():
    """Check if running in demo mode"""
    return get_current_user_id() == 0
