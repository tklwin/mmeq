import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Load the Myanmar earthquake dataset
df_myanmar = pd.read_csv("earthquake_data_myanmar.csv")

# Convert 'time' column to datetime format (remove timezone issues)
df_myanmar["time"] = pd.to_datetime(df_myanmar["time"]).dt.tz_localize(None)

# Get min and max date from the dataset
min_date = df_myanmar["time"].min().date()
max_date = df_myanmar["time"].max().date()

st.title("Myanmar Earthquake Map")
st.write("Explore earthquake data in Myanmar using an interactive map.")

# Date Range Selection using Streamlit's slider
start_date, end_date = st.slider(
    "Select Date Range:",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)

# Filter data based on selected date range
filtered_df = df_myanmar[(df_myanmar["time"] >= pd.Timestamp(start_date)) &
                          (df_myanmar["time"] <= pd.Timestamp(end_date))]

st.write(f"Showing earthquakes from {start_date} to {end_date}")

# Create a base map centered on Myanmar
myanmar_map = folium.Map(location=[21.0, 96.0], zoom_start=6)

# Add earthquake markers
for _, row in filtered_df.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=row["mag"] * 1.5,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.6,
        popup=f"Date: {row['time'].date()}<br>Magnitude: {row['mag']}<br>Depth: {row['depth']} km<br>Location: {row['place']}",
    ).add_to(myanmar_map)

# Display the map using Streamlit
st_folium(myanmar_map, width=700, height=500)  

# Show number of earthquakes in the selected range
st.write(f"Total Earthquakes in Selected Range: {len(filtered_df)}")
