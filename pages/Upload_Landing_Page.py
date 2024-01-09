import pandas as pd
import streamlit as st

st.title("Chase Credit Card Statement Reader-Inator")

uploaded_files = st.file_uploader("Please upload your Chase CC Account Activity", type = ['csv'], accept_multiple_files= True)
if uploaded_files not in st.session_state:
    st.session_state.uploaded_files = uploaded_files
if uploaded_files:
        read_data = [pd.read_csv(file) for file in uploaded_files]
        df = pd.concat(read_data)
        # flip sign of amount
        df['Amount'] = df['Amount'] * - 1
    
        # separate payments and charges
        charges = df[df['Type'] == 'Sale']
        charges['Description'] = charges['Description'].str.upper()
        payments = df[df['Type'] == 'Payment']
        if 'charges' not in st.session_state:
            st.session_state.charges = charges
        if 'payments' not in st.session_state:
            st.session_state.payments = payments
