import pandas as pd
import streamlit as st
import duckdb
st.title("Charges Querying Module")
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
  select_str = "SELECT * from charges WHERE 1 = 1"
  categories = charges['Category'].unique().tolist()
  with st.sidebar:
    st.write('Filters')
    desc = st.checkbox("Filter on Description?")
    amt = st.checkbox("Filter on Amount?")
    date = st.checkbox("Filter on Transaction Date?")
    cate = st.checkbox("Filter on Category?")
    
  st.subheader('Filter Selection')
  if desc:
      search = st.text_input("What would you like to find in the description?",'')
      wildcards = st.checkbox('Do you want to add a wildcard to your search?')
      if wildcards:
          search_term = "'%" + search + "%'"
      else:
          search_term = "'" + search + "'"
      desc_str = f" and Description ILIKE {search_term}"
  if amt:
      equality = st.selectbox("How would you like to filter the charge amounts?"
                   , ('Greater than or equal to XX'
                      , 'Less than or equal to XX'
                      ,'Between XX and YY'))
      if equality == 'Greater than or equal to XX':
          num = st.number_input("Greater than", placeholder = 0)
          amt_str = f" and Amount >= {num}"
      elif equality == 'Less than or equal to XX':
          num = st.number_input("Less than", placeholder = 0)
          amt_str = f" and Amount <= {num}"
      elif equality == 'Between XX and YY':
          lower = st.number_input("Lower Boundary", placeholder = 0)
          upper = st.number_input("Upper Boundary", placeholder = 2000)
          amt_str = f" and Amount between {lower} and {upper}"
  if date:
      rnge = st.selectbox("How would you like to filter the transaction dates?"
                          , ('Before date'
                             , 'After date'
                             , 'Between dates'))
      if rnge == 'Before date':
          date = st.text_input("Please input the date you would like to filter for in the format MM/DD/YYYY")
          date_str = f" and TransactionDate <= '{date}'"
      if rnge == 'After date':
          date = st.text_input("Please input the date you would like to filter for in the format MM/DD/YYYY")
          date_str = f" and TransactionDate >= '{date}'"
      if rnge == 'Between dates':
          lower = st.text_input("Please input the lower boundary of the date range")
          upper = st.text_input("Please input the upper boundary of the date range")
          date_str = f" and TransactionDate between '{lower}' and '{upper}'"
  if cate:
      choice = st.multiselect("Selec the category or categories you would like to filter on"
                            , categories)
      in_cl = ''
      for val in choice:
          in_cl = in_cl + "'" + val + "'" + ","
      in_cl = in_cl[:-1]
      in_cl = "(" + in_cl + ")"
      cate_str = f" and Category IN {in_cl}" 
      
  # all four
  if desc and amt and date and cate:
      result_str = select_str + desc_str + amt_str + date_str + cate_str
  # no desc
  elif not desc and amt and date and cate:
      result_str = select_str + amt_str + date_str + cate_str
  # no amt
  elif desc and not amt and date and cate:
      result_str = select_str + desc_str + date_str + cate_str
  # no date
  elif desc and amt and not date and cate:
      result_str = select_str + desc_str + amt_str + cate_str
  # no cate
  elif desc and amt and date and not cate:
      result_str = select_str + desc_str + amt_str + date_str
  # desc and amt
  elif desc and amt and not date and not cate:
      result_str = select_str + desc_str + amt_str 
  # desc and date
  elif desc and date and not amt and not cate:
      result_str = select_str + desc_str + date_str
  # desc and cate
  elif desc and cate and not amt and not date:
      result_str = select_str + desc_str + cate_str
  # amt and date
  elif amt and date and not desc and not cate:
      result_str = select_str + amt_str + date_str
  # amt and cate
  elif amt and cate and not desc and not date:
      result_str = select_str + amt_str + cate_str
  # date and cate 
  elif date and cate and not desc and not amt:
      result_str = select_str + date_str + cate_str
  # just desc
  elif desc and not amt and not date and not cate:
      result_str = select_str + desc_str
  # just amt
  elif not desc and amt and not date and not cate:
      result_str = select_str + amt_str
  # just date
  elif not desc and not amt and date and not cate:
      result_str = select_str + date_str
  # just cate
  elif not desc and not amt and not date and cate:
      result_str = select_str + cate_str
  elif not desc and not amt and not date and not cate:
      result_str = select_str
  # output results
  st.subheader("Query Run")
  st.write(result_str)
  st.subheader("Results")
  results = duckdb.sql(result_str).df()
  results_sum = results['Amount'].sum()
  st.write("There are", results.shape[0], "charges matching your parameters")
  st.write("The flagged charges have a total value of $", round(results_sum,2))
  st.dataframe(results)
else:
  st.write('Please upload csv files on the main page')
