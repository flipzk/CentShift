import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu 
from datetime import date
import os  

st.set_page_config(page_title="CentShift", page_icon="💳", layout="wide", initial_sidebar_state="expanded")

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.title("CentShift")
st.markdown("### Personal Finance Tracker")

with st.sidebar:
    st.header("Configuration")
    
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
                st.success("Plan updated successfully")
            else:
                st.error("Error calculating budget")
        except:
            st.error("Backend is offline")

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

# NAvigation Menu
selected = option_menu(
    menu_title=None, 
    options=["Dashboard", "AI Scan", "Add Transaction", "History"], 
    icons=["bar-chart", "camera", "plus", "clock"],  
    default_index=0, 
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "icon": {"color": "orange", "font-size": "16px"}, 
        "nav-link": {"font-size": "15px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#FF4B4B"},
    }
)

# DASHBOARD 
if selected == "Dashboard":
    st.subheader("Overview")
    
    try:
        response = requests.get(f"{API_URL}/transactions/")
        transactions = response.json() if response.status_code == 200 else []
    except:
        transactions = []

    if not transactions:
        st.info("No data available. Start by scanning a receipt or adding a transaction.")
    else:
        df = pd.DataFrame(transactions)
        df_expenses = df[df['type'].isin(['expense', 'investment', 'saving'])]
        
        if not df_expenses.empty:
            current_spending = df_expenses.groupby('category')['amount'].sum()
        else:
            current_spending = pd.Series()

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

# AI SCANNER 
if selected == "AI Scan":
    st.subheader("Receipt Scanner")
    st.markdown("Upload a receipt image for automatic data extraction.")

    uploaded_file = st.file_uploader("Choose a receipt image...", type=["jpg", "png", "jpeg", "heic"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Receipt", width=300)
        
        if st.button("Analyze Receipt", type="primary"):
            with st.spinner("Processing..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    response = requests.post(f"{API_URL}/transactions/scan", files=files)
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state['scanned_data'] = data
                        st.success("Analysis complete")
                    else:
                        st.error(f"Analysis Failed: {response.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")

    # Form to review AI data
    if 'scanned_data' in st.session_state:
        st.divider()
        st.subheader("Review & Save")
        
        ai_data = st.session_state['scanned_data']
        
        with st.form("scanned_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                try:
                    default_date = date.fromisoformat(ai_data.get("date", str(date.today())))
                except:
                    default_date = date.today()

                new_date = st.date_input("Date", value=default_date)
                new_desc = st.text_input("Description", value=ai_data.get("description", ""))
                new_type = st.selectbox("Type", ["expense", "income", "investment", "saving"], index=0)

            with col2:
                new_amount = st.number_input("Amount (€)", value=float(ai_data.get("total", 0.0)), step=0.5)
                
                if st.session_state.get('budget_plan'):
                    cats = list(st.session_state['budget_plan'].keys()) + ["Salary/Income", "Other"]
                else:
                    cats = ["Salary/Income", "Other"]
                
                suggested_cat = ai_data.get("category", "Other")
                cat_index = cats.index(suggested_cat) if suggested_cat in cats else 0
                
                new_category = st.selectbox("Category", cats, index=cat_index)
                new_currency = st.selectbox("Currency", ["EUR", "USD", "BRL"], index=0)

            submitted = st.form_submit_button("Confirm & Save")
            
            if submitted:
                payload = {
                    "type": new_type,
                    "amount": new_amount,
                    "currency": new_currency,
                    "category": new_category,
                    "description": new_desc,
                    "date": str(new_date)
                }
                
                try:
                    resp = requests.post(f"{API_URL}/transactions/", json=payload)
                    if resp.status_code == 200:
                        st.success("Transaction saved")
                        del st.session_state['scanned_data']
                    else:
                        st.error(f"Error saving: {resp.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

if selected == "Add Transaction":
    st.subheader("Manual Entry")
    
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
        date_tx = st.date_input("Date")

    if st.button("Save Transaction", type="primary", use_container_width=True):
        data = {
            "type": type_,
            "amount": amount,
            "currency": currency,
            "category": category,
            "description": description,
            "date": str(date_tx)
        }
        try:
            response = requests.post(f"{API_URL}/transactions/", json=data)
            if response.status_code == 200:
                st.success("Transaction saved")
            else:
                st.error(f"Error: {response.text}")
        except:
            st.error("Backend connection failed")

# HISTORY 
if selected == "History":
    st.subheader("Records")
    try:
        response = requests.get(f"{API_URL}/transactions/")
        if response.status_code == 200:
            transactions = response.json()
            if transactions:
                df_show = pd.DataFrame(transactions)
                st.dataframe(
                    df_show[["date", "category", "amount", "type", "description"]], 
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No records found.")
        else:
            st.error("Could not fetch data.")
    except:
        st.error("Could not load history. Is backend running?")