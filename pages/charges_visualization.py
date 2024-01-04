import pandas as pd
import streamlit as st
import seaborn as sns

if 'charges' in st.session_state:
  st.dataframe(st.session_state.charges)
else:
  st.write('Please upload csv files on the main page')
