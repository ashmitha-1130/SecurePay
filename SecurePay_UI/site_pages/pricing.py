import streamlit as st
import time
from razorpay_integration import create_order  # Razorpay integration
from database import update_payment_status, has_paid  
import streamlit.components.v1 as components

    
#Check if payment was successful and update session state + database
if "payment_success" in st.query_params:
    username = st.session_state.get("username", "")

    if username:
        # print(f"DEBUG: Updating payment status for user -> {username}") 
        update_payment_status(username)
        time.sleep(1) 

    #Ensure session state updates
    st.session_state["paid"] = True
    st.session_state["user_plan"] = "Paid"
    st.session_state["payment_status"] = "Paid"
    st.query_params.clear()

    st.session_state["page"] = "predict"
    st.rerun()



def show():
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>💳 Choose Your Plan</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #333;'>🚀 Secure your transactions with our AI-powered fraud detection. Pick a plan and stay safe!</p>", unsafe_allow_html=True)

    username = st.session_state.get("username", "")

    # Check if user has already paid (Persistent check)
    if username:
        st.session_state["paid"] = has_paid(username)  # Check DB
        st.session_state["payment_status"] = "Paid" if str(st.session_state["paid"]) in ["Paid", "1"] else "Free"
        st.session_state["user_plan"] = "Paid" if str(st.session_state["paid"]) in ["Paid", "1"] else "Free"


        
        print("DEBUG: Updated session state in pricing.py ->", st.session_state)

    plans = [
        {
            "title": "Free Plan",
            "benefits": ["✔ Basic Fraud Detection", "✔ Limited Transactions", "✔ Community Support"],
            "price": "FREE",
            "button_text": "Get Started",
            "redirect": "predict",
            "amount": 0
        },
        {
            "title": "Advanced Plan",
            "benefits": ["✔ All Free Features", "✔ Priority Support", "✔ Faster Processing"],
            "price": "₹19.99/month",
            "button_text": "Pay Now",
            "amount": 1999
        },
        {
            "title": "Enterprise Plan",
            "benefits": ["✔ Custom Reports", "✔ Dedicated Support", "✔ High Volume Transactions"],
            "price": "₹49.99/month",
            "button_text": "Pay Now",
            "amount": 4999
        },
    ]

    col1, col2, col3 = st.columns(3)

    for col, plan in zip([col1, col2, col3], plans):
        with col:
            st.markdown(f"""
                <div style="border: 2px solid #1E3A8A; border-radius: 15px; padding: 20px; text-align: center; background-color: #F8FAFC;">
                    <h3 style="color: #1E3A8A;">{plan["title"]}</h3>
                    <ul style="list-style-type: none; padding: 0;">
                        {"".join(f"<li style='color: #1E3A8A; font-size: 16px;'>{benefit}</li>" for benefit in plan["benefits"])}
                    </ul>
                    <h2 style="color: #1E3A8A;">{plan["price"]}</h2>
                </div>
            """, unsafe_allow_html=True)

            if plan["title"] == "Free Plan":
                if st.session_state.get("free_trial_exhausted", False):
                    st.button(plan["button_text"], key=plan["title"], use_container_width=True, disabled=True)
          
                else:
                    if st.button(plan["button_text"], key=plan["title"], use_container_width=True):
                        st.session_state.page = "predict"
                       
                        st.rerun()
            else:
                order = create_order(plan["amount"])
                if order and "id" in order:
                    order_id = order["id"]

                    # Razorpay payment integration 
                    components.html(f"""
                        <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
                        <button id="rzp-button-{plan["title"]}" style="background-color: #1E3A8A; color: white; padding: 12px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; width: 100%; font-weight: bold;">
                            {plan["button_text"]}
                        </button>
                        <script>
                            var options = {{
                                "key": "YOUR_API_KEY",
                                "amount": "{plan["amount"]}00",
                                "currency": "INR",
                                "name": "{plan["title"]}",
                                "description": "Payment for {plan["title"]}",
                                "order_id": "{order_id}",
                                "handler": function (response) {{
                                    alert("✅ Payment successful! Payment ID: " + response.razorpay_payment_id);
                                    
                                    // ✅ Update payment status in DB
                                    fetch('/update_payment_status?username={username}&paid=true')
                                    .then(response => response.json())
                                    .then(data => {{
                                        if (data.success) {{
                                            window.location.href = "/?payment_success=true"; 
                                        }}
                                    }});
                                }},
                                "prefill": {{
                                    "name": "{username}",
                                    "email": "customer@example.com",
                                    "contact": "9999999999"
                                }},
                                "theme": {{
                                    "color": "#1E3A8A"
                                }}
                            }};

                            document.getElementById('rzp-button-{plan["title"]}').onclick = function(e) {{
                                var rzp = new Razorpay(options);
                                rzp.open();
                                e.preventDefault();
                            }};
                        </script>
                    """, height=300)
                else:
                    st.error("Failed to create order. Please try again.")

if __name__ == "__main__":
    show()
