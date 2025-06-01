import streamlit as st

def show():
    st.markdown("""
        <style>
            .section {
                padding: 20px;
                background-color: #F8FAFC;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            .card {
                border: 2px solid #1E3A8A;
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                background-color: #F8FAFC;
                height: 200px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            .highlight {
                color: #1E3A8A;
                font-weight: bold;
            }
            .fraud-card {
                background-color: #fff;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                margin: 10px 0;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🚨 The Rise of UPI Fraud</h2>", unsafe_allow_html=True)
    st.markdown("""
        <p style='text-align: center; font-size: 18px; color: #333;'>
            Digital payments have transformed transactions, but they have also given rise to cyber fraud. 
            In 2023 alone, <span class='highlight'>over 95,000 cases</span> of UPI fraud were reported, resulting in financial losses worth crores.
        </p>
    """, unsafe_allow_html=True)

    # Create two columns
    col1, col2 = st.columns([2, 1])  # Left column for text, right column for image

    with col1:
        st.markdown("<h3 style='color: #1E3A8A;'>⚠️ Common UPI Fraud Tactics:</h3>", unsafe_allow_html=True)
        st.markdown("<div class='fraud-card'>🔗 <b>Fake Payment Links:</b> Fraudsters send phishing links to steal credentials.</div>", unsafe_allow_html=True)
        st.markdown("<div class='fraud-card'>📞 <b>Impersonation Calls:</b> Scammers pretend to be bank representatives for OTPs.</div>", unsafe_allow_html=True)
        st.markdown("<div class='fraud-card'>💳 <b>Unauthorized Transactions:</b> Hidden malware extracts funds from accounts.</div>", unsafe_allow_html=True)
        st.markdown("<div class='fraud-card'>🎁 <b>Fake Cashback Offers:</b> Fraudsters lure users into sharing personal details.</div>", unsafe_allow_html=True)

    with col2:
        st.image("site_pages/images/upi.png", use_container_width=True)

    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🔍 Why Choose SecurePay?</h2>", unsafe_allow_html=True)
    st.markdown("""
        <p style='text-align: center; font-size: 18px; color: #333;'>
            SecurePay is an AI-powered fraud detection system that ensures your transactions remain safe.
        </p>
        <ul style='font-size: 16px; color: #333;'>
            <li>🛡️ <b>Real-time Fraud Alerts:</b> Get instant warnings on suspicious transactions.</li>
            <li>📊 <b>AI-driven Analysis:</b> Detects fraud patterns with machine learning.</li>
            <li>⚡ <b>Fast & Secure:</b> Protects your money without transaction delays.</li>
            <li>✅ <b>Seamless Integration:</b> Easy to use and integrates with your UPI system.</li>
        </ul>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🛡️ How SecurePay Works</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #333;'>🔍 AI-powered fraud detection in three simple steps.</p>", unsafe_allow_html=True)

    steps = [
        {"price": "Step 1", "title": "Upload Transaction"},
        {"price": "Step 2", "title": "Model Predicts Fraud"},
        {"price": "Step 3", "title": "Real-time Fraud Updates"},
    ]

    col1, col2, col3 = st.columns(3)

    for col, step in zip([col1, col2, col3], steps):
        with col:
            st.markdown(f"""
                <div class="card">
                    <h3 style="color: #1E3A8A;">{step["price"]}</h3>
                    <h3 style="color: #1E3A8A;">{step["title"]}</h3>
                </div>
            """, unsafe_allow_html=True)

    # Add "Get Started" button at the bottom
    st.markdown("<br>", unsafe_allow_html=True)  # Add space before the button
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button("🚀 Get Started", use_container_width=True):
            st.session_state.page = "signup"

if __name__ == "__main__":
    show()
