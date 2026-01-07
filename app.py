import pandas as pd
import streamlit as st

# Read the cleaned data from the Parquet file
oljefondet = pd.read_parquet('data/cleaned_data.parquet', )

# Filtering functions
def filter_by_region(region: str):
    return oljefondet.loc[oljefondet['region'].str.contains(region)]

def filter_by_country(country: str):
    return oljefondet.loc[oljefondet['country'].str.contains(country)]

def filter_by_name(name: str):
    return oljefondet.loc[oljefondet['name'].str.contains(name, case=False)]

def filter_by_industry(industry: str):
    return oljefondet.loc[oljefondet['industry'].str.contains(industry)]

def filter_by_market_value(mv_min: int, mv_max: int):
    return oljefondet.loc[oljefondet['market_value'].between(mv_min, mv_max)]

def filter_by_voting(voting_min: float, voting_max: float):
    return oljefondet.loc[oljefondet['voting'].between(voting_min, voting_max)]

def filter_by_ownership(ownership: float):
    return oljefondet.loc[oljefondet['ownership'].between(ownership, 100)]


st.title('Oljefondet 💰')

r1_c1, r1_c2 = st.columns(2)
r2_c1, r2_c2 = st.columns(2)
r3_c1, r3_c2, r3_c3 = st.columns([1, 98, 1])
r4_c1, r4_c2 = st.columns(2)

with r1_c1:
    region = st.text_input('Region: ', placeholder='Ex. Oceania').strip()
with r1_c2:
    country = st.text_input('Country: ', placeholder='Ex. Australia').strip()
with r2_c1:
    name = st.text_input('Name: ', placeholder='Ex. NVIDIA Corp').strip()
with r2_c2:
    industry = st.text_input('Industry: ', placeholder='Ex. Technology').strip()
with r3_c2:
    market_value_selection = st.select_slider('Market Value', options=['-1 trillion', '-100 billion', '-10 billion', '-1 billion', '-100 million', '-10 million', '-1 million', '0', '1 million', '10 million', '100 million', '1 billion', '10 billion', '100 billion', '1 trillion'], value='0')
    selection_to_value = {
        '-1 trillion': -1_000_000_000_000,
        '-100 billion': -100_000_000_000,
        '-10 billion': -10_000_000_000,
        '-1 billion': -1_000_000_000,
        '-100 million': -100_000_000,
        '-10 million': -10_000_000,
        '-1 million': -1_000_000,
        '0': 0,
        '1 million': 1_000_000,
        '10 million': 10_000_000,
        '100 million': 100_000_000,
        '1 billion': 1_000_000_000,
        '10 billion': 10_000_000_000,
        '100 billion': 100_000_000_000,
        '1 trillion': 1_000_000_000_000
    }
    market_value = selection_to_value[market_value_selection]
with r4_c1:
    voting = st.slider('Voting', min_value=0, max_value=100, step=1)
with r4_c2:
    ownership = st.slider('Ownership', min_value=0, max_value=100, step=1)

# Create a copy of the original DataFrame
filtered = oljefondet.copy()

# Apply filtering if the user changed anything
if region:
    filtered = filtered[filtered['region'].str.contains(region, case=False, na=False)]

if country:
    filtered = filtered[filtered['country'].str.contains(country, case=False, na=False)]

if name:
    filtered = filtered[filtered['name'].str.contains(name, case=False, na=False)]

if industry:
    filtered = filtered[filtered['industry'].str.contains(industry, case=False, na=False)]

if market_value:
    filtered = filtered[filtered['market_value'] >= market_value]

if voting:
    filtered = filtered[filtered['voting'] >= voting]

if ownership:
    filtered = filtered[filtered['ownership'] >= ownership]

st.dataframe(filtered, hide_index=True)