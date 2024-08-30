#0) Importing libraries and setting up page
#==============================================================================================================================
import streamlit as st
from pathlib import Path
import pandas as pd
from modules.page_render import basic_render,page_footer,load_dataframe
from modules.reporting import create_medal_tally

#Rendering page
basic_render("No")

#Initialising session state variable with loaded dataframe
st.session_state['df'] = load_dataframe()

#Recalling df from session state
df = st.session_state['df']

#1) Setting universal filters
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

#2) Calculating key metrics
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
medal_count = "{:,}".format(len(df))

#Calculating gender ratio
total_count = df['gender'].value_counts().sum()
men_ratio = int((df['gender'].value_counts().get('Men',0)/total_count)*100) if total_count >0 else 0
women_ratio = int((df['gender'].value_counts().get('Women',0)/total_count)*100) if total_count >0 else 0
mixed_ratio = int((df['gender'].value_counts().get('Mixed',0)/total_count)*100) if total_count >0 else 0

#Calculating % of gold medals won by host country
mask = (df['host_country']==df['ct']) & (df['Position']=='1')
host_country_win_perc = f"{int((len(df[mask]) / df['event_url'].nunique())*100)}%"

#3) Displaying calculated metrics in presentable format with suitable column spacing
#==============================================================================================================================
col1, col2, col3 = st.columns([4,5,3])

with col1:
    st.metric("**Olympic Games**",games)
    st.metric("**Olympic Sport**",sports)
    st.metric("**Host Country Gold Medal %**",host_country_win_perc,help="Gold medals won by the host country of the Games expressed as a percentage of all events")

with col2:
    st.metric("**Most Successful Country**",successful_country,help="Country with greatest medal tally of all-time")
    st.metric(f"**Gold Medals Won by {successful_country}**",gold_count)
    st.metric("**Medalist Gender Ratio (Men : Women : Mixed Event)**",f"{men_ratio} : {women_ratio} : {mixed_ratio}")

with col3: 
    st.metric("**Total Sports**",sport_count)
    st.metric("**Total Events**",event_count)
    st.metric("**Total Medals Awarded**",medal_count,help="Sum of all medals awarded across all countries and events")

#Creating page footer
page_footer()