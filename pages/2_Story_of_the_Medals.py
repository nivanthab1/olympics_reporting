#0) Importing libraries and setting up page
#==============================================================================================================================
import streamlit as st
from pathlib import Path
import pandas as pd
from modules.page_render import basic_render,page_footer,load_dataframe
from modules.reporting import create_medal_tally,medal_tally_vis, dynamic_medals_vis

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

#Depending on radio button selection, grouping of medal table is done by either Country or Sport
view_type = st.sidebar.radio("**Select view option**", options = ['Country','Sport'],horizontal=True)

st.subheader("Story of the Medals")

#Creating additional line spacing in sidebar
st.sidebar.write("\n")

#2a) Tabular output within expander
#==============================================================================================================================
with st.expander(f"**Medal Table by {view_type}**",expanded=True):

    #Creating medal table and rendering in Streamlit
    medal_df = create_medal_tally(df,view_type)
    st.dataframe(medal_df,use_container_width=True,hide_index=True)

#2b) Stacked bar chart for top 10 medal performance within expander
#==============================================================================================================================
with st.expander(f"**Top 10 Medal Performance by {view_type}**",expanded=True):

    st.write("\n")
    
    #Filtering to top 10 categories to allow meaningful visualisation
    top_10 = medal_df.loc[0:9,view_type]
    medal_df_top10 = medal_df[medal_df[view_type].isin(top_10)]

    #Preparing dataframe for visualisation by converting wide format medal_df to long format
    if 'Total' in medal_df.columns:
        stacked_df = pd.melt(medal_df_top10.drop(columns='Total'),id_vars=view_type,var_name = 'Medal', value_name = 'Count')
        sorted_field = medal_df_top10.sort_values('Total',ascending=False)[view_type].tolist()
    
    else:
        stacked_df = pd.melt(medal_df_top10,id_vars=view_type,var_name = 'Medal', value_name = 'Count')
        sorted_field = medal_df_top10.sort_values('🥇 Gold',ascending=False)[view_type].tolist()

    #Creating medal tally visualisation
    medal_tally_vis(stacked_df,sorted_field,view_type)

#2c) Bar chart of gold medal winners over Olympic Games within expander
#==============================================================================================================================

#This visualisation should only appear if All Games selected and more than one Olympics present
if games=='All' and df['Olympics'].nunique()!=1:

    with st.expander(f"**Olympic Games Progression: Gold Medals by {view_type}**",expanded=True):
            
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

        #Preparing dataframe for visualisation by converting wide format to long format
        stacked_df = pd.melt(dynamic_chart_df[[view_type,'🥇 Gold']], id_vars=view_type, value_name='Count')
        stacked_df.drop(columns='Position',inplace=True)
        stacked_df = stacked_df.sort_values(by='Count',ascending=False)

        #Creating sorted field based on gold medal count for visualisation
        sorted_field = stacked_df[view_type].tolist()

        #Calculating maximum value + 10% in scale at slider end to scale visualisation accordingly
        max_range = create_medal_tally(df,view_type).loc[0,'🥇 Gold']*1.1

        #Creating dynamic visualisation with slider selection
        dynamic_medals_vis(stacked_df,sorted_field,view_type,max_range)

#2d) Bar chart of gold medals winners over Day of Olympic Games within expander
#==============================================================================================================================

#This visualisation should only appear if more than one day of games present
if df['Day of Games'].nunique()!=1:

    with st.expander(f"**Day-by-day Progression: Gold Medals by {view_type}**",expanded=True):

        #Creating sorted list of Day of Games to assign to slider options
        sorted_day = list(sorted(df['Day of Games'].unique().astype(int)))

        #Creating slider of Day of Olympic games
        end_day = st.select_slider("Day of Games",options = sorted_day)

        #Creating list of all days from first to last selected
        try:
            all_days = sorted_day[:sorted_day.index(end_day)+1]
        except:
            st.write("Error")
    
        #Filtering dataframe for selected Day of Olympic games and top 10 countries
        day_games_df = df[(df['Day of Games'].astype(int).isin(all_days)) & (df[view_type].isin(top_10))].copy()
   
        #Creating dynamic_chart_df
        dynamic_chart_df = create_medal_tally(day_games_df,view_type)

        #Preparing dataframe for visualisation by converting wide format to long format
        stacked_df = pd.melt(dynamic_chart_df[[view_type,'🥇 Gold']], id_vars=view_type, value_name='Count')
        stacked_df.drop(columns='Position',inplace=True)
        stacked_df = stacked_df.sort_values(by='Count',ascending=False)

        #Creating sorted field based on gold medal count for visualisation
        sorted_field = stacked_df[view_type].tolist()

        #Calculating maximum value + 10% in scale at slider end to scale visualisation accordingly
        max_range = medal_df.loc[0,'🥇 Gold']*1.1

        #Creating dynamic visualisation with slider selection
        dynamic_medals_vis(stacked_df,sorted_field,view_type,max_range)

#Creating page footer
page_footer()