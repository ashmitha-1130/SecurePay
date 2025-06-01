import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

def show():
    st.title("\U0001F4CA UPI Fraud Detection Dashboard")

    # Load Data
    @st.cache_data
    def load_data():
        df = pd.read_csv("C:\\Users\\ashmi\\Desktop\\SecurePay\\SecurePay_UI\\SecurePay_UPI_Dataset.csv")
        df['Date'] = pd.to_datetime(df['Date'])  # Convert Date to datetime
        return df

    df = load_data()


    # Styling Fix for Selectbox and Labels
    st.markdown(
        """
        <style>
        /* Ensure selectbox dropdown background is white and text is black */
        div[data-baseweb="select"] > div {
            background-color: white !important;
            color: black !important;
        }
        
        /* Ensure dropdown popover background is white and text is black */
        div[data-baseweb="popover"] {
            background-color: white !important;
        }
        
       div[data-baseweb="select"] {
    background-color: white !important;
    color: black !important;
}

/* Force the dropdown options popover background to white */
div[role="listbox"] {
    background-color: white !important;
}

/* Ensure dropdown options text is black */
div[role="option"] {
    color: black !important;
    background-color: white !important;
}

/* Ensure the dropdown arrow is black */
div[data-baseweb="select"] svg {
    fill: black !important;
}
        /* Change the color of the dropdown arrow to black */
        div[data-baseweb="select"] svg {
            fill: black !important;
        }
        
        /* Change label color above select boxes to black */
        label[data-testid="stWidgetLabel"] {
            color: black !important;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )



    # Filter Options
    years = sorted(df['Date'].dt.year.unique(), reverse=True)
    months = {
        "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
        "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
    }

    # Place filters in a single row (aligned to top-right)
    col1, col2, col3 = st.columns([2, 1, 1])  

    with col2:
        selected_year = st.selectbox("Select Year", years, index=0)
    
    with col3:
        selected_month = st.selectbox("Select Month", list(months.keys()), index=0)

    # Filter Data
    filtered_df = df[(df["Date"].dt.year == selected_year) & (df["Date"].dt.month == months[selected_month])]

    # Define a function to apply a white background and black text color
    def update_chart_layout(fig):
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black'),
            title=dict(font=dict(color='black')),
            xaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
            yaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
            legend=dict(font=dict(color='black'))
        )
        return fig

    # \U0001F4CA **Visualization 1 & 2: Side by Side**
    if not filtered_df.empty:
        col1, col2 = st.columns([2, 2])  # Increased width

        with col1:
            transaction_counts = filtered_df["Transaction_Type"].value_counts()
            fig1 = px.bar(
                x=transaction_counts.index,
                y=transaction_counts.values,
                color=transaction_counts.index,
                title="Fraud Distribution by Transaction Type",
                labels={'x': 'Transaction Type', 'y': 'Fraud Cases'},
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig1 = update_chart_layout(fig1)
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            fraud_by_payment = filtered_df[filtered_df["fraud"] == 1]["Payment_Gateway"].value_counts().reset_index()
            fraud_by_payment.columns = ["Payment_Gateway", "Fraud"]

            fig2 = px.pie(
                 fraud_by_payment,
                 names="Payment_Gateway",
                 values="Fraud",
                 title="Fraud Cases by Payment Gateway",
                 color_discrete_sequence=px.colors.qualitative.Vivid,
                 hole=0.3 
            )
            fig2 = update_chart_layout(fig2)
            st.plotly_chart(fig2, use_container_width=True)

        # \U0001F4CA **Visualization 3 & 4: Side by Side**
        col3, col4 = st.columns([2, 2])  # Increased width

        with col3:
            fraud_by_merchant = filtered_df[filtered_df["fraud"] == 1]["Merchant_Category"].value_counts().reset_index()
            fraud_by_merchant.columns = ["Merchant Category", "Fraud Cases"]
            
            fig3 = px.bar(
                fraud_by_merchant,
                x="Merchant Category",
                y="Fraud Cases",
                color="Merchant Category",
                title="Fraud Distribution by Merchant Category",
                labels={"Merchant Category": "Merchant Category", "Fraud Cases": "Number of Fraud Cases"},
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig3 = update_chart_layout(fig3)
            st.plotly_chart(fig3, use_container_width=True)

        with col4:
            fraud_by_state = filtered_df[filtered_df["fraud"] == 1]["Transaction_State"].value_counts().reset_index()
            fraud_by_state.columns = ["Transaction State", "Fraud Cases"]

            fig4 = px.bar(
                fraud_by_state,
                x="Transaction State",
                y="Fraud Cases",
                color="Transaction State",
                title="Fraud Distribution by Transaction State",
                labels={"Transaction State": "Transaction State", "Fraud Cases": "Number of Fraud Cases"},
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig4 = update_chart_layout(fig4)
            st.plotly_chart(fig4, use_container_width=True)

        # \U0001F4CA **Visualization 5: Centered Heatmap**
        st.markdown("### Fraud Heatmap by Year")
        col5, col6, col7 = st.columns([1, 4, 1])  # Center heatmap
        
        with col6:
            fraud_by_year = df.groupby([df["Date"].dt.year, "fraud"]).size().unstack()
            fig5, ax = plt.subplots(figsize=(10, 5))  # Increased width
            sns.heatmap(fraud_by_year, annot=True, fmt="d", cmap="coolwarm", linewidths=0.5, ax=ax)
            
            ax.set_title("Fraud Cases Heatmap by Year", color='black')
            ax.set_xlabel("Fraud Status (0 = No Fraud, 1 = Fraud)", color='black')
            ax.set_ylabel("Year", color='black')
            
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_color('black')
            
            st.pyplot(fig5)

    else:
        st.warning("⚠️ No data available for the selected month and year.")

if __name__ == "__main__":
    show()