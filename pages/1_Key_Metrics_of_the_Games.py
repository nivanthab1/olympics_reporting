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

#Gender ratio calculation
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

#Displaying calculated metrics in presentable format with suitable column spacing
col1, col2, col3 = st.columns([5,7,2])
col1.metric("**Olympic Games**",games)
col1.metric("**Sport**",sports)
col1.metric("**Number of Medalist Countries**",countries_count)
col2.metric("**Most Successful Country**",successful_country)
col2.metric(f"**Gold Medals Won by {successful_country}**",gold_count)
col2.metric("**Event Gender Ratio (Men : Women : Mixed)**",f"{men_ratio} : {women_ratio} : {mixed_ratio}")
col3.metric("**Number of Sports**",sport_count)
col3.metric("**Number of Events**",event_count)
col3.metric("**Number of Medalists**",athlete_count)

#Creating page footer
page_footer()