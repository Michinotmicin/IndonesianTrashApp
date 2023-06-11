import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import webbrowser
import altair as alt
import plotly.graph_objects as go
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

# HOME
if selected == "Home":
    st.sidebar.caption("Author: Michelle Tsjin")

    # Define a function to open the webpage
    def source_home():
        webbrowser.open("https://datacatalog.worldbank.org/search/dataset/0039597")
    # Add widgets to the sidebar
    st.sidebar.markdown("## Source of data for Homepage")
    if st.sidebar.button("The World Bank [Link]"):
        source_home()

    st.sidebar.markdown("## Analytical Methods")
    st.sidebar.markdown("The analysis is conducted by observing and utilizing bar charts, pie charts, and line charts for both \
                        the Home page and Dashboard page.")

    st.markdown("<span style='font-size: 25px;'>__Background Information__</span>", unsafe_allow_html=True)
    st.markdown("Waste management and environmental sustainability are critical global concerns. As human activities continue \
                to generate significant amounts of waste, exploring effective strategies for waste reduction and disposal \
                becomes imperative. Recycling has gained increasing attention as a key component of waste management due to \
                its potential positive impact on reducing the volume of waste that ends up in landfills. By collecting, \
                processing, and converting discarded materials into new products, recycling reduces the need for raw materials \
                and decreases waste accumulation. This paper aims to investigate whether the increase in recycling will affect \
                reducing the volume of waste that ends up in landfills, with a specific focus on Indonesia.")
    annotated_text(
    "Now, aren't you curious which country ranks at the top in terms of donating waster?      ",
    ("The World Bank", ""),)
    st.write("")

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
    selected_countries = st.multiselect('Choose Countries:', final_df_waste['country_name'], default=all_countries)

    # Filter the DataFrame based on the selected countries
    filtered_df = final_df_waste[final_df_waste['country_name'].isin(selected_countries)]

    st.markdown("<h4 style='text-align: center;'>Total Waste Produced by Countries in 2019</h4>",unsafe_allow_html=True)

    color_scale = alt.Scale(domain=['China', 'Indonesia', 'Others', 'United States', 'India', 'Brazil', 'Russian Federation', \
                                    'Mexico', 'Germany', 'Japan', 'France'],
                         range=['#2b758e', '#ffa600', '#ff6361', '#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3', \
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
        st.metric("TOP 1", "CHINA", "-395,081,376 ton ")
    with col_metric2:
        st.metric("AVERAGE", "OTHERS", "4,072,490.89")
    with col_metric3:
        st.metric("TOP 5", "INDONESIA", "-65,200,000")
        
    st.write(" ")
    st.write(" ")
    st.markdown("<span style='font-size: 25px;'>**Hypothesis**</span>", unsafe_allow_html=True)
    st.warning("Does the increase in recycling have an effect on reducing the volume of waste that ends up in Indonesia landfills? \
                \n\n Apakah dengan meningkatkan daur ulang, dapat mengurangi volume sampah yang berakhir di Tempat Pembuangan Akhir (TPA) Sampah Indonesia?")

# DASHBOARD
if selected == "Dashboards":
    st.sidebar.caption("Author: Michelle Tsjin")

    # Hypotheses
    st.sidebar.markdown("## Hypothesis")
    st.sidebar.info("Does the increase in recycling have an effect on reducing the volume of waste that ends up in Indonesia landfills? \
                   \n\n Apakah dengan meningkatkan daur ulang, dapat mengurangi volume sampah yang berakhir di Tempat Pembuangan Akhir (TPA) Sampah Indonesia?")

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
        st.markdown("#### SOUTH KOREA")
        annotated_text(
        "is ranked number 1 in terms of waste management and recycling. They are able to ", ("recycle", "60%"), \
        "of their generated waste, which resulted to ", ("only", "0.12%"), " of the trash ended up in the landfill ",
        "",)

    with col4:
        st.write("")

    with col5:
        st.markdown("#### South Korea Recycling System")
        st.write("")
        st.markdown("South Korean government is implementing **Extended Procedure Responsibility (EPR)** \
                    which is about strengthening the producer's responsibility from the production stage up to collection \
                    and recycling. What type of packaging or trash the EPR system is applied? The EPR system is applied to \
                    four packaging materials: **paper packaging, glass bottles, metal cans, and plastic packaging**")
    st.write("")
    st.write("")
    st.warning("The question now is whether Indonesia can adopt Korea's proven best recycling methods. \
               Additionally, can Indonesia achieve a recycling rate of 60% by recycling its current waste to minimize \
               the amount of trash ending up in landfills?")

    col1, col2, col3, col4, col5 = st.columns([2.4,0.2,0.8,0.2,1.4])
    col11, col22, col33 = st.columns([2.4,0.2,2.4])

    TrashComposition = pd.read_excel("TrashCompositionClean.xlsx")
    
    with col11:
        st.sidebar.markdown("## Trash Composition Parameter")
        selected_year = st.sidebar.selectbox('Select Year', TrashComposition['Tahun'].unique())

        # Filter the DataFrame based on the selected year
        filtered_df = TrashComposition[TrashComposition['Tahun'] == selected_year]

        # Calculate the total for each column
        total_per_column = filtered_df.iloc[:, 2:].sum()

        # Create the pie chart using Plotly
        fig = go.Figure(data=go.Pie(
            labels=total_per_column.index,
            values=total_per_column.values,
            hoverinfo='label+value',
            textinfo='percent',
            hovertemplate='%{label}: %{value:.2f}',
        ))

        st.markdown(f"#### Trash Composition in {selected_year}")
        st.write("Based on the Indonesian trash composition, if South Korean EPR is implemented by assuming that all plastic, \
                 metal, paper, and glass can be effectively recycled, the average recyclable portion of these materials \
                 from 2019 to 2022 will be 31%. ")

        # Display the chart
        st.plotly_chart(fig, use_container_width=True)

    with col22:
        st.write("")

    with col33:
        st.markdown("#### Prediction Landfill If Proper Recycling is Done")
        st.write("By applying the recycling rate to the current Indonesian landfill data, a significant decrease \
                 in the amount of trash ending up in landfills can be expected.")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        
        TPA_df = pd.read_excel("Recyled_TPA_Clean.xlsx")
                
        # Bar Chart
        bar_chart = alt.Chart(TPA_df).mark_bar(color='lightgrey').encode(
            alt.X('Tahun:O', axis=alt.Axis(format='d'), title='Year'),
            y=alt.Y('TimbulanSampahTahunan', title='Landfill (Ton)'),
            tooltip=[alt.Tooltip('Tahun', title='Year'), alt.Tooltip('TimbulanSampahTahunan', title='Current Landfill')]
        ).properties(
            width=450,
            height=400
        )

        # Create the line chart
        line_chart = alt.Chart(TPA_df).mark_line(color='purple').encode(
            alt.X('Tahun:O', axis=alt.Axis(format='d'), title='Year'),
            y=alt.Y('TimbulanSampahTahunan', title='Landfill (Ton)'),
            tooltip=[alt.Tooltip('Tahun', title='Year'), alt.Tooltip('TimbulanSampahTahunan', title='Current Landfill')]
        ).properties(
            width=450,
            height=400
        )

        # Bar Chart Prediciton
        bar_char_pred = alt.Chart(TPA_df).mark_bar(color='#3b518a').encode(
            alt.X('Tahun:O', axis=alt.Axis(format='d'), title='Year'),
            y=alt.Y('PredictionRecyling', title='Landfill (Ton)'),
            tooltip=[alt.Tooltip('Tahun', title='Year'), alt.Tooltip('PredictionRecyling', title='Prediction Landfill ')]
        ).properties(
            width=450,
            height=400
        )

        # Line Chart Prediction
        line_chart_pred = alt.Chart(TPA_df).mark_line(color='#fce725', strokeWidth=4).encode(
            alt.X('Tahun:O', axis=alt.Axis(format='d'), title='Year'),
            y=alt.Y('PredictionRecyling', title='Landfill (Ton)'),
            tooltip=[alt.Tooltip('Tahun', title='Year'), alt.Tooltip('PredictionRecyling', title='Prediction Landfill')]
        ).properties(
            width=450,
            height=400
        )

        # Combine the bar chart and line chart
        combined_chart = bar_chart + line_chart + bar_char_pred + line_chart_pred

        st.altair_chart(combined_chart, use_container_width=True)

    # Define a function to open the webpage
    def source_dash1():
        webbrowser.open("https://sensoneo.com/global-waste-index/")
    def source_dash2():
        webbrowser.open("https://wedocs.unep.org/bitstream/handle/20.500.11822/9031/-Korea%20Environmental%20Policy%20Bulletin%20-%20Extended%20Producer%20Responsibility%20(EPR)-2010Extended%20Producer%20Responsibility_KEPB2010.pdf?sequence=3&amp%3BisAllowed=")
    def source_dash3():
        webbrowser.open("https://sipsn.menlhk.go.id/sipsn/public/data/komposisi")
    def source_dash4():
        webbrowser.open("https://sipsn.menlhk.go.id/sipsn/public/data/capaian#")
    # Add widgets to the sidebar
    st.sidebar.markdown(" ## Source of data for Dashboard")
    if st.sidebar.button("Global Waste Index 2022"):
        source_dash1()
    if st.sidebar.button("South Korea Recycling System"):
        source_dash2()
    if st.sidebar.button("Indonesia Trash Composition"):
        source_dash3()
    if st.sidebar.button("Indonesia's Landfill Data"):
        source_dash4()

# SUMMARY
if selected == "Summary":
    # Hypotheses
    st.markdown("### Hypothesis")
    st.info("Does the increase in recycling have an effect on reducing the volume of waste that ends up in Indonesia landfills? \
                   \n\n Apakah dengan meningkatkan daur ulang, dapat mengurangi volume sampah yang berakhir di Tempat Pembuangan Akhir (TPA) Sampah Indonesia?")

    st.markdown("### Findings")
    st.warning("If South Korea's recycling method, known as Extended Producer Responsibility (EPR), is implemented in \
               Indonesia, focusing on recycling paper packaging, glass bottles, metal cans, and plastic packaging, it is \
               predicted that an average of 31% of the current landfill waste can be effectively recycled based on acquired \
               data from Indonesia's trash composition and landfill quantities from 2019 to 2022. This implementation would \
               significantly decrease the amount of trash ending up in Indonesian landfills in the coming years.")

    st.markdown("### Future Topics")
    st.success("Can recycling improve a country's economy? Exploring the Circular Economy concept.")


# CONTACT
if selected == "Contact":
    st.markdown("#### Author")
    st.markdown("Hi 👋, my name is **Michelle Tsjin**, and I am currently an undergraduate student studying Data Science \
                and Big Data Technology with a focus on Contemporary Entrepreneurialism. If you're interested in getting \
                to know me better, please find more information below:")
    
    def linkedin():
        webbrowser.open("https://www.linkedin.com/in/michelle-tsjin/")
    if st.button("Linkedin"):
        linkedin()

    st.write("")
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
