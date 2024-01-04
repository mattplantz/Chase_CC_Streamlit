import pandas as pd
import streamlit as st
import seaborn as sns
st.title("Charges Visualizer-Inator")
if 'charges' in st.session_state:
  charges = st.session_state.charges
  with st.sidebar:
    option = st.selectbox("What visualization would you like to see?"
                          ,('Histogram','Box Plot', 'Swarm Plot by Category', 'Number of Charges by Category'))
    
  if option == 'Histogram':
      st.subheader('Histogram of All Charges')
      user_bins = st.number_input(label = "How many bins in the Histogram?", min_value = 10, max_value = 100, placeholder = 50)
      hist = sns.histplot(data = charges, x = 'Amount', bins = user_bins)
      st.pyplot(hist.get_figure())
  if option == 'Box Plot':
      cate = st.checkbox("Would you like to see the charges separated by chase-defined categories?")
      if cate:
          st.subheader('Boxplot of Charges by Chase Defined Category')
          box = sns.boxplot(charges, x = 'Amount', y = 'Category')
          st.pyplot(box.get_figure())
      else:
          st.subheader('Boxplot of Charges')
          box = sns.boxplot(charges, x = 'Amount')
          st.pyplot(box.get_figure())
  if option == 'Swarm Plot by Category':
      st.subheader('Swarm plot of Charges by Category')
      swarm = sns.swarmplot(data = charges, x = 'Amount', y = 'Category', hue = 'Category', legend = False)
      st.pyplot(swarm.get_figure())
  if option == 'Number of Charges by Category':
    st.subheader('Charges by Category')
    count = sns.countplot(data = charges, x = 'Category')
    count.set_xticklabels(count.get_xticklabels(), rotation=40, ha="right")
    st.pyplot(count.get_figure())
else:
  st.write('Please upload csv files on the main page')
