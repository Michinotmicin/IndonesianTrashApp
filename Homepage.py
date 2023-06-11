import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import webbrowser
import altair as alt
import locale
import re
from streamlit_option_menu import option_menu
from annotated_text import annotated_text

# Set the page width
st.set_page_config(
    page_title="Hello",
    layout="wide"
)

selected = option_menu(
    menu_title=None, # required
    options=["Home", "Dashboards", "Summary", "Contact"],
    icons=["house", "speedometer2", "card-text", "envelope"],
    menu_icon="cast", 
    default_index=0,
    orientation="horizontal",
     styles={
    "nav-link": {
        "--hover-color": "#eee",
        "--active-background-color": "#eee",
    },
    "nav-link-selected": {"background-color": "#003f5c"},
    },
)

if selected == "Home":
    # Define a function to open the webpage
    def source_home():
        webbrowser.open("https://datacatalog.worldbank.org/search/dataset/0039597")
    # Add widgets to the sidebar
    st.sidebar.title(f"Source of data for Homepage")
    if st.sidebar.button("The World Bank [Link]"):
        source_home()

    st.markdown("<span style='font-size: 25px;'>__Background Information__</span>", unsafe_allow_html=True)
    annotated_text(
    "Aren't you curious which country __ranks at the top__ in terms of __donating waste__?      ",
    ("The World Bank", ""),)

    # Data Top Waste
    df_waste = pd.read_csv("country_level_data_0.csv")

    # Take and create the TOP 10 and Others
    sorted_df = df_waste.sort_values('total_msw_total_msw_generated_tons_year', ascending=False)
    top_10_countries = sorted_df.head(10)
    # Calculate the average of 'total_msw_total_msw_generated_tons_year' for the remaining countries
    average_value = sorted_df.iloc[10:, sorted_df.columns.get_loc('total_msw_total_msw_generated_tons_year')].mean()
    # Create a new row for 'Others' with the average value
    others_row = pd.DataFrame({'country_name': ['Others'], 'total_msw_total_msw_generated_tons_year': [average_value]})
    # Set other columns to null/NaN
    others_row = others_row.reindex(columns=df_waste.columns)

    # Concatenate the top 10 countries DataFrame and the 'Others' row
    final_df_waste = pd.concat([top_10_countries, others_row])

    # Add 'rank' column with ranking
    final_df_waste['rank'] = final_df_waste['total_msw_total_msw_generated_tons_year'].rank(ascending=False)
    # Set the rank value for 'Others' as '-'
    final_df_waste.loc[final_df_waste['country_name'] == 'Others', 'rank'] = 11

    # Default ALL & Multiselect
    all_countries = final_df_waste['country_name'].tolist()
    selected_countries = st.multiselect('**Choose Countries:**', final_df_waste['country_name'], default=all_countries)

    # Filter the DataFrame based on the selected countries
    filtered_df = final_df_waste[final_df_waste['country_name'].isin(selected_countries)]

    st.markdown("<h4 style='text-align: center;'>Total Waste Produced by Countries in 2019</h4>",unsafe_allow_html=True)

    color_scale = alt.Scale(domain=['China', 'Indonesia', 'Others', 'United States', 'India', 'Brazil', 'Russian Federation', \
                                    'Mexico', 'Germany', 'Japan', 'France'],
                         range=['#58508d', '#ffa600', '#ff6361', '#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3', \
                                '#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3'])

    # Create the bar chart using Altair
    chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X('country_name:N', title='Country', axis=alt.Axis(labelAngle=-55)),
        y=alt.Y('total_msw_total_msw_generated_tons_year:Q', title='Total Waste (tons/year)'),
        color=alt.Color('country_name:N', scale=color_scale, legend=None),
        tooltip=[
            alt.Tooltip('rank:O', title='Rank', format=".0f"),
            alt.Tooltip('country_name:N', title='Country'),
            alt.Tooltip('total_msw_total_msw_generated_tons_year:Q', title='Total Waste (tons/year)', format=".2f")
        ]
    ).properties(
        width=800, 
        height=600
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )

    # Display the chart
    st.altair_chart(chart, use_container_width=True)

    st.write('')

    
    st.markdown("<span style='font-size: 25px;'>**Insights**</span>", unsafe_allow_html=True)
    col_metric1, col_metric2, col_metric3 = st.columns(3)
    with col_metric1:
        st.metric("__TOP 1__", "CHN", "-395,081,376 ton ")
    with col_metric2:
        st.metric("__AVG__", "OTHERS", "4,072,490.89")
    with col_metric3:
        st.metric("__TOP 5__", "INA", "-65,200,000")
        

    st.markdown("<span style='font-size: 25px;'>**Hypothesis**</span>", unsafe_allow_html=True)
    st.warning("Does the increase in recycling have an effect on reducing the volume of waste that ends up in landfills? \
               \n\n Apakah dengan meningkatkan daur ulang, dapat mengurangi volume sampah yang berakhir di Tempat Pembuangan Akhir (TPA) Sampah?")

if selected == "Dashboards":
    # Hypotheses
    st.sidebar.markdown("## Hypothesis")
    st.sidebar.info("Does the increase in recycling have an effect on reducing the volume of waste that ends up in landfills? \
                   \n\n Apakah dengan meningkatkan daur ulang, dapat mengurangi volume sampah yang berakhir di Tempat Pembuangan Akhir (TPA) Sampah?")

    # Define a function to open the webpage
    def source_dash1():
        webbrowser.open("https://sensoneo.com/global-waste-index/")
    def source_dash2():
        webbrowser.open("https://wedocs.unep.org/bitstream/handle/20.500.11822/9031/-Korea%20Environmental%20Policy%20Bulletin%20-%20Extended%20Producer%20Responsibility%20(EPR)-2010Extended%20Producer%20Responsibility_KEPB2010.pdf?sequence=3&amp%3BisAllowed=")
    # Add widgets to the sidebar
    st.sidebar.markdown(" ## Source of data for Dashboard")
    if st.sidebar.button("Global Waste Index 2022"):
        source_dash1()
    if st.sidebar.button("South Korea Recycling System"):
        source_dash2()

    st.write("")

    annotated_text(
    "As mentioned earlier, according to government data on total landfill waste,", ("Indonesia ranks 5th", ""), " among the \
    countries that produce", ("the most waste.", ""), " Now, are you curious to know which country ",
    ("tops the list regarding recycling", "?."),)

    st.write("")

    col1, col2, col3, col4, col5 = st.columns([2.4,0.2,0.8,0.2,1.4])

    with col1:
        st.markdown('<h5 style="text-align: center;">Top 8 - Waste Management & Recycling in 2022</h5>', unsafe_allow_html=True)

        GlobalRecycling = pd.read_excel("Sensoneo_FullDatasetGlobalWasteIndex.xlsx")

        # Data Pre-processing or Data Cleaning
        # Replace spaces, "/", "(", and ")" with underscores in column names
        GlobalRecycling.columns = [re.sub(r"\s+|/|\(|\)", "_", col).replace("__", "_").strip("_") for col in GlobalRecycling.columns]
        top_countries_GR = GlobalRecycling.sort_values('Rank').head(8)

        top_countries_GR['Waste_Generated_Calculated'] = top_countries_GR['Waste_Generated_kg'] - top_countries_GR['Recycling_kg'] - top_countries_GR['Landfill_kg']

        chart = alt.Chart(top_countries_GR).mark_bar().encode(
            x=alt.X('Country:N', title='Country'),
            y=alt.Y('Waste_Generated_kg:Q', title='Total Waste (kg)'),
            color=alt.Color('Recycled_Generated:Q', title="Recycling Rate", scale=alt.Scale(scheme='viridis')),
            tooltip=[
            alt.Tooltip('Country:N'),
            alt.Tooltip('Waste_Generated_kg:Q', title='Waste Generated (kg)'),
            alt.Tooltip('Recycled_Generated:Q', title='Recycling Rate'),
            alt.Tooltip('Recycling_kg:Q', title='Recycled (kg)'),
            alt.Tooltip('Landfill_kg:Q', title='Landfill (kg)')
        ])

        # Display the chart in Streamlit
        st.altair_chart(chart, use_container_width=True)
                    
    with col2: 
        st.write("")

    with col3:
        st.markdown("**INSIGHTS**")
        st.markdown("##### SOUTH KOREA")
        annotated_text(
        "is ranked number 1 in terms of waste management and recycling. They are able to ", ("recycle", "60%"), \
        "of their generated waste, which resulted to ", ("only", "0.12%"), " of the trash ended up in the landfill ",
        "",)

    with col4:
        st.write("")

    with col5:
        st.write("###### South Korea Recycling System")


    col11, col22, col33 = st.columns(3)
    
    with col11:
        st.write("t")

    with col22:
        st.write("t")

    with col33:
        st.write("t")


    
    
if selected == "Summary":
    st.title(f"You have selected {selected}")


if selected == "Contact":
    # di sidebar taro hypothesis and findings!

    # maybe add What I do

    st.title(f"You have selected {selected}")

    st.markdown("#### 📩 Get In Touch With Me!")


    contact_form = """
    <form action="https://formsubmit.co/michelletsjin020@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here"></textarea>
        <button type="submit">Send</button>
    </form>
    """

    st.markdown(contact_form, unsafe_allow_html=True)

    # Use Local CSS File
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    local_css("style/style.css")
