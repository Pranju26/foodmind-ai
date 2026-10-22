"""
FoodMind AI - AI-Powered Nutrition Tracking Application
Main Streamlit application file
"""

import streamlit as st
from pathlib import Path
import sys

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import database
from database.db import Database

# Import modules
from modules import (
    dashboard,
    food_analysis,
    meal_tracking,
    ai_assistant,
    profile,
    reports,
    auth
)


# Page configuration
st.set_page_config(
    page_title="FoodMind AI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for styling
def load_custom_css():
    """Load custom CSS with professional RGB color scheme and optimal readability"""
    st.markdown("""
    <style>
    /* Professional Color Palette - Official Material Design Colors */
    :root {
        /* Primary Brand Colors */
        --primary-blue: rgb(25, 118, 210);        /* Deep Blue */
        --primary-blue-light: rgb(66, 165, 245);  /* Light Blue */
        --primary-blue-dark: rgb(13, 71, 161);    /* Dark Blue */
        
        --accent-green: rgb(67, 160, 71);         /* Success Green */
        --accent-orange: rgb(251, 140, 0);        /* Warm Orange */
        --accent-purple: rgb(142, 36, 170);       /* Rich Purple */
        
        /* Background Colors */
        --bg-main: rgb(248, 249, 250);
        --bg-card: rgb(255, 255, 255);
        --bg-sidebar: linear-gradient(180deg, rgb(25, 118, 210) 0%, rgb(13, 71, 161) 100%);
        
        /* Text Colors - High Contrast */
        --text-primary: rgb(33, 33, 33);
        --text-secondary: rgb(66, 66, 66);
        --text-muted: rgb(117, 117, 117);
        --text-white: rgb(255, 255, 255);
        
        /* Status Colors */
        --success: rgb(67, 160, 71);
        --warning: rgb(251, 140, 0);
        --error: rgb(229, 57, 53);
        --info: rgb(25, 118, 210);
    }
    
    /* Hide Streamlit branding and header */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hide Streamlit toolbar */
    .stDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}
    
    /* Remove header padding */
    .main > div:first-child {
        padding-top: 0rem;
    }
    
    /* Remove top padding from app */
    .block-container {
        padding-top: 1rem;
    }
    
    /* Main App Background */
    [data-testid="stAppViewContainer"] {
        background: rgb(248, 249, 250);
    }
    
    .main .block-container {
        background: transparent;
        padding: 2rem 1rem;
    }
    
    /* Sidebar - Professional Blue Gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, 
            rgb(25, 118, 210) 0%, 
            rgb(13, 71, 161) 100%) !important;
    }
    
    /* Sidebar Text - White for high contrast on blue */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown *,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMetric label,
    [data-testid="stSidebar"] .stMetric [data-testid="stMetricValue"] {
        color: rgb(255, 255, 255) !important;
    }
    
    /* Sidebar Divider */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    /* Navigation Buttons - FIXED for better visibility */
    .stButton > button {
        background: rgba(255, 255, 255, 0.15) !important;
        color: rgb(255, 255, 255) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
        color: rgb(255, 255, 255) !important;
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Primary Button (Active Nav) - FIXED to prevent white-on-white */
    .stButton > button[kind="primary"] {
        background: rgb(255, 255, 255) !important;
        color: rgb(25, 118, 210) !important;
        border-color: rgb(255, 255, 255) !important;
        font-weight: 700;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: rgb(255, 255, 255) !important;
        color: rgb(13, 71, 161) !important;
        border-color: rgb(255, 255, 255) !important;
    }
    
    /* Force button text to always be visible */
    .stButton > button *,
    .stButton > button span,
    .stButton > button p,
    .stButton > button div {
        color: inherit !important;
    }
    
    /* Sidebar buttons specifically */
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255, 255, 255, 0.15) !important;
        color: rgb(255, 255, 255) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: rgb(255, 255, 255) !important;
        color: rgb(25, 118, 210) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button[kind="primary"] * {
        color: rgb(25, 118, 210) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:not([kind="primary"]) * {
        color: rgb(255, 255, 255) !important;
    }
    
    /* Main content buttons - make them visible */
    .main .stButton > button {
        background: rgb(25, 118, 210) !important;
        color: rgb(255, 255, 255) !important;
        border: 2px solid rgb(25, 118, 210) !important;
        font-weight: 600 !important;
    }
    
    .main .stButton > button:hover {
        background: rgb(13, 71, 161) !important;
        border-color: rgb(13, 71, 161) !important;
    }
    
    .main .stButton > button[kind="primary"] {
        background: rgb(25, 118, 210) !important;
        color: rgb(255, 255, 255) !important;
    }
    
    .main .stButton > button[kind="primary"] * {
        color: rgb(255, 255, 255) !important;
    }
    
    .main .stButton > button[kind="secondary"] {
        background: rgb(255, 255, 255) !important;
        color: rgb(25, 118, 210) !important;
        border: 2px solid rgb(25, 118, 210) !important;
    }
    
    .main .stButton > button[kind="secondary"]:hover {
        background: rgb(25, 118, 210) !important;
        color: rgb(255, 255, 255) !important;
    }
    
    /* Main Content Headers - High Contrast */
    h1 {
        color: rgb(25, 118, 210);
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        line-height: 1.2;
    }
    
    h2 {
        color: rgb(33, 33, 33);
        font-weight: 700;
        font-size: 1.75rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: rgb(66, 66, 66);
        font-weight: 600;
        font-size: 1.25rem;
        margin-bottom: 0.75rem;
    }
    
    /* Body Text - High Contrast */
    .stMarkdown p,
    .stMarkdown div,
    .stMarkdown span,
    .stMarkdown li {
        color: rgb(33, 33, 33) !important;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    /* Force all main content text to be dark */
    .main p,
    .main span,
    .main div:not([data-testid="stSidebar"]),
    .main label,
    .main li {
        color: rgb(33, 33, 33) !important;
    }
    
    /* Ensure white text only in sidebar */
    [data-testid="stAppViewContainer"] > .main * {
        color: rgb(33, 33, 33);
    }
    
    /* Keep sidebar white text */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] * {
        color: rgb(255, 255, 255) !important;
    }
    
    /* Metric Cards - White Background with Colored Accents */
    .stMetric {
        background: rgb(255, 255, 255);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid rgb(25, 118, 210);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(25, 118, 210, 0.15);
    }
    
    .stMetric label {
        color: rgb(117, 117, 117) !important;
        font-weight: 600;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: rgb(25, 118, 210) !important;
        font-weight: 700;
        font-size: 2.25rem;
    }
    
    .stMetric [data-testid="stMetricDelta"] {
        color: rgb(67, 160, 71) !important;
        font-weight: 600;
    }
    
    /* Form Inputs - Clean Design with WHITE background */
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea,
    .stSelectbox select,
    .stDateInput input,
    .stTimeInput input,
    input,
    textarea,
    select {
        border: 2px solid rgb(224, 224, 224) !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        color: rgb(33, 33, 33) !important;
        background: rgb(255, 255, 255) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stTextArea textarea:focus,
    .stSelectbox select:focus,
    .stDateInput input:focus,
    .stTimeInput input:focus,
    input:focus,
    textarea:focus,
    select:focus {
        border-color: rgb(189, 189, 189) !important;
        box-shadow: none !important;
        outline: none !important;
        background: rgb(248, 249, 250) !important;
        color: rgb(33, 33, 33) !important;
    }
    
    /* Input placeholder text */
    input::placeholder,
    textarea::placeholder {
        color: rgb(158, 158, 158) !important;
    }
    
    /* Password eye icon - grey color */
    .stTextInput button,
    [data-testid="baseButton-secondary"] {
        background: transparent !important;
        color: rgb(117, 117, 117) !important;
        border: none !important;
    }
    
    .stTextInput button:hover {
        background: rgba(117, 117, 117, 0.1) !important;
        color: rgb(33, 33, 33) !important;
    }
    
    .stTextInput svg {
        fill: rgb(117, 117, 117) !important;
    }
    
    /* Dropdown arrow icon - grey */
    .stSelectbox svg,
    .stMultiSelect svg,
    [data-baseweb="select"] svg {
        fill: rgb(117, 117, 117) !important;
    }
    
    /* Plus/Minus buttons in number input - grey */
    .stNumberInput button,
    .stNumberInput svg {
        color: rgb(117, 117, 117) !important;
        fill: rgb(117, 117, 117) !important;
        background: transparent !important;
    }
    
    .stNumberInput button:hover {
        background: rgba(117, 117, 117, 0.1) !important;
        color: rgb(33, 33, 33) !important;
    }
    
    .stNumberInput button:hover svg {
        fill: rgb(33, 33, 33) !important;
    }
    
    /* Dropdown menu - faint grey background */
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    [role="listbox"],
    [role="option"],
    .stSelectbox div[data-baseweb="select"] > div,
    .stSelectbox [role="listbox"],
    .stMultiSelect [role="listbox"] {
        background: rgb(248, 249, 250) !important;
        color: rgb(33, 33, 33) !important;
        border: 1px solid rgb(224, 224, 224) !important;
    }
    
    /* Dropdown options */
    [role="option"],
    [data-baseweb="menu"] li,
    .stSelectbox [role="option"],
    .stMultiSelect [role="option"] {
        background: rgb(248, 249, 250) !important;
        color: rgb(33, 33, 33) !important;
    }
    
    [role="option"]:hover,
    [data-baseweb="menu"] li:hover {
        background: rgb(224, 224, 224) !important;
        color: rgb(33, 33, 33) !important;
    }
    
    /* Select box internal elements */
    .stSelectbox > div > div,
    .stSelectbox > div > div > div,
    .stMultiSelect > div > div {
        background: rgb(255, 255, 255) !important;
        color: rgb(33, 33, 33) !important;
    }
    
    /* Date picker calendar - faint grey */
    [data-baseweb="calendar"],
    .stDateInput [data-baseweb="calendar"],
    [data-baseweb="calendar"] * {
        background: rgb(248, 249, 250) !important;
        color: rgb(33, 33, 33) !important;
    }
    
    /* Date picker header */
    [data-baseweb="calendar-header"],
    [data-baseweb="calendar"] header {
        background: rgb(224, 224, 224) !important;
        color: rgb(33, 33, 33) !important;
    }
    
    /* Date cells */
    [data-baseweb="calendar"] [role="button"],
    [data-baseweb="calendar"] button {
        color: rgb(33, 33, 33) !important;
        background: transparent !important;
    }
    
    [data-baseweb="calendar"] [role="button"]:hover {
        background: rgb(224, 224, 224) !important;
    }
    
    /* Selected date */
    [data-baseweb="calendar"] [aria-selected="true"] {
        background: rgb(189, 189, 189) !important;
        color: rgb(255, 255, 255) !important;
    }
    
    /* Time picker */
    .stTimeInput [data-baseweb="popover"],
    .stTimeInput [data-baseweb="menu"] {
        background: rgb(248, 249, 250) !important;
    }
    
    /* Calendar navigation arrows - grey */
    [data-baseweb="calendar"] svg {
        fill: rgb(117, 117, 117) !important;
    }
    
    /* Date input icon - grey */
    .stDateInput svg,
    .stTimeInput svg {
        fill: rgb(117, 117, 117) !important;
    }
    
    /* Ensure all input-related popups use faint grey */
    [class*="Popover"],
    [class*="Menu"],
    [class*="Dropdown"] {
        background: rgb(248, 249, 250) !important;
        border: 1px solid rgb(224, 224, 224) !important;
    }
    
    /* Form Labels - Dark and Bold */
    label,
    .stTextInput label,
    .stNumberInput label,
    .stTextArea label,
    .stSelectbox label,
    .stDateInput label,
    .stTimeInput label,
    .stRadio label,
    .stCheckbox label {
        color: rgb(33, 33, 33) !important;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }
    
    /* Form Container */
    .stForm {
        background: rgb(255, 255, 255);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        border: 1px solid rgb(240, 240, 240);
    }
    
    /* Form submit buttons - fix dark background */
    .stForm button,
    .stForm button[kind="secondary"],
    form button {
        background: rgb(255, 255, 255) !important;
        color: rgb(25, 118, 210) !important;
        border: 2px solid rgb(25, 118, 210) !important;
        font-weight: 600 !important;
    }
    
    .stForm button:hover,
    form button:hover {
        background: rgb(25, 118, 210) !important;
        color: rgb(255, 255, 255) !important;
    }
    
    .stForm button[kind="primary"] {
        background: rgb(25, 118, 210) !important;
        color: rgb(255, 255, 255) !important;
        border: 2px solid rgb(25, 118, 210) !important;
    }
    
    .stForm button[kind="primary"]:hover {
        background: rgb(13, 71, 161) !important;
        border-color: rgb(13, 71, 161) !important;
    }
    
    /* Tabs - Modern Design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgb(248, 249, 250);
        padding: 8px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        color: rgb(66, 66, 66);
        background: transparent;
        border: none;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(25, 118, 210, 0.08);
        color: rgb(25, 118, 210);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: rgb(25, 118, 210);
        color: rgb(255, 255, 255) !important;
    }
    
    /* Alerts - Colored Backgrounds with Dark Text */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid;
        padding: 1rem 1.5rem;
    }
    
    /* Success Alert */
    .stSuccess,
    [data-baseweb="notification"][kind="success"] {
        background: rgb(237, 247, 237);
        border-left-color: rgb(67, 160, 71);
        color: rgb(27, 94, 32) !important;
    }
    
    .stSuccess *,
    [data-baseweb="notification"][kind="success"] * {
        color: rgb(27, 94, 32) !important;
    }
    
    /* Info Alert */
    .stInfo,
    [data-baseweb="notification"][kind="info"] {
        background: rgb(232, 244, 253);
        border-left-color: rgb(25, 118, 210);
        color: rgb(13, 60, 97) !important;
    }
    
    .stInfo *,
    [data-baseweb="notification"][kind="info"] * {
        color: rgb(13, 60, 97) !important;
    }
    
    /* Warning Alert */
    .stWarning,
    [data-baseweb="notification"][kind="warning"] {
        background: rgb(255, 248, 225);
        border-left-color: rgb(251, 140, 0);
        color: rgb(153, 69, 0) !important;
    }
    
    .stWarning *,
    [data-baseweb="notification"][kind="warning"] * {
        color: rgb(153, 69, 0) !important;
    }
    
    /* Error Alert */
    .stError,
    [data-baseweb="notification"][kind="error"] {
        background: rgb(253, 237, 237);
        border-left-color: rgb(229, 57, 53);
        color: rgb(143, 12, 10) !important;
    }
    
    .stError *,
    [data-baseweb="notification"][kind="error"] * {
        color: rgb(143, 12, 10) !important;
    }
    
    /* Tables - Clean and Professional */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border: 1px solid rgb(224, 224, 224);
    }
    
    .dataframe thead tr {
        background: rgb(25, 118, 210);
    }
    
    .dataframe thead th {
        color: rgb(255, 255, 255) !important;
        font-weight: 600;
        padding: 1rem;
        text-align: left;
    }
    
    .dataframe tbody tr {
        background: rgb(255, 255, 255);
    }
    
    .dataframe tbody tr:nth-child(even) {
        background: rgb(248, 249, 250);
    }
    
    .dataframe tbody tr:hover {
        background: rgb(232, 244, 253);
    }
    
    .dataframe td {
        color: rgb(33, 33, 33) !important;
        padding: 0.75rem 1rem;
        border-bottom: 1px solid rgb(240, 240, 240);
    }
    
    /* Expander - Clean Design */
    .streamlit-expanderHeader {
        background: rgb(248, 249, 250);
        border: 1px solid rgb(224, 224, 224);
        border-radius: 8px;
        font-weight: 600;
        color: rgb(33, 33, 33) !important;
        padding: 1rem;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgb(232, 244, 253);
        border-color: rgb(25, 118, 210);
        color: rgb(25, 118, 210) !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, 
            rgb(67, 160, 71) 0%, 
            rgb(25, 118, 210) 100%);
    }
    
    /* Chat Messages */
    .stChatMessage {
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .stChatMessage[data-testid="user"] {
        background: rgb(232, 244, 253);
        border-left: 4px solid rgb(25, 118, 210);
    }
    
    .stChatMessage[data-testid="user"] * {
        color: rgb(13, 60, 97) !important;
    }
    
    .stChatMessage[data-testid="assistant"] {
        background: rgb(248, 249, 250);
        border-left: 4px solid rgb(142, 36, 170);
    }
    
    .stChatMessage[data-testid="assistant"] * {
        color: rgb(33, 33, 33) !important;
    }
    
    /* File Uploader */
    .stFileUploader {
        border: 2px dashed rgb(224, 224, 224);
        border-radius: 10px;
        padding: 2rem;
        background: rgb(248, 249, 250);
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: rgb(25, 118, 210);
        background: rgb(232, 244, 253);
    }
    
    .stFileUploader label {
        color: rgb(66, 66, 66) !important;
    }
    
    /* Checkbox and Radio */
    .stCheckbox label,
    .stRadio label {
        color: rgb(33, 33, 33) !important;
        font-weight: 500;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgb(248, 249, 250);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgb(189, 189, 189);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgb(25, 118, 210);
    }
    
    /* Column Spacing */
    [data-testid="column"] {
        padding: 0 0.5rem;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: rgb(25, 118, 210) !important;
    }
    
    /* Ensure all paragraph text is readable */
    p, span, div {
        color: rgb(33, 33, 33);
    }
    
    /* Code blocks */
    code {
        background: rgb(248, 249, 250);
        color: rgb(229, 57, 53);
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-size: 0.9em;
    }
    
    pre {
        background: rgb(33, 33, 33);
        color: rgb(255, 255, 255);
        padding: 1rem;
        border-radius: 8px;
        overflow-x: auto;
    }
    
    pre code {
        background: transparent;
        color: rgb(255, 255, 255);
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'db' not in st.session_state:
        st.session_state.db = Database()
    
    if 'page' not in st.session_state:
        st.session_state.page = "Dashboard"


def show_sidebar():
    """Display sidebar navigation"""
    with st.sidebar:
        # App logo and title with gradient
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0;'>
            <h1 style='color: rgb(255, 255, 255); margin: 0; font-size: 2.5rem;'>🥗 FoodMind AI</h1>
            <p style='color: rgba(255, 255, 255, 0.9); margin: 0.5rem 0 0 0; font-size: 1.1rem;'>Your Nutrition Companion</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation menu
        st.markdown("### 📱 Navigation")
        
        pages = {
            "Dashboard": "🏠",
            "Food Analysis": "🔍",
            "Meal Tracking": "🍽️",
            "Nutrition Reports": "📊",
            "AI Assistant": "🤖",
            "Profile & Goals": "👤"
        }
        
        for page_name, icon in pages.items():
            if st.button(
                f"{icon} {page_name}",
                key=f"nav_{page_name}",
                use_container_width=True,
                type="primary" if st.session_state.page == page_name else "secondary"
            ):
                st.session_state.page = page_name
                st.rerun()
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📈 Quick Stats")
        
        from datetime import date
        from database import db as db_module
        
        db = st.session_state.db
        today = date.today().strftime("%Y-%m-%d")
        
        summary = db_module.get_daily_nutrition_summary(db, today)
        if summary and summary['meal_count'] > 0:
            st.metric("Today's Calories", f"{summary['total_calories']:.0f} kcal")
            st.metric("Meals Logged", summary['meal_count'])
        else:
            st.info("No meals logged today")
        
        st.markdown("---")
        
        # About section
        with st.expander("ℹ️ About FoodMind AI"):
            st.markdown("""
            **Version:** 1.0.0
            
            FoodMind AI is an AI-powered nutrition tracking application built with:
            - **Streamlit** - Web framework
            - **Pillow** - Image processing
            - **Pandas** - Data analysis
            - **Matplotlib** - Visualizations
            - **Gemini AI** - Nutrition assistant
            
            Track your meals, analyze nutrition, and achieve your health goals with intelligent insights.
            """)


def main():
    """Main application entry point"""
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Check authentication
    if not auth.is_authenticated():
        auth.show_login_page()
        return
    
    # Show user profile in sidebar (top)
    auth.show_user_profile_card()
    
    # Show sidebar navigation
    show_sidebar()
    
    # Show logout button at bottom of sidebar
    auth.show_logout_button()
    
    # Get database instance
    db = st.session_state.db
    
    # Route to appropriate page
    page = st.session_state.page
    
    try:
        if page == "Dashboard":
            dashboard.show_dashboard(db)
        
        elif page == "Food Analysis":
            food_analysis.show_food_analysis(db)
        
        elif page == "Meal Tracking":
            meal_tracking.show_meal_tracking(db)
        
        elif page == "Nutrition Reports":
            reports.show_reports(db)
        
        elif page == "AI Assistant":
            ai_assistant.show_ai_assistant(db)
        
        elif page == "Profile & Goals":
            profile.show_profile_and_goals(db)
        
        else:
            st.error(f"Page '{page}' not found")
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.exception(e)


if __name__ == "__main__":
    main()
