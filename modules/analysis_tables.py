#Below functions are to create analysis tables using Olympics data
#=================================================================================================

#Importing libraries
import pandas as pd
import streamlit as st

#Medal tally table and subsequent commentary
def create_medal_tally(df,view_type):

    #Pivoting df to obtain overall medal table and resetting index
    medal_df = pd.pivot_table(df,index=view_type,columns='Position',values='event_url',aggfunc='count').fillna(0).reset_index()

    #Renaming columns where they exist
    def rename_columns(medal_df):
        rename_dict = {
        '1': '🥇 Gold',
        '2': '🥈 Silver',
        '3': '🥉 Bronze'}

        medal_df.rename(columns={col: rename_dict.get(col, col) for col in medal_df.columns}, inplace=True)
        return medal_df
    medal_df = rename_columns(medal_df)

    #Creating total medal count column if Gold, Silver and Bronze columns are present
    if all(col in medal_df.columns for col in ['🥇 Gold','🥈 Silver','🥉 Bronze']):
        medal_df['Total'] = medal_df['🥇 Gold'] + medal_df['🥈 Silver'] + medal_df['🥉 Bronze']

    #Sorting medal table by gold medal count and resetting index
    medal_df = medal_df.sort_values(by='🥇 Gold',ascending=False).reset_index(drop=True)

    return medal_df