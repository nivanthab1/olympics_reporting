#Importing libraries
import streamlit as st
from pathlib import Path
import pandas as pd
from modules.page_render import basic_render,page_footer,load_dataframe
from modules.analysis_tables import create_medal_tally

#Rendering page
basic_render("No")

#Initialising session state variable with loaded dataframe
st.session_state['df'] = load_dataframe()

#Recalling df from session state
df = st.session_state['df']

#Setting universal filters
#==============================================================================================================================

#Creating selectbox to select specific Olympic games
games = st.sidebar.selectbox("**Olympic Games**",options=(["All"] + list(df['Olympics'].unique())))

#Filtering to selected games
if games!='All':
    df = df[df['Olympics']==games]

#Creating selectbox to select specific sport
sports = st.sidebar.selectbox("**Sport**",options=(["All"] + sorted(list(df['Sport'].unique()))))

#Filtering to selected sport
if sports!='All':
    df = df[df['Sport']==sports]

#Key metrics section 
#==============================================================================================================================

st.subheader("Key Metrics of the Games")

#Creating medal_df using create_medal_tally function grouped by country for below metric calculations
medal_df = create_medal_tally(df,'Country')

#Calculating metrics to be displayed
countries_count = medal_df['Country'].nunique()
successful_country = medal_df.loc[0,'Country']
gold_count = medal_df.loc[0,'🥇 Gold'].astype(int)
sport_count = "{:,}".format(df['Sport'].nunique())
event_count = "{:,}".format(df['event_url'].nunique())
athlete_count = "{:,}".format(df['Athlete'].nunique())

#Calculating gender ratio
try:
    men_ratio = round((df['gender'].value_counts().get('Men')/df['gender'].value_counts().sum())*100,1).astype(int)
except:
    men_ratio = 0

try:
    women_ratio = round((df['gender'].value_counts().get('Women')/df['gender'].value_counts().sum())*100,2).astype(int)
except:
    women_ratio = 0

try:
    mixed_ratio = round((df['gender'].value_counts().get('Mixed')/df['gender'].value_counts().sum())*100,2).astype(int)
except:
    mixed_ratio = 0

#Calculating % of gold medals won by host country
mask = (df['host_country']==df['country']) & (df['Position']=='1')
host_country_win_perc = int((len(df[mask]) / df['event_url'].nunique())*100)

#Displaying calculated metrics in presentable format with suitable column spacing
col1, col2, col3 = st.columns([4,5,2])

col1.metric("**Olympic Games**",games)
col1.metric("**Olympic Sport**",sports)
col1.metric("**Most Successful Country**",successful_country)
col2.metric("**Host Country Gold Medal %**",host_country_win_perc)
col2.metric("**Gender Ratio (Men : Women : Mixed Event)**",f"{men_ratio} : {women_ratio} : {mixed_ratio}")
col2.metric(f"**Gold Medals Won by {successful_country}**",gold_count)
col3.metric("**Sports**",sport_count)
col3.metric("**Events**",event_count)
col3.metric("**Medals Awarded**",athlete_count)
#col3.metric("**Medalist Countries**",countries_count)

#Creating page footer
page_footer()