import streamlit as st
import database  # Import the database functions
from site_pages.pricing import show  # Assuming 'show()' is defined in pricing.py

import time

# Function to load custom CSS
def load_css(file_name):
    with open(file_name, "r", encoding="utf-8") as f:  
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Setting page title and layout
st.set_page_config(page_title="SecurePay-UPI Fraud Detection", page_icon="🕵️‍♂️", layout="wide")

# Load CSS file
load_css("static/style.css")

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# Sidebar Navigation
st.sidebar.markdown("## Navigation")

# If user is logged in, show their name
if st.session_state.get("logged_in") and st.session_state.get("username"):
    st.sidebar.markdown(f"### 👤 {st.session_state.username}")

# Navigation buttons
if st.sidebar.button("Home", use_container_width=True):
    st.session_state.page = "Home"
    st.rerun()

if st.sidebar.button("About", use_container_width=True):
    st.session_state.page = "about"
    st.rerun()

if st.sidebar.button("Dashboard", use_container_width=True):
    st.session_state.page = "dashboard"
    st.rerun()


if st.sidebar.button("Predict", use_container_width=True):
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        # Show error message for unauthenticated users
        st.markdown(
            """
            <div style="background-color: #FFCDD2; padding: 15px; border-radius: 10px; text-align: center; 
                        font-size: 18px; color: #D32F2F; font-weight: bold;">
                ❌ Oh no! You have to log in to access this page.
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(2)
        st.session_state.page = "login"
    else:
        st.session_state.page = "predict"
    st.rerun()

# Pricing Page Button
if st.sidebar.button("Pricing", use_container_width=True):  
    st.session_state.page = "pricing"
    st.rerun()

if not st.session_state.logged_in:
    if st.sidebar.button("Login", use_container_width=True):
        st.session_state.page = "login"
        st.rerun()
    if st.sidebar.button("Signup", use_container_width=True):
        st.session_state.page = "signup"
        st.rerun()
else:
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.page = "Home"
        st.session_state.logged_in = False
        st.session_state.username = None
        st.success("Logged out successfully!")
        st.rerun()

# Display the current page
if st.session_state.page == "Home":
    st.markdown("<h1 class='title'>🕵️‍♂️ SecurePay - Fraud Detection System</h1>", unsafe_allow_html=True)
    st.markdown("<p class='tagline'>Detect fraudulent transactions using machine learning</p>", unsafe_allow_html=True)

    # "How it Works" Section
    st.markdown(
        """
        <div class="how-it-works">
            <h3>How it Works? 🚀</h3>
            <ul>
                <li>📂 Upload transaction data</li>
                <li>⚠️ Our model analyzes and detects fraud</li>
                <li>🚀 Get real-time fraud alerts!</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<p class="get-started">🚀 Get Started</p>', unsafe_allow_html=True)

    # Buttons for login and signup
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        colA, colB = st.columns(2)

        with colA:
            if st.button("Login 🔑", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()

        with colB:
            if st.button("Sign Up 📝", use_container_width=True):
                st.session_state.page = "signup"
                st.rerun()

elif st.session_state.page == "about":
    from site_pages import about
    about.show()

elif st.session_state.page == "predict":
    from site_pages import predict
    predict.show()

elif st.session_state.page == "pricing":
    from site_pages import pricing
    pricing.show()

elif st.session_state.page == "login":
    from site_pages import login
    login.show()

elif st.session_state.page == "signup":
    from site_pages import signup
    signup.show()

elif st.session_state.page == "dashboard":
    from site_pages import dashboard
    dashboard.show()
