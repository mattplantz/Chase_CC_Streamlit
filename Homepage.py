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
    
with st.sidebar:
    Flag_Charges = st.checkbox("Flag Specific Charges")
    Over_val = st.checkbox("Flag Charges Over $XX")
if Flag_Charges:
    st.write("Please input the parameters for your search")
    text_to_find = st.text_input("What text would you like to flag? Please separate multiple search terms with '|'", '')
    text_to_find = text_to_find.upper()
    if text_to_find != '' and 'charges' in st.session_state:
        charges = st.session_state.charges
        charges['Flag'] = charges['Description'].str.contains(text_to_find).astype(int)
        st.session_state['charges'] = charges
        st.subheader("Flagged Instances")
        st.write("There are ", charges['Flag'].sum(), "instances of your flag")
        flagged_sum = charges.loc[charges['Flag'] == 1, 'Amount'].sum()
        st.write("The flagged charges have a total value of $", round(flagged_sum,2))
        st.dataframe(charges[charges['Flag'] == 1])
    elif text_to_find != '' and 'charges' not in st.session_state:
        st.write("Please upload your CC files")
    elif text_to_find == '' and 'charges' in st.session_state:
        st.write("Please add text to flag")
if Over_val:
    charges = st.session_state.charges
    user_input = st.number_input("Flag charges over this value", placeholder = 50)
    flagged = charges[charges['Amount'] >= user_input]
    st.write("There are", flagged.shape[0], "charges over $", user_input)
    st.write("The flagged charges have a total value of $", round(flagged['Amount'].sum(),2))
    st.dataframe(flagged)
    
