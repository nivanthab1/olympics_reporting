#Below functions are to render the page for the Olympics reporting app
#=================================================================================================

#Importing libraries
import streamlit as st
from pathlib import Path
from PIL import Image

#Function to render homepage
def basic_render(home):

    #Getting path of favicon image
    file_directory = Path(__file__).parent.parent
    logo = Image.open(file_directory / 'inputs' / 'Browser Icon Reverse.png')
    
    #Configuring Streamlit page
    st.set_page_config(page_title = 'Olympic View',
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

    #Welcome page writeup in justified text if homepage
    if home=='Yes':

        st.subheader("Welcome to my Olympics Reporting Application!")

        st.markdown("""
                    <div style="text-align: justify;">
                    
                    As someone who's always been captivated by the fierce competition of the Olympics, I've combined my passion for the Games with my knack for data analytics to create this interactive platform. I've spent countless hours watching the powerhouses battle it out, and that drive led me to dive deep, uncovering the granular details that tell the story behind the Games, sports, events and medals.
                    
                    Building this application wasn’t just about pulling together data; it was a journey. It started with recognising the challenge of finding detailed, structured Olympic data—something that could be dissected and explored. From there, I rolled up my sleeves and got to work, extracting and refining the data with Python and Selenium, ensuring its quality, and then transforming it into something meaningful. The final step was developing this accessible and user-friendly app using Streamlit, so others could explore the same insights that have fascinated me.
                    
                    I hope this platform offers you a new perspective on the Olympics, allowing you to dig deeper into the stories that make the Games so compelling.""",unsafe_allow_html=True)

#Function to create page footer
def page_footer():
    st.divider()
    st.write("**Product of NivAnalytics - https://www.nivanalytics.com**")
