import altair as alt
import numpy as np
import pandas as pd
import time
import streamlit as st
import datetime
from datetime import datetime as dt
from database import has_paid
import base64
import pickle
import sqlite3  # Database import for payment status
from xgboost import XGBClassifier


def get_payment_status(username):
    """Check if the user has made a successful payment."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT payment_status FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "Unpaid"


def show():
    # Injecting Custom CSS
    st.markdown(
        """
        <style>
        label { color: #1E3A8A !important; font-weight: bold !important; font-size: 16px !important; }
        body { background-color: #f0f8ff; color: #003366; }
        .stButton>button { background-color: #003366; color: white; width: 100%; padding: 10px; font-size: 18px; }
        .stSelectbox, .stTextInput, .stNumberInput { width: 100%; background-color: #f0f8ff; }
        .stFileUploader { width: 100%; }
        
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

        .warning-message {
            background-color: #FFF3CD;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 18px;
            color: #856404;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Welcome to your own UPI Transaction Fraud Detector!")
    st.write("You can inspect a single transaction or upload a .csv file to check multiple transactions.")

    pickle_file_path = r"C:\\Users\\ashmi\\Desktop\\SecurePay\\SecurePay_UI\\UPI_fraud_detection.pkl"
    loaded_model = pickle.load(open(pickle_file_path, 'rb'))

    username = st.session_state.get("username", None)
    if username:
        st.session_state["paid"] = has_paid(username)
        st.session_state["payment_status"] = "Paid" if str(st.session_state["paid"]) in ["Paid", "1"] else "Free"
        st.session_state["user_plan"] = "Paid" if str(st.session_state["paid"]) in ["Paid", "1"] else "Free"

    tt = ["Bill Payment", "Investment", "Other", "Purchase", "Refund", "Subscription"]
    pg = ["MobiKwik", "Stripe", "BHIM", "Other", "Paytm", "CReditPAY", "Razorpay", "Rupay"]
    ts = ['Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 
          'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 
          'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 
          'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
    mc = ['Donations and Devotion', 'Financial services and Taxes', 'Home delivery', 'Investment', 'More Services', 
          'Other', 'Purchases', 'Travel bookings', 'Utilities']

    tran_date = st.date_input("Select the date of your transaction", datetime.date.today())
    selected_date = dt.combine(tran_date, dt.min.time())
    month, year = selected_date.month, selected_date.year

    tran_type = st.selectbox("Select transaction type", tt)
    pmt_gateway = st.selectbox("Select payment gateway", pg)
    tran_state = st.selectbox("Select transaction state", ts)
    merch_cat = st.selectbox("Select merchant category", mc)
    amt = st.number_input("Enter transaction amount", step=0.1)
    if amt < 0:
        st.markdown('<div class="error-message">❌ Enter a valid amount! Amount cannot be negative.</div>', unsafe_allow_html=True)
        return 

    st.write("### OR")
    df = pd.read_csv(r"C:\\Users\\ashmi\\Desktop\\SecurePay\\SecurePay_UI\\sample.csv")
    st.write("CSV Format:", df)

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded CSV:", df)

    button_clicked = st.button("Check transaction(s)", key="predict_button")

    if button_clicked:
        if uploaded_file is not None:
            with st.spinner("Checking transactions..."):
                def download_csv():
                    csv = df.to_csv(index=False, header=True)
                    b64 = base64.b64encode(csv.encode()).decode()
                    return f'<a href="data:file/csv;base64,{b64}" download="output.csv">Download Output CSV</a>'

                df[['Month', 'Year']] = df['Date'].str.split('-', expand=True)[[1, 2]].astype(int)
                df.drop(columns=['Date'], inplace=True)

                results = []
                for _, row in df.iterrows():
                    input_values = [row['Amount'], row['Year'], row['Month']]
                    input_values += [1 if row['Transaction_Type'] == val else 0 for val in tt]
                    input_values += [1 if row['Payment_Gateway'] == val else 0 for val in pg]
                    input_values += [1 if row['Transaction_State'] == val else 0 for val in ts]
                    input_values += [1 if row['Merchant_Category'] == val else 0 for val in mc]

                    results.append(loaded_model.predict([input_values])[0])

                df['fraud'] = results
                message = '<div class="success-message">✅ Checked transactions!</div>'
                st.markdown(message, unsafe_allow_html=True)
                st.markdown(download_csv(), unsafe_allow_html=True)
        else:
            with st.spinner("Checking transaction(s)..."):
                input_values = [amt, year, month]
                input_values += [1 if tran_type == val else 0 for val in tt]
                input_values += [1 if pmt_gateway == val else 0 for val in pg]
                input_values += [1 if tran_state == val else 0 for val in ts]
                input_values += [1 if merch_cat == val else 0 for val in mc]

                result = loaded_model.predict([input_values])[0]
                
                message = ('<div class="success-message">✅ Not a fraudulent transaction.</div>' 
                           if result == 0 
                           else '<div class="error-message">❌ Fraudulent transaction detected!</div>')
                st.markdown(message, unsafe_allow_html=True)


if __name__ == "__main__":
    show()
