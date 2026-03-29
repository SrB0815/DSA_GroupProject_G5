import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.markdown("""
    <style>
        .block-container {
            padding-top: 1.8rem;
            padding-bottom: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)
df=pd.read_csv('cleaned_data.csv')
st.set_page_config(layout="wide")
st.sidebar.title("Filters")
country = st.sidebar.multiselect("Select Country", df['Country'].unique())
region = st.sidebar.selectbox("Select Region", ["All"] + list(df['Region'].unique()))
city=st.sidebar.selectbox("Select City",["All"]+list(df['City'].unique()))
year_range = st.sidebar.slider("Year Range", int(df['Year'].min()), int(df['Year'].max()), (int(df['Year'].min()), int(df['Year'].max())))

# Apply filters
filtered_df = df.copy()

if country:
    filtered_df = filtered_df[filtered_df['Country'].isin(country)]

if region != "All":
    filtered_df = filtered_df[filtered_df['Region'] == region]
if city != "All":
    filtered_df = filtered_df[filtered_df['City'] == city]


filtered_df = filtered_df[
    (filtered_df['Year'] >= year_range[0]) &
    (filtered_df['Year'] <= year_range[1])
]

st.markdown("""
<h3 style="font-family: 'Verdana'; text-align: center;">
Global Air Quality Dashboard
</h3>
""", unsafe_allow_html=True)



#KPI metrics

st.markdown("<h3 style='text-align: center;'>Key Metrics  </h3>", unsafe_allow_html=True)



def kpi_card(title, value, color):
    st.markdown(f"""
        <div style="
            background:{color};
            padding:6px 8px;
            border-radius:8px;
            text-align:center;
            color:white;
            line-height:1.2;
            box-shadow:0 1px 4px rgba(0,0,0,0.2);
        ">
            <div style="
                font-size:11px;
                opacity:0.85;
            ">
                {title}
            </div>
            <div style="
                font-size:16px;
                font-weight:600;
                margin-top:2px;
            ">
                {value}
            </div>
        </div>
    """, unsafe_allow_html=True)



col1,col2,col3,col4,col5,col6= st.columns(6)

with col1:
  
    if st.checkbox("Show Raw data"):
        st.dataframe(df)

    if st.checkbox("Show Filtered  data"):
        st.dataframe(filtered_df)
with col2:
    kpi_card("Avg AQI", round(filtered_df['AQI'].mean(), 2), "#E74C3C")
with col3:
    kpi_card("Avg CO2", round(filtered_df['CO2_Emissions_MT'].mean(), 2), "#8E44AD")
with col4:
    kpi_card("Deforestation %", round(filtered_df['Deforestation_Rate_%'].mean(), 2), "#F39C12")
with col5:
    kpi_card("Forest Change %", round(filtered_df['Net_Forest_Change_%'].mean(), 2), "#009F13")
with col6:
    kpi_card("Life Expectancy", round(filtered_df['Avg_Life_Expectancy_Index'].mean(), 2), "#18A2F8")


col1,col2,col3= st.columns(3)

with col1:
    
    fig = px.scatter(
            filtered_df,
            x="PM_Ratio",
            y="Pollution_Health_Impact",
            color="AQI_category",
            
            facet_col="Income group",
            title="Faceted chart : Relationship Between PM Ratio and Health Impact Across Income Groups"
        )
    fig.update_layout(height=300,showlegend=False)
    st.plotly_chart(fig)
    
with col2:
        fig = px.scatter(
            filtered_df,
            x="Vehicles_Increase_%",
            y="Pollution_Health_Impact",
            color="AQI_category",          
            hover_name="Country",         
            hover_data=["Year", "Region"],  
            title="Multi Layer Chart : Vehicles Increase in % vs Pollution Health Impact"
            
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig)

with col3:
# Geo Spatial Visualization
    cols=filtered_df[['Country','AQI','PM_Ratio','Net_Forest_Change_%','CO2_per_Population']]
    coords = {
    'Australia': (-25.2744, 133.7751),
    'Brazil': (-14.2350, -51.9253),
    'Canada': (56.1304, -106.3468),
    'China': (35.8617, 104.1954),
    'France': (46.2276, 2.2137),
    'Germany': (51.1657, 10.4515),
    'India': (20.5937, 78.9629),
    'Japan': (36.2048, 138.2529),
    'UK': (55.3781, -3.4360),
    'USA': (37.0902, -95.7129)
}

    
    cols['lat'] = cols['Country'].apply(lambda x: coords[x][0])
    cols['lon'] = cols['Country'].apply(lambda x: coords[x][1])

    
    fig = px.scatter_geo(
        cols,
        lat='lat',
        lon='lon',
        color='AQI',
        size='PM_Ratio', 
        hover_name='Country',
        hover_data=['AQI','Net_Forest_Change_%','CO2_per_Population'],
        color_continuous_scale='Reds',
        projection='natural earth',
        title='Geo Spatial Visualization based on AQI'
    )

    fig.update_layout(height=300, margin={"r":0,"t":50,"l":0,"b":0})

    st.plotly_chart(fig, use_container_width=True)





col1,  col2,col3 = st.columns([1, 1, 1])

with col1:
    

    scenario = st.selectbox(
        "Scenario Based Comparision : Select Scenario",
        ["High vs Low AQI", "High vs Low CO2", "High vs Low Population Density"]
    )
    if scenario == "High vs Low AQI":
        high = filtered_df[filtered_df['AQI'] > filtered_df['AQI'].median()]
        low = filtered_df[filtered_df['AQI'] <= filtered_df['AQI'].median()]
        fig = px.box(
            pd.concat([high.assign(Type="High AQI"), low.assign(Type="Low AQI")]),
            x="Type",
            y="Avg_Life_Expectancy_Index",
            color="Type",
            
        )
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)

    elif scenario == "High vs Low CO2":
        high = filtered_df[filtered_df['CO2_Emissions_MT'] > filtered_df['CO2_Emissions_MT'].median()]
        low = filtered_df[filtered_df['CO2_Emissions_MT'] <= filtered_df['CO2_Emissions_MT'].median()]

        fig = px.box(
            pd.concat([high.assign(Type="High CO2"), low.assign(Type="Low C02")]),
            x="Type",
            y="AQI",
            color="Type",
            
        )
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
       
    elif scenario=="High vs Low Population Density":
        high=filtered_df[filtered_df['Population_Density_Per_SqKm']>filtered_df['Population_Density_Per_SqKm'].median()]
        low=filtered_df[filtered_df['Population_Density_Per_SqKm']<=filtered_df['Population_Density_Per_SqKm'].median()]
        fig = px.box(
            pd.concat([high.assign(Type="High Population Density"), low.assign(Type="Low Population Density")]),
            x="Type",
            y="AQI",
            color="Type",
            
        )
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
        


with col2:

    fig = px.bar(
        filtered_df.groupby("Income group", as_index=False)["Green_Space_Ratio_%"].mean(),
        x="Income group",
        y="Green_Space_Ratio_%",
        color="Income group",  
        title="Ethically Bias Visuals : Green Space Distribution Across Income Groups"
    )
    fig.update_layout(showlegend=False,height=300)

    st.plotly_chart(fig, use_container_width=True)
with col3:
    df_summary = filtered_df.groupby(['Region', 'Year'], as_index=False).agg(AQI_mean=('AQI', 'mean'))
    regions = df_summary['Region'].unique()

    fig = go.Figure()
    for region in regions:
        data = df_summary[df_summary['Region'] == region].sort_values('Year')
        
        
        fig.add_trace(go.Scatter(
            x=data['Year'],
            y=data['AQI_mean'],
            name=f'{region} mean'
        ))

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Average AQI',
        legend_title='Region',
        title="AQI Trend with Uncertainty by Country, Region and    City"
    )
    fig.update_layout(showlegend=False,height=300)
    st.plotly_chart(fig, use_container_width=True)