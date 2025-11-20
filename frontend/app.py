import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu 

# Page Configuration
# initial_sidebar_state="expanded" garante que a barra começa aberta
st.set_page_config(page_title="CentShift", page_icon="💳", layout="wide", initial_sidebar_state="expanded")
API_URL = "http://127.0.0.1:8000"

st.title("CentShift")
st.markdown("### Personal Finance Tracker")

# --- SIDEBAR: BUDGET CONFIGURATION ---
with st.sidebar:
    st.header("Configuration ⚙️")
    
    salary = st.number_input("Monthly Income (€)", min_value=0.0, value=1000.0, step=50.0)
    
    strategy = st.selectbox(
        "Allocation Strategy",
        ["50/30/20", "Smart Saver (50/30/10/10)", "70/20/10", "Aggressive Investor (30/30/40)"]
    )
    
    if st.button("Update Plan", type="primary"):
        try:
            resp = requests.get(f"{API_URL}/budget/calculate", params={"amount": salary, "strategy": strategy})
            if resp.status_code == 200:
                st.session_state['budget_plan'] = resp.json()
                st.toast("Plan updated successfully!", icon="✅")
            else:
                st.error("Error calculating budget.")
        except:
            st.error("Backend is offline.")

    st.markdown("---")
    st.caption("CentShift v1.0")

# Default plan initialization
if 'budget_plan' not in st.session_state:
    try:
        resp = requests.get(f"{API_URL}/budget/calculate", params={"amount": 1000, "strategy": "50/30/20"})
        if resp.status_code == 200:
            st.session_state['budget_plan'] = resp.json()
        else:
             st.session_state['budget_plan'] = {}
    except:
        st.session_state['budget_plan'] = {}

# --- NAVIGATION MENU (REPLACES TABS) ---
# Removi o background-color para ficar transparente/nativo
selected = option_menu(
    menu_title=None, 
    options=["Dashboard", "Add Transaction", "History"], 
    icons=["speedometer2", "plus-circle-fill", "clock-history"], 
    menu_icon="cast", 
    default_index=0, 
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "icon": {"color": "orange", "font-size": "20px"}, 
        "nav-link": {"font-size": "18px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#FF4B4B"},
    }
)

#  DASHBOARD 
if selected == "Dashboard":
    st.subheader("Overview")
    
    try:
        response = requests.get(f"{API_URL}/transactions/")
        transactions = response.json() if response.status_code == 200 else []
    except:
        transactions = []

    if not transactions:
        st.info("No data available. Start by adding a transaction.")
    else:
        df = pd.DataFrame(transactions)
        df_expenses = df[df['type'].isin(['expense', 'investment', 'saving'])]
        current_spending = df_expenses.groupby('category')['amount'].sum()

        if st.session_state['budget_plan']:
            cols = st.columns(len(st.session_state['budget_plan']))
            
            for idx, (category_name, budget_limit) in enumerate(st.session_state['budget_plan'].items()):
                spent = current_spending.get(category_name, 0.0)
                
                if budget_limit > 0:
                    progress = min(spent / budget_limit, 1.0)
                else:
                    progress = 0.0
                
                with cols[idx]:
                    st.metric(
                        label=category_name, 
                        value=f"€{spent:.2f}", 
                        delta=f"Limit: €{budget_limit:.2f}",
                        delta_color="inverse"
                    )
                    st.progress(progress)
                    
                    if spent > budget_limit:
                        st.error(f"Over by €{spent - budget_limit:.2f}")
        else:
            st.warning("Please configure your plan in the sidebar.")

#  ADD TRANSACTION 
if selected == "Add Transaction":
    st.subheader("New Entry")
    
    col1, col2 = st.columns(2)
    with col1:
        type_ = st.selectbox("Transaction Type", ["expense", "income", "investment", "saving"])
        amount = st.number_input("Amount (€)", min_value=0.0, format="%.2f")
        currency = st.selectbox("Currency", ["EUR", "USD", "BRL", "CHF"])
    with col2:
        if st.session_state.get('budget_plan'):
            budget_categories = list(st.session_state['budget_plan'].keys()) + ["Salary/Income", "Other"]
        else:
            budget_categories = ["Salary/Income", "Other"]
        
        category = st.selectbox("Category", budget_categories)
        description = st.text_input("Description", placeholder="e.g., Supermarket")
        date = st.date_input("Date")

    if st.button("Save Transaction", type="primary", use_container_width=True):
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
                st.success("Transaction saved successfully!")
            else:
                st.error(f"Error: {response.text}")
        except:
            st.error("Backend connection failed.")

#  HISTORY 
if selected == "History":
    st.subheader("Records")
    try:
        if transactions:
            df_show = pd.DataFrame(transactions)
            st.dataframe(
                df_show[["date", "category", "amount", "type", "description"]], 
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No records found.")
    except:
        st.error("Could not load history.")