#Importing libraries
import streamlit as st
from pathlib import Path
import pandas as pd
from modules.page_render import basic_render,page_footer
from modules.analysis_tables import create_medal_tally
from modules.visualisations import medal_tally_vis, dynamic_medals_vis

#Rendering page
basic_render("No")

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

#Medal history section 
#==============================================================================================================================

st.subheader("Story of the Medals")

#Creating additional line spacing in sidebar
st.sidebar.write("\n")

#Depending on radio button selection, medal_df is grouped by either Country or Sport
view_type = st.sidebar.radio("**Select view option**", options = ['Country','Sport'],horizontal=True)
medal_df = create_medal_tally(df,view_type)

#Creating sorted field list based on Total count for visualisation
sorted_field = medal_df.sort_values('Total',ascending=False)[view_type].tolist()

#Tabular output within expander
with st.expander(f"**Medal Table by {view_type}**",expanded=True):

    #Displaying medal table
    st.dataframe(medal_df,use_container_width=True,hide_index=True)

#Stacked bar chart within expander
with st.expander(f"**Visualisation of Top 10 by {view_type}**",expanded=True):

    st.write("\n")
    
    #Filtering to top 10 categories to allow meaningful visualisation
    top_10 = medal_df.loc[0:9,view_type]
    medal_df = medal_df[medal_df[view_type].isin(top_10)]

    #Preparing dataframe for visualisation by converting wide format medal_df to long format
    stacked_df = pd.melt(medal_df.drop(columns='Total'),id_vars=view_type,var_name = 'Medal', value_name = 'Count')

    #Creating medal tally visualisation
    medal_tally_vis(stacked_df,sorted_field,view_type)

#This visualisation should only appear if All Games selected
if games=='All':

    #Bar chart of gold medal winners over Olympic Games within expander
    with st.expander(f"**Visualisation of Cumulative Gold Medals by {view_type} Across Olympic Games**",expanded=True):
            
        #Creating slider of Olympic games
        end_game = st.select_slider("Olympic Games",options = df['Olympics'].unique(),label_visibility='hidden')

        #Obtaining index of last games selected
        end_game = list(df['Olympics'].unique()).index(end_game)
        
        #Creating list of all games from first to last selected
        all_games = list(df['Olympics'].unique())[0:end_game+1]

        #Filtering dataframe for selected Olympic games and top 10 countries
        olympic_games_df = df[(df['Olympics'].isin(all_games)) & (df[view_type].isin(top_10))].copy()

        #Creating dynamic_chart_df
        dynamic_chart_df = create_medal_tally(olympic_games_df,view_type)

        #Preparing dataframe for visualisation by converting wide format medal_df to long format
        stacked_df = pd.melt(dynamic_chart_df[[view_type,'🥇 Gold']], id_vars=view_type, value_name='Count')
        stacked_df.drop(columns='Position',inplace=True)
        stacked_df = stacked_df.sort_values(by='Count',ascending=False)

        #Creating sorted field based on gold medal count for visualisation
        sorted_field = stacked_df[view_type].tolist()

        #Creating dynamic visualisation with slider selection
        dynamic_medals_vis(stacked_df,sorted_field,view_type)

#Bar chart of gold medals winners over Day of Olympic Games within expander
with st.expander(f"**Visualisation of Cumulative Gold Medals by {view_type} Across Day of Olympic Games**",expanded=True):

    #Creating slider of Day of Olympic games
    end_day = st.select_slider("Day of Games",options = df['Day of Games'].unique().astype(int),label_visibility='hidden')

    #Creating list of all days from first to last selected
    try:
        all_days = list(df['Day of Games'].unique())[0:end_day+1]
    except:
        st.write("Error")

    #Filtering dataframe for selected Day of Olympic games and top 10 countries
    day_games_df = df[(df['Day of Games'].isin(all_days)) & (df[view_type].isin(top_10))].copy()

    #Creating dynamic_chart_df
    dynamic_chart_df = create_medal_tally(day_games_df,view_type)

    #Preparing dataframe for visualisation by converting wide format medal_df to long format
    stacked_df = pd.melt(dynamic_chart_df[[view_type,'🥇 Gold']], id_vars=view_type, value_name='Count')
    stacked_df.drop(columns='Position',inplace=True)
    stacked_df = stacked_df.sort_values(by='Count',ascending=False)

    #Creating sorted field based on gold medal count for visualisation
    sorted_field = stacked_df[view_type].tolist()

    #Creating dynamic visualisation with slider selection
    dynamic_medals_vis(stacked_df,sorted_field,view_type)

#Creating page footer
page_footer()