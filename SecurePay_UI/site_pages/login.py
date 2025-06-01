import streamlit as st
import database  # Import database functions

def load_css():
    st.markdown(""" 
        <style>
            label {
                color: #1E3A8A !important;  /* Deep Blue */
                font-weight: bold !important;
                font-size: 16px !important;
            }
            .success-message {
                background-color: #E8F5E9;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                font-size: 18px;
                color: #388E3C;
                font-weight: bold;
            }
            .error-message {
                background-color: #FFCDD2;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                font-size: 18px;
                color: #D32F2F;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

def show():
    load_css()
    st.title("🔑 Login to Your Account")
    st.write("Enter your credentials to access SecurePay.")

    # Show error message if login fails
    if "login_error" in st.session_state:
        st.markdown(f'<div class="error-message">❌ {st.session_state.login_error}</div>', unsafe_allow_html=True)
        del st.session_state["login_error"]

    # Show welcome message after login
    if st.session_state.get("logged_in", False) and st.session_state.get("show_welcome_message", False):  
        st.markdown(f'<div class="success-message">✅ Welcome back, {st.session_state.username}!</div>', unsafe_allow_html=True)

    # Username input
    username = st.text_input("Username", key="login_username", placeholder="Enter your username").strip()

    # Password input
    password = st.text_input("Password", key="login_password", placeholder="Enter your password", type="password")

    #  Login logic
    if st.button("Login"):
        user = database.authenticate_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.show_welcome_message = True  # Show welcome message
            st.session_state.page = "Home"  # Redirect to Home
        else:
            st.session_state.login_error = "Invalid username or password. Please try again."
            st.rerun()  # Reload to show error message

if __name__ == "__main__":
    show()
