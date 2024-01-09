import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
st.title("Charges Visualizer")
if 'charges' in st.session_state:
  charges = st.session_state.charges
  charges['Month'] = pd.DatetimeIndex(charges['Transaction Date']).month
  charges['Month'] = charges['Month'].astype(str)
  for i, row in charges.iterrows():
      if len(row['Month']) == 1:
          charges.loc[i, 'Month'] = '0' + row['Month']
      else:
          continue
  charges['Year'] = pd.DatetimeIndex(charges['Transaction Date']).year
  charges['YearMo'] = charges['Year'].astype(str) + charges['Month'].astype(str)
  charges['YearMo'] = charges['YearMo'].astype(int)
  with st.sidebar:
    option = st.selectbox("What visualization would you like to see?"
                          ,('Histogram'
                            ,'Box Plot'
                            ,'Swarm Plot by Category'
                            ,'Number of Charges by Category'
                            , 'Monthly Spending'
                           , 'Violin Distribution))
    
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
  if option == 'Monthly Spending':
    st.subheader('Spending by Month')
    legend = st.checkbox('Would you like to see the charges colored by category?')
    if legend:
        monthly = sns.stripplot(data = charges, x = 'YearMo', y = 'Amount', hue = 'Category', legend = 'brief')
        monthly.set_xticklabels(monthly.get_xticklabels(), rotation=40, ha="right")
        sns.move_legend(monthly, "upper left", bbox_to_anchor=(1, 1))
        st.pyplot(monthly.get_figure())
    else:
        monthly = sns.stripplot(data = charges, x = 'YearMo', y = 'Amount')
        monthly.set_xticklabels(monthly.get_xticklabels(), rotation=40, ha="right")
        st.pyplot(monthly.get_figure())
  if option == 'Violin Distribution':
    st.subheader('Violin Distribution of Charges')
    opt = st.selectbox("Do you want to separate the plots by one of the following categories?"
                 , ('By Month & Year'
                    , 'By Category'
                    , 'None'))
    if opt == 'By Month & Year':
        violin = sns.violinplot(data = charges, x = 'Amount', y = 'YearMo')
        st.pyplot(violin.get_figure())
    if opt == 'By Category':
        violin = sns.violinplot(data = charges, x = 'Amount', y = 'Category')
        st.pyplot(violin.get_figure())
    if opt == 'None':
        violin = sns.violinplot(data = charges, x = 'Amount')
        st.pyplot(violin.get_figure())
else:
  st.write('Please upload csv files on the main page')
