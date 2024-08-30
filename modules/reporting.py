#Importing libraries
import pandas as pd
import streamlit as st
import altair as alt

#=================================================================================================
#Medal tally table
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

#=================================================================================================
#Medal tally visualisation
def medal_tally_vis(df,sort_order,view_type):

    #Creating stacked bar chart with selected categories with Altair customisation
    bar_chart = alt.Chart(df).mark_bar().encode(x=alt.X('Count:Q',stack='zero',axis=None),
                                                                y=alt.Y(f'{view_type}:N',sort=sort_order,axis=alt.Axis(labelFontWeight='bold')),
                                                                color=alt.Color('Medal:N', scale=alt.Scale(domain=['🥇 Gold', '🥈 Silver', '🥉 Bronze'], 
                                                                                                            range=['#FFD700','#C0C0C0','#CD7F32'])),
                                                                tooltip=[f'{view_type}:N','Medal:N',
                                                                            alt.Tooltip('Count:Q',format=',')]).properties(height=500)


    #Display the chart in a scrollable container
    return st.altair_chart(bar_chart, theme="streamlit", use_container_width=True)

#=================================================================================================
#Dynamic medal tally visualisation
def dynamic_medals_vis(df,sort_order,view_type,max_range):

    #Creating stacked bar chart with selected categories with Altair customisation
    bar_chart = alt.Chart(df).mark_bar(color='#FFD700').encode(x=alt.X('Count:Q',axis=None, scale=alt.Scale(domain=[0, max_range])),
                                                                y=alt.Y(f'{view_type}:N',sort=sort_order,axis=alt.Axis(labelFontWeight='bold')),
                                                                tooltip=[f'{view_type}:N',
                                                                         alt.Tooltip('Count:Q',format=',')]).properties(height=500)
    
    #Creating the text labels
    text = bar_chart.mark_text(
        align="left",
        baseline='middle',
        dx=3,  #Adjusting the position to move text slightly to the right of the bar
        size=12, #Increasing text size
        fontWeight='bold').encode(text=alt.Text('Count:Q', format=','))  #Displaying the count as text

    #Combining the bar chart and text labels
    final_chart = bar_chart + text

    #Display the chart in a scrollable container
    return st.altair_chart(final_chart, theme="streamlit", use_container_width=True)

#=================================================================================================
#Event performance visualisation
def event_performance_vis(df,sort_order,field,min_val,max_val):

    #Creating stacked bar chart with selected categories with Altair customisation
    line_chart = alt.Chart(df).mark_line(point=True).encode(x=alt.X('Olympics:N',sort=sort_order),
                                                                y=alt.Y(f'{field}:Q', scale=alt.Scale(domain=[min_val,max_val]),),
                                                                tooltip=['Olympics:N',f'{field}:Q','Athlete:N','Country:N']).properties(height=500)
    #Display the chart in a scrollable container
    return st.altair_chart(line_chart, theme="streamlit", use_container_width=True)