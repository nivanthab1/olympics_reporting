#Importing libraries
import streamlit as st
from pathlib import Path
import pandas as pd
from modules.page_render import basic_render,page_footer,load_dataframe
from modules.visualisations import event_performance_vis

#Rendering page
basic_render("No")

#Checking if dataframe in session state. If not, load dataframe
if 'df' not in st.session_state:
    st.session_state['df'] = load_dataframe()

#Recalling df from session state
df = st.session_state['df']

#Event performance section 
#==============================================================================================================================

#Initially, filtering for either time or scored events
event_performance_df = df[(df['Score'].notnull() | (df['Time(s)'].notnull()))].copy()

#Secondary filtering to selected sports
event_performance_df = event_performance_df[event_performance_df['sport'].isin(['Athletics','Swimming','Diving','Artistic Gymnastics'])]

#Creating columns to display subheader and radio buttons separately with suitable column spacing
col1,col2,col3 = st.columns([10,5,7])

with col1:
    st.subheader("Event Performance")

#Creating selectbox to choose sport
with col2:
    sport = st.selectbox("**Select sport**", index=None, options = sorted(event_performance_df['Sport'].unique()))

#Performs the below if sport selected
if sport is not None:

    #Filtering dataframe for selected sport
    event_performance_df = event_performance_df[event_performance_df['Sport']==sport]

#Creating selectbox to choose event name
with col3:
    event_name = st.selectbox("**Select event name**", index=None, options = sorted(event_performance_df['Event Name'].unique()))

#Performs the below if event_name selected
if event_name is not None:

    #Filtering dataframe for selected event name and winners
    event_performance_df = event_performance_df[(event_performance_df['Event Name']==event_name) & (event_performance_df['Position']=='1')]
    
    #Identify if event is timed or scored
    if len(event_performance_df[event_performance_df['Score'].isnull()])>0:
        field = 'Time(s)'
    
    else:
        field = 'Score'

    #Calculating minimum and maximum values for chart y-axis range
    min_val = event_performance_df[field].min()
    max_val = event_performance_df[field].max()

    #Sorting x-axis
    sorted_field = event_performance_df['Olympics'].unique()

    #Creating event performance visualisation
    event_performance_vis(event_performance_df,sorted_field,field,min_val,max_val)

#Creating page footer
page_footer()