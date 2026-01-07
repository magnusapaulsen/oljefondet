import pandas as pd
import streamlit as st

# Read CSV
oljefondet = pd.read_csv('oljefondet.csv', encoding='utf-16', sep=';', decimal=',', thousands='.')

# Clean data
# Remove unnecessary columns
oljefondet = oljefondet.drop(columns=['Incorporation Country', 'Market Value USD'])
# Change datatypes
oljefondet['Region'] = oljefondet['Region'].astype('category')
oljefondet['Country'] = oljefondet['Country'].astype('category')
oljefondet['Name'] = oljefondet['Name'].astype('string')
oljefondet['Industry'] = oljefondet['Industry'].astype('category')
oljefondet['Ownership'] = pd.to_numeric(oljefondet['Ownership'].str.replace('%', '').str.replace(',', '.'), errors='coerce')
oljefondet['Voting'] = pd.to_numeric(oljefondet['Voting'].str.replace('%', '').str.replace(',', '.'), errors='coerce')
# These changes halved the amount of memory usage


def filter_by_region(region: str):
    return oljefondet.loc[oljefondet['Region'].str.contains(region)]

def filter_by_country(country: str):
    return oljefondet.loc[oljefondet['Country'].str.contains(country)]

def filter_by_name(name: str):
    return oljefondet.loc[oljefondet['Name'].str.contains(name, case=False)]

def filter_by_industry(industry: str):
    return oljefondet.loc[oljefondet['Industry'].str.contains(industry)]

def filter_by_market_value(mv_min: int, mv_max: int):
    return oljefondet.loc[oljefondet['Market Value NOK'].between(mv_min, mv_max)]

def filter_by_voting(voting_min: float, voting_max: float):
    return oljefondet.loc[oljefondet['Voting'].between(voting_min, voting_max)]

def filter_by_ownership(ownership: float):
    return oljefondet.loc[oljefondet['Ownership'].between(0, ownership)]


st.title('Oljefondet 💰')

name = st.text_input('Name: ', placeholder='Ex. NVIDIA Corp').strip()

if name:
    st.dataframe(filter_by_name(name))

ownership = st.slider('Ownership', min_value=0, max_value=100, step=1)

if ownership:
    st.dataframe(filter_by_ownership(ownership, 100))