import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000"  

st.title("CentShift - Personal Finance Management")

with st.form("add_transaction"):
    st.subheader("Add New Transaction")
    type_ = st.selectbox("Type", ["expense", "income", "investment", "saving"])
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    currency = st.selectbox("Currency", ["EUR", "USD", "BRL", "CHF"])
    category = st.text_input("Category")
    description = st.text_input("Description")
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
        response = requests.post(f"{API_URL}/transactions/", json=data)
        if response.status_code == 200:
            st.success("Transaction added successfully!")
        else:
            st.error(f"Error: {response.text}")

st.subheader("Recent Transactions")
response = requests.get(f"{API_URL}/transactions/")
if response.status_code == 200:
    df = pd.DataFrame(response.json())
    st.dataframe(df)
else:
    st.error("Unable to load transactions")
