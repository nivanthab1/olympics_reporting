#Importing libraries
import streamlit as st
from pathlib import Path
import pandas as pd
from modules.page_render import basic_render,page_footer

#Rendering page
basic_render("Yes")

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

#Assigning df to session state variable to remain in memory across the application's pages
if 'df' not in st.session_state:
    st.session_state['df'] = df

#Creating page footer
page_footer()