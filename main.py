import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize in-memory data storage with static data for testing
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame({
        "Date": ["2024-01-15", "2024-02-10", "2024-03-05"],
        "Category": ["Rent", "Supplies", "Salaries"],
        "Amount": [1500.0, 300.0, 2500.0],
        "Description": ["Office rent", "Stationery and office supplies", "Monthly salaries"]
    })

if "invoices" not in st.session_state:
    st.session_state.invoices = pd.DataFrame({
        "Date": ["2024-01-20", "2024-02-15", "2024-03-10"],
        "Client": ["Client A", "Client B", "Client C"],
        "Amount": [5000.0, 2000.0, 3000.0],
        "Description": ["Consulting services", "Project development", "Monthly subscription"]
    })

# Function to add a new expense
def add_expense(date, category, amount, description):
    new_expense = pd.DataFrame([[date, category, amount, description]], columns=st.session_state.expenses.columns)
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)

# Function to add a new invoice
def add_invoice(date, client, amount, description):
    new_invoice = pd.DataFrame([[date, client, amount, description]], columns=st.session_state.invoices.columns)
    st.session_state.invoices = pd.concat([st.session_state.invoices, new_invoice], ignore_index=True)

# Sidebar input forms
st.sidebar.header("Add New Transaction")
with st.sidebar.form("Add Transaction"):
    transaction_type = st.selectbox("Transaction Type", ["Expense", "Invoice"])
    date = st.date_input("Date", value=datetime.today())
    amount = st.number_input("Amount", min_value=0.0, format="%f")
    description = st.text_input("Description")

    if transaction_type == "Expense":
        category = st.selectbox("Category", ["Rent", "Supplies", "Salaries", "Utilities", "Other"])
        submit = st.form_submit_button("Add Expense")
        if submit:
            add_expense(date, category, amount, description)
            st.success("Expense added successfully.")
    elif transaction_type == "Invoice":
        client = st.text_input("Client")
        submit = st.form_submit_button("Add Invoice")
        if submit:
            add_invoice(date, client, amount, description)
            st.success("Invoice added successfully.")

# Display current data
st.header("Current Data")
st.subheader("Expenses")
st.write(st.session_state.expenses)

st.subheader("Invoices")
st.write(st.session_state.invoices)

# Financial Report Generation
st.header("Financial Reports")

def generate_balance_sheet():
    total_assets = st.session_state.invoices["Amount"].sum()
    total_liabilities = st.session_state.expenses["Amount"].sum()
    net_worth = total_assets - total_liabilities
    return {"Total Assets": total_assets, "Total Liabilities": total_liabilities, "Net Worth": net_worth}

def generate_income_statement():
    income = st.session_state.invoices["Amount"].sum()
    expenses = st.session_state.expenses["Amount"].sum()
    net_income = income - expenses
    return {"Income": income, "Expenses": expenses, "Net Income": net_income}

def generate_cash_flow_statement():
    cash_inflow = st.session_state.invoices["Amount"].sum()
    cash_outflow = st.session_state.expenses["Amount"].sum()
    net_cash_flow = cash_inflow - cash_outflow
    return {"Cash Inflow": cash_inflow, "Cash Outflow": cash_outflow, "Net Cash Flow": net_cash_flow}

st.subheader("Balance Sheet")
balance_sheet = generate_balance_sheet()
st.write(balance_sheet)

st.subheader("Income Statement")
income_statement = generate_income_statement()
st.write(income_statement)

st.subheader("Cash Flow Statement")
cash_flow_statement = generate_cash_flow_statement()
st.write(cash_flow_statement)
