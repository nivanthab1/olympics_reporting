#Below functions are to render the page for the Olympics reporting app
#=================================================================================================

#Importing libraries
import streamlit as st
from pathlib import Path
from PIL import Image

#Function to render homepage
def basic_render():

    #Getting path of favicon image
    file_directory = Path(__file__).parent.parent
    logo = Image.open(file_directory / 'inputs' / 'Browser Icon Reverse.png')
    
    #Configuring Streamlit page
    st.set_page_config(page_title = 'Olympics Reporting Application',
                       page_icon = logo,
                       layout = "wide",
                       initial_sidebar_state="expanded")
    
    #Creating container with columns for page heading, specific title and logo
    with st.container():
        col1, col2, padding = st.columns([12,1,1])

        #Setting page header and subheader
        with col1:
            st.header("Summer Olympic Insights (Berlin 1936 - Tokyo 2020)")
            st.markdown("##### Explore the epic journey of the Summer Games with interactive, in-depth analysis and uncover the data stories behind the medals!")
            st.write("**Source: https://www.olympedia.org**")

        #Setting logo
        with col2:
            olympics_logo = Image.open(file_directory / 'inputs' / 'olympics.jpeg')
            st.image(olympics_logo, width=180, output_format='auto')

    #Horizontal divider
    st.divider()

#Function to create page footer
def page_footer():
    st.divider()
    st.write("**Product of NivAnalytics - https://www.nivanalytics.com**")
