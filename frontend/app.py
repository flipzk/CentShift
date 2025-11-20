import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000"  

# Set page configuration (optional but looks better)
st.set_page_config(page_title="CentShift", page_icon="💰", layout="wide")

st.title("CentShift - Personal Finance Management")

# --- SECTION 1: ADD TRANSACTION ---
with st.form("add_transaction"):
    st.subheader("Add New Transaction")
    
    col1, col2 = st.columns(2)
    with col1:
        type_ = st.selectbox("Type", ["expense", "income", "investment", "saving"])
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        currency = st.selectbox("Currency", ["EUR", "USD", "BRL", "CHF"])
    with col2:
        category = st.text_input("Category", placeholder="e.g., Food, Rent, Salary")
        description = st.text_input("Description", placeholder="Short description")
        date = st.date_input("Date")

    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        data = {
            "type": type_,
            "amount": amount,
            "currency": currency,
            "category": category,
            "description": description,
            "date": str(date)
        }
        try:
            response = requests.post(f"{API_URL}/transactions/", json=data)
            if response.status_code == 200:
                st.success("Transaction added successfully! ")
            else:
                st.error(f"Error: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to Backend. Is Uvicorn running?")

st.markdown("---")
st.header("Budget Planner ")

col_budget_1, col_budget_2 = st.columns(2)

with col_budget_1:
    st.caption("Simulate how to divide your income based on financial strategies.")
    
    salary_input = st.number_input("Your Monthly Salary (€)", min_value=0.0, value=1000.0, step=50.0)
    
    strategy_input = st.selectbox(
        "Pick a Strategy", 
        [
            "50/30/20", 
            "Smart Saver (50/30/10/10)", 
            "70/20/10", 
            "Aggressive Investor (30/30/40)"
        ]
    )

    if st.button("Calculate Allocation"):
        try:
            resp = requests.get(
                f"{API_URL}/budget/calculate", 
                params={"amount": salary_input, "strategy": strategy_input}
            )
            
            if resp.status_code == 200:
                allocation_data = resp.json()
                
                st.success("Suggested Plan:")
                for category, value in allocation_data.items():
                    st.write(f"**{category}:** €{value:.2f}")
                
                st.session_state['budget_data'] = allocation_data
            else:
                st.error("Error calculating budget.")
        except requests.exceptions.ConnectionError:
            st.error("Backend is offline.")

with col_budget_2:

    if 'budget_data' in st.session_state:
        data = st.session_state['budget_data']
        
        # Pie Chart using Matplotlib
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(
            data.values(), 
            labels=data.keys(), 
            autopct='%1.1f%%', 
            startangle=90,
            colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'] 
        )
        ax.axis('equal')  
        st.pyplot(fig)

st.markdown("---")
st.subheader("Recent Transactions")

try:
    response = requests.get(f"{API_URL}/transactions/")
    if response.status_code == 200:
        transactions = response.json()
        if transactions:
            df = pd.DataFrame(transactions)
            
            column_order = ["date", "type", "category", "amount", "currency", "description"]
            # Filter columns that exist in the dataframe to avoid errors
            cols_to_show = [col for col in column_order if col in df.columns]
            
            st.dataframe(df[cols_to_show], use_container_width=True)
        else:
            st.info("No transactions found yet.")
    else:
        st.error("Unable to load transactions")
except requests.exceptions.ConnectionError:
    st.warning("Could not fetch transactions. Backend seems to be offline.")