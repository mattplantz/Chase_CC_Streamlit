import streamlit as st

st.title("Credit Card Charges Analyzer")
st.markdown('''
            The goal of this application is to create an EDA (Exploratory Data Analysis) environment for credit card charges. The application was created with the output from a Chase credit card in mind. Because of this, the following columns are required for functionality:  
                    - **Transaction Date**: Date of transaction  
                    - **Description**: Description of charge  
                    - **Category**: General category of charge  
                    - **Type**: Sale or Payment. Sale = charge to card; payment = payment of card balance  
                    - **Amount**: Value of sale or payment. Please note that sales will be negative and payments will be positive   
                
             The application contains four pages:  
                 - **Homepage**: Description of application, inputs, and requirements  
                 - **Upload Landing Page**: Landing page to upload CSV files containing statement data  
                 - **Query Module**: Interface allowing for SQL-like querying of statement data  
                 - **Visualization**: Module containing multiple premade visualizations of statement data  

             Please use this link to download your own personal chase account activity for usage in the application: https://www.tillerhq.com/how-to-export-chase-bank-statements-into-excel-and-google-sheets/  
            
            For questions on usage or to see the underlying Python script, please visit the Github repository: https://github.com/mattplantz/Chase_CC_Streamlit/  
            Author: Matt Plantz
            ''')
