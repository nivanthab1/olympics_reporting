#Importing libraries
import streamlit as st
from pathlib import Path
import pandas as pd
from modules.page_render import basic_render,page_footer
from modules.analysis_tables import create_medal_tally
from modules.visualisations import medal_tally_vis, dynamic_medals_vis, event_performance_vis

#Rendering page
basic_render()

#File read and pre-processing
#==============================================================================================================================

#Setting path to input file to be read for analysis
file_directory = Path(__file__).parent
file_path = file_directory / 'inputs' / 'Olympics_Analysis_Data.pkl'

#Reading into pandas dataframe
df = pd.read_pickle(file_path)

#Filtering out older Olympics games
df = df[df['olympics_name'].isin(df['olympics_name'].unique()[9::])].reset_index()

#Filtering out Wushu from Olympics games
df = df[df['sport']!='Wushu'].reset_index()

#Renaming columns
df.rename(columns={'sports_emojis':'Sport',
                   'country_flag':'Country',
                   'event_name':'Event Name',
                   'clean_position':'Position',
                   'clean_time':'Time(s)',
                   'new_score':'Score',
                   'olympics_name':'Olympics',
                   'clean_athlete':'Athlete',
                   'day_of_games':'Day of Games'},inplace=True)

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

#Horizontal divider
st.divider()

#Medal history section 
#==============================================================================================================================

#Creating columns to display subheader and radio buttons separately with suitable column spacing
col1,col2 = st.columns([20,4.6])

with col1:
    st.subheader("Medal History")

#Depending on radio button selection, medal_df is grouped by either Country or Sport
with col2:
    view_type = st.radio("**Select view option**", options = ['Country','Sport'],horizontal=True)
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

#Horizontal divider
st.divider()

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