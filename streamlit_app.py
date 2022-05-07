import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

page = st.selectbox("Choose your page", ["Population", "Survival Curve"]) 

cache_population = 'data_cache/population/dataframe.pkl'
df = pd.read_pickle(cache_population)

with open('footnote.md') as f:
  footnote = f.read()

if page == "Population":
  # population trend
  st.title('Viewing Population data')
  
  all_min_age = df.age.min()
  all_max_age = df.age.max()
  all_age = range(all_min_age, all_max_age)
  st.write(all_age)
  
  min_age, max_age = st.select_slider(
       'Select a range of age',
       options=list(all_age),
       value=(all_min_age, all_max_age-1))
  st.write('You selected ages between', min_age, 'and', max_age)
  
  fig = px.bar(        
          df[(df.gender!='both')&(df.age >= min_age)&(df.age < max_age)],
          x = "year",
          y = "population",
          title = "history of population",
          color = "gender"
      )
  st.plotly_chart(fig)

elif page == "Survival Curve":
  # graph of birth_year and age
  st.title('Viewing Population data by birth year')
  
  all_min_year = 1890
  all_max_year = df.year.max()
  all_year = range(all_min_year, all_max_year)
  st.write(all_year)
  
  options = list(all_year)
  the_birth_year = st.selectbox("birth year", options)

  df['birth_year'] = df['year'] - df['age']
  df = df[df.gender!='both']
  df = df.groupby(['birth_year','age'],as_index=False)['population'].sum()
  
  fig = px.bar(        
          df[(df.birth_year==the_birth_year)],
          x = "age",
          y = "population",
          title = "Survival Curve of the Selcected birth-year",
      )
  st.plotly_chart(fig)

st.markdown(footnote)
