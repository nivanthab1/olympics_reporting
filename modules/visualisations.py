#Below functions are to create visualisations using Olympics data
#=================================================================================================

#Importing libraries
import pandas as pd
import streamlit as st
import altair as alt

#Medal tally visualisation
def medal_tally_vis(df,sort_order,view_type):

    #Creating stacked bar chart with selected categories with Altair customisation
    bar_chart = alt.Chart(df).mark_bar().encode(x=alt.X('Count:Q',stack='zero'),
                                                                y=alt.Y(f'{view_type}:N',sort=sort_order,axis=alt.Axis(labelFontWeight='bold')),
                                                                color=alt.Color('Medal:N', scale=alt.Scale(domain=['🥇 Gold', '🥈 Silver', '🥉 Bronze'], 
                                                                                                            range=['#FFD700','#C0C0C0','#CD7F32'])),
                                                                tooltip=[f'{view_type}:N','Medal:N',
                                                                            alt.Tooltip('Count:Q',format=',')]).properties(height=500)
    #Display the chart in a scrollable container
    return st.altair_chart(bar_chart, theme="streamlit", use_container_width=True)

#Dynamic medal tally visualisation
def dynamic_medals_vis(df,sort_order,view_type):

    #Creating stacked bar chart with selected categories with Altair customisation
    bar_chart = alt.Chart(df).mark_bar(color='#FFD700').encode(x=alt.X('Count:Q',axis=None, scale=alt.Scale(domain=[0, 900])),
                                                                y=alt.Y(f'{view_type}:N',sort=sort_order,axis=alt.Axis(labelFontWeight='bold')),
                                                                tooltip=[f'{view_type}:N',
                                                                         alt.Tooltip('Count:Q',format=',')]).properties(height=500)
    
    #Creating the text labels
    text = bar_chart.mark_text(
        align="left",
        baseline='middle',
        dx=3,  #Adjusting the position to move text slightly to the right of the bar
        size=12, #Increasing text size
        fontWeight='bold',
    ).encode(
        text=alt.Text('Count:Q', format=',')  #Displaying the count as text
    )

    #Combining the bar chart and text labels
    final_chart = bar_chart + text

    #Display the chart in a scrollable container
    return st.altair_chart(final_chart, theme="streamlit", use_container_width=True)

#Evemt performance visualisation
def event_performance_vis(df,sort_order,field,min_val,max_val):

    #Creating stacked bar chart with selected categories with Altair customisation
    line_chart = alt.Chart(df).mark_line(point=True).encode(x=alt.X('Olympics:N',sort=sort_order),
                                                                y=alt.Y(f'{field}:Q', scale=alt.Scale(domain=[min_val,max_val])),
                                                                tooltip=['Olympics:N',f'{field}:Q','Athlete:N','Country:N']).properties(height=500)
    #Display the chart in a scrollable container
    return st.altair_chart(line_chart, theme="streamlit", use_container_width=True)