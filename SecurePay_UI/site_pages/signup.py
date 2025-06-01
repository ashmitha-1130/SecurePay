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
        </style>
    """, unsafe_allow_html=True)

def show():
    load_css()

    st.title("🚀 Create Your Account")
    st.write("Join **SecurePay** and start detecting fraudulent transactions.")

    # Show error message at the top if it exists
    if "signup_error" in st.session_state:
        st.markdown(
            f"""
            <div style="background-color: #FFCDD2; padding: 15px; border-radius: 10px; text-align: center; 
                        font-size: 18px; color: #D32F2F; font-weight: bold;">
                ❌ {st.session_state.signup_error}
            </div>
            """,
            unsafe_allow_html=True
        )
        del st.session_state["signup_error"]  # Remove error after displaying

    # Show success message at the top if it exists
    if "signup_success" in st.session_state:
        st.markdown(
            f"""
            <div style="background-color: #E0F2F1; padding: 15px; border-radius: 10px; text-align: center; 
                        font-size: 18px; color: #00796B; font-weight: bold;">
                ✅ {st.session_state.signup_success}
            </div>
            """,
            unsafe_allow_html=True
        )
        # del st.session_state["signup_success"]  # Remove success message after displaying

    # Input Fields
    username = st.text_input("Username", key="signup_username", placeholder="Enter your username").strip()
    email = st.text_input("Email", key="signup_email", placeholder="Enter your email").strip()
    password = st.text_input("Password", key="signup_password", placeholder="Enter your password", type="password")
    confirm_password = st.text_input("Confirm Password", key="signup_confirm_password", placeholder="Re-enter your password", type="password")

    # Signup button
    if st.button("Sign Up"):
        if not username or not email or not password or not confirm_password:
            st.session_state.signup_error = "All fields are required."
            st.rerun()
        elif password != confirm_password:
            st.session_state.signup_error = "Passwords do not match."
            st.rerun()
        else:
            try:
                database.add_user(username, email, password)
                st.session_state.signup_success = "🎉 Account created successfully! Please log in."
                st.session_state.page = "login"
                st.rerun()
            except ValueError as e:
                st.session_state.signup_error = str(e)
                st.rerun()

# Call the function only once
if __name__ == "__main__":
    show()
