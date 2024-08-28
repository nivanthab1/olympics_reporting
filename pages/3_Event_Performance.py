#Importing libraries
import streamlit as st
from pathlib import Path
import pandas as pd
from modules.page_render import basic_render,page_footer,load_dataframe
from modules.visualisations import event_performance_vis

#Rendering page
basic_render("No")

#Initialising session state variable with loaded dataframe
st.session_state['df'] = load_dataframe()

#Recalling df from session state
df = st.session_state['df']

#Event performance section 
#==============================================================================================================================

#Initially, filtering for either time or scored events
event_performance_df = df[(df['Score'].notnull() | (df['Time(s)'].notnull()))].copy()

#Secondary filtering to selected sports
event_performance_df = event_performance_df[event_performance_df['sport'].isin(['Athletics','Swimming','Diving','Artistic Gymnastics','Canoe Slalom','Trampolining'])]

#Section descriptions
st.subheader("Event Performance")
st.write("Discover how Olympic champions' performances have evolved over the years, from record-breaking times to higher scores. Select a sport and event to see the trends and improvements among gold medalists across different Olympic Games.")
st.write('\n')

#Creating selectbox to choose sport
sport = st.sidebar.selectbox("**Sport**", index=None, options = sorted(event_performance_df['Sport'].unique()))

#Performs the below if sport selected
if sport is not None:

    #Filtering dataframe for selected sport
    event_performance_df = event_performance_df[event_performance_df['Sport']==sport]

#Creating selectbox to choose event name
event_name = st.sidebar.selectbox("**Event Name**", index=None, options = sorted(event_performance_df['Event Name'].unique()))

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