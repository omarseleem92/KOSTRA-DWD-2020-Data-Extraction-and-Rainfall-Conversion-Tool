import pandas as pd
import geopandas as gpd
import streamlit as st
import folium
from streamlit_folium import folium_static
import os
import numpy as np
import matplotlib.pyplot as plt
from pyproj import Transformer
from io import StringIO
from datetime import datetime, timedelta

# Set the theme to 'Dark'
# Add some custom CSS to change the background color and text color
# Add custom CSS to create a dark theme
def set_theme():
    st.markdown(
        f"""
        <style>
        /* Set the background color of the entire page */
        body {{
            background-color: #0E1117;
            color: #FAFAFA;
            font-family: 'sans-serif';
        }}

        /* Set the background color of the sidebar */
        .sidebar .sidebar-content {{
            background-color: #262730;
            color: #FAFAFA;
        }}

        /* Set the text color of the sidebar header */
        .sidebar .sidebar-content .sidebar-top {{
            color: #FAFAFA;
        }}

        /* Set the background color of the main content area */
        .main {{
            background-color: #0E1117;
            color: #FAFAFA;
        }}

        /* Set the color of text input boxes */
        .stTextInput>div>div>input {{
            color: #FAFAFA;
        }}

        /* Set the color of button text */
        .stButton>button {{
            color: #FAFAFA;
        }}

        /* Set the background color of buttons */
        .stButton>button {{
            background-color: #FF4B4B;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def Show_table_Niderschlagshoehe(selected_cell,gdf_KOSTRA_D5, gdf_KOSTRA_D10, gdf_KOSTRA_D15, gdf_KOSTRA_D20,
                                 gdf_KOSTRA_D30, gdf_KOSTRA_D45, gdf_KOSTRA_D60, gdf_KOSTRA_D90, gdf_KOSTRA_D120,
                                 gdf_KOSTRA_D180, gdf_KOSTRA_D240, gdf_KOSTRA_D360, gdf_KOSTRA_D540, gdf_KOSTRA_D720,
                                 gdf_KOSTRA_D1080, gdf_KOSTRA_D1440, gdf_KOSTRA_D2880, gdf_KOSTRA_D4320,
                                 gdf_KOSTRA_D5760, gdf_KOSTRA_D7200, gdf_KOSTRA_D8640, gdf_KOSTRA_D10080):

    '''
    Display rainfall depth data for selected raster ell.

    Parameters:
    -----------
    selected_cell : str The selected raster cell index from KOSTRA-DWD data.
    gdf_KOSTRA_D5, gdf_KOSTRA_D10, ..., gdf_KOSTRA_D10080 : GeoDataFrames
        GeoDataFrames containing rainfall data for various durations.

    Returns:
    --------
    None

    Description:
    ------
    - The function extracts rows from each GeoDataFrame based on the selected raster cell index and duration.
    - It concatenates the extracted rows into a single DataFrame and displays the rainfall depth data in a tabular format.
    - Users can download the data as a CSV file using the provided download button.
    '''

    # Extract rows where INDEX_RC is as given by the user and add a column for the source DataFrame name
    dfs = []

    # Define the duration and dataframe pairs up to the entered duration
    duration_df_pairs = [(5, gdf_KOSTRA_D5), (10, gdf_KOSTRA_D10),
                         (15, gdf_KOSTRA_D15), (20, gdf_KOSTRA_D20),
                         (30, gdf_KOSTRA_D30), (45, gdf_KOSTRA_D45),
                         (60, gdf_KOSTRA_D60), (90, gdf_KOSTRA_D90),
                         (120, gdf_KOSTRA_D120), (180, gdf_KOSTRA_D180),
                         (240, gdf_KOSTRA_D240), (360, gdf_KOSTRA_D360),
                         (540, gdf_KOSTRA_D540), (720, gdf_KOSTRA_D720),
                         (1080, gdf_KOSTRA_D1080), (1440, gdf_KOSTRA_D1440),
                         (2880, gdf_KOSTRA_D2880), (4320, gdf_KOSTRA_D4320),
                         (5760, gdf_KOSTRA_D5760), (7200, gdf_KOSTRA_D7200),
                         (8640, gdf_KOSTRA_D8640), (10080, gdf_KOSTRA_D10080)]

    # Iterate over the duration and dataframe pairs
    for duration, df in duration_df_pairs:
        filtered_rows = df[df['INDEX_RC'] == selected_cell].copy()
        filtered_rows['Dauer (min)'] = duration
        dfs.append(filtered_rows)


    # Concatenate the DataFrames into a single DataFrame
    result_df = pd.concat(dfs, ignore_index=True)

    Niederschlagshöhe=pd.DataFrame()
    Niederschlagshöhe['Dauerstufe (min)']=result_df['Dauer (min)']
    Niederschlagshöhe['1']=result_df['HN_001A_']
    Niederschlagshöhe['2']=result_df['HN_002A_']
    Niederschlagshöhe['3']=result_df['HN_003A_']
    Niederschlagshöhe['5']=result_df['HN_005A_']
    Niederschlagshöhe['10']=result_df['HN_010A_']
    Niederschlagshöhe['20']=result_df['HN_020A_']
    Niederschlagshöhe['30']=result_df['HN_030A_']
    Niederschlagshöhe['50']=result_df['HN_050A_']
    Niederschlagshöhe['100']=result_df['HN_100A_']
    # make the duration as an index
    Niederschlagshöhe.set_index('Dauerstufe (min)', inplace=True)

    # Write the dataframe as a table
    st.dataframe(Niederschlagshöhe)

    # Check if the user clicked the download button
    st.download_button(
        label="Download rainfall depth as CSV",
        data=Niederschlagshöhe.to_csv(sep='\t', index=True, encoding='utf-8'),
        file_name='Rainfalldepth.csv',
        mime='text/tab-separated-values',
    )

    return

def show_extracted_data_based_on_user_input(selected_cell,selected_duration,selected_return_period,peak_time,gdf_KOSTRA_D5, gdf_KOSTRA_D10, gdf_KOSTRA_D15, gdf_KOSTRA_D20,
                                 gdf_KOSTRA_D30, gdf_KOSTRA_D45, gdf_KOSTRA_D60, gdf_KOSTRA_D90, gdf_KOSTRA_D120,
                                 gdf_KOSTRA_D180, gdf_KOSTRA_D240, gdf_KOSTRA_D360, gdf_KOSTRA_D540, gdf_KOSTRA_D720,
                                 gdf_KOSTRA_D1080, gdf_KOSTRA_D1440, gdf_KOSTRA_D2880, gdf_KOSTRA_D4320,
                                 gdf_KOSTRA_D5760, gdf_KOSTRA_D7200, gdf_KOSTRA_D8640, gdf_KOSTRA_D10080):
    '''
        Extracts and displays rainfall data based on user input.

        Parameters:
        -----------
        selected_cell : str
            The selected cell index.
        selected_duration : int
            The selected duration.
        selected_return_period : str
            The selected return period.
        peak_time : float
            The peak time based on the selected euler disribution.
        gdf_KOSTRA_D5, gdf_KOSTRA_D10, ..., gdf_KOSTRA_D10080 : GeoDataFrames
            GeoDataFrames containing rainfall data for various durations.

        Returns:
        --------
        tuple (Dauer, Typ_II)
            Dauer : duration Series
                Series containing durations.
            Typ_II : rainfall depth based on the selected distributions as a Series
                Series containing Typ II values.

        Description:
        ------
        - The function extracts rows from each GeoDataFrame based on the selected cell index,return period and duration.
        - It concatenates the extracted rows into a single DataFrame and displays the rainfall depth data in a tabular format.
        - The function use the extracted data to distribute the rainfall based on the selected rainfall distribution by the user
        - Users can download the data as a CSV file using the provided download button.
        - The function also plots Typ I and Typ II against duration and displays cumulative rainfall data.
        - A PNG image of the plot can be downloaded.
    '''

    # Extract rows where INDEX_RC is as given by the user and add a column for the source DataFrame name
    dfs = []

    # Define the duration and dataframe pairs up to the entered duration
    duration_df_pairs = [(5, gdf_KOSTRA_D5), (10, gdf_KOSTRA_D10),
                         (15, gdf_KOSTRA_D15), (20, gdf_KOSTRA_D20),
                         (30, gdf_KOSTRA_D30), (45, gdf_KOSTRA_D45),
                         (60, gdf_KOSTRA_D60), (90, gdf_KOSTRA_D90),
                         (120, gdf_KOSTRA_D120), (180, gdf_KOSTRA_D180),
                         (240, gdf_KOSTRA_D240), (360, gdf_KOSTRA_D360),
                         (540, gdf_KOSTRA_D540), (720, gdf_KOSTRA_D720),
                         (1080, gdf_KOSTRA_D1080), (1440, gdf_KOSTRA_D1440),
                         (2880, gdf_KOSTRA_D2880), (4320, gdf_KOSTRA_D4320),
                         (5760, gdf_KOSTRA_D5760), (7200, gdf_KOSTRA_D7200),
                         (8640, gdf_KOSTRA_D8640), (10080, gdf_KOSTRA_D10080)]

    # Iterate over the duration and dataframe pairs
    for duration, df in duration_df_pairs:
        if duration > selected_duration:  # Stop the loop if the duration exceeds the entered duration
            break
        filtered_rows = df[df['INDEX_RC'] == selected_cell].copy()
        filtered_rows['Dauer (min)'] = duration
        dfs.append(filtered_rows)

    # Concatenate the DataFrames into a single DataFrame
    result_df = pd.concat(dfs, ignore_index=True)

    # Filter with retrun Period
    KOSTRA_df=pd.DataFrame()
    KOSTRA_df['Dauer (min)']=result_df['Dauer (min)']
    KOSTRA_df[selected_return_period]=result_df[selected_return_period]

    #st.dataframe(KOSTRA_df)
    # Display the DataFrame in the sidebar
    st.sidebar.subheader('Extracted data from KOSTRA dataset')
    st.sidebar.write(KOSTRA_df)
    # Check if the user clicked the download button


    # Display the download button in the sidebar
    st.sidebar.download_button(
            label="Download extracted KOSTRA data as CSV",
            data=KOSTRA_df.to_csv(sep=';', index=True, encoding='utf-8'),
            file_name='Extracted_KOSTRA.csv',
            mime='text/tab-separated-values'
    )

    # Check if the user clicked the download button
#    st.download_button(
#            label="Download extracted KOSTRA data as CSV",
#            data=KOSTRA_df.to_csv(sep='\t', index=True, encoding='utf-8'),
#            file_name='Extracted_KOSTRA.csv',
#            mime='text/tab-separated-values',
#        )


    # Convert the extracted data to the Euler typ II distribution

    Euler_2_df=pd.DataFrame() # make a new dataframe
    new_index = range(KOSTRA_df['Dauer (min)'].min(), KOSTRA_df['Dauer (min)'].max() + 1, 5) # make index every 5 minutes because the extracted data are not every 5 mins
    Euler_2_df = KOSTRA_df.set_index('Dauer (min)').reindex(new_index).reset_index()

    # Fill NaN values with the average between consecutive non-NaN values
    Euler_2_df[selected_return_period+'_new'] = Euler_2_df[selected_return_period].interpolate()

    # Calculate Typ I column as the difference between the cell in the rainfall column
    Euler_2_df['Typ I'] = Euler_2_df[selected_return_period+'_new'].diff()
    Euler_2_df.at[0, 'Typ I'] = Euler_2_df.at[0, selected_return_period+'_new']  # First value in Typ I column is the same as original niederschlag höhe column

    max_typ_i = Euler_2_df['Typ I'].max() # Max value in Typ I
    max_dauer = Euler_2_df['Dauer (min)'].max() # Max dauer

    # Calculate the threshold for 'Dauer (min)'
    threshold = peak_time * max_dauer

    # Find the index closest to the threshold
    idx_closest = (Euler_2_df['Dauer (min)'] - threshold).abs().idxmin()

    # Add the max Typ I value to Typ II column at the index closest to 0.33 * max_dauer
    Euler_2_df.loc[idx_closest, 'Typ II'] = max_typ_i


    # Find the index of the first non-NaN value in the 'Typ II' column
    first_non_nan_index = Euler_2_df['Typ II'].first_valid_index()

    # Assign values from 'Typ I' to 'Typ II' for cells after the first non-NaN value in 'Typ II'
    Euler_2_df.loc[first_non_nan_index+1:, 'Typ II'] = Euler_2_df.loc[first_non_nan_index+1:, 'Typ I']

    # Find the index of the first valid value in the 'Typ II' column
    first_valid_index = Euler_2_df['Typ II'].first_valid_index()

    # Get the values from the 'Typ I' column to fill NaN values in 'Typ II'
    values_to_fill = Euler_2_df['Typ I'].iloc[1:first_valid_index+1]

    # Reverse the values_to_fill array
    values_to_fill_reversed = values_to_fill[::-1]

    # Update the 'Typ II' column with values from 'Typ I' column
    Euler_2_df['Typ II'].iloc[:first_valid_index] = values_to_fill_reversed

    # Create the cumulative column
    Euler_2_df['cumulative_regen_höhe'] = Euler_2_df['Typ II'].cumsum()

    Euler_2_df['Regen_Percent']=(Euler_2_df['Typ II'] / Euler_2_df['Typ II'].sum())*100

    # Create the cumulative percentage column
    Euler_2_df['cumulative_regen_perentage'] = Euler_2_df['Regen_Percent'].cumsum()

    # Cread a regenspende column
    Euler_2_df['Regenspende (l/(s*ha))']=Euler_2_df['Typ II']/5/0.006




    # Plot the results
    # Data from Euler_2_df DataFrame
    Dauer = Euler_2_df['Dauer (min)']
    Typ_I = Euler_2_df['Typ I']
    Typ_II = Euler_2_df['Typ II']
    Cumulative_Rainfall = Euler_2_df['cumulative_regen_höhe']

    # Define the width of each bar
    bar_width = 0.35

    # Calculate the step size for x-axis ticks
    step_size = max(1, len(Dauer) // 20)

    # Set the x-axis positions for the bars
    x = np.arange(len(Dauer))

    # Create a figure and axis objects
    fig, ax1 = plt.subplots(figsize=(12, 7))

    # Plot Typ I and Typ II as bar plots
    bars1 = ax1.bar(x - bar_width/2, Typ_I, width=bar_width, color='skyblue', label='Typ I')
    bars2 = ax1.bar(x + bar_width/2, Typ_II, width=bar_width, color='salmon', label='Typ II')

    # Set x-axis and y-axis labels for the main plot
    ax1.set_xlabel('5-min Zeitintervalle', fontsize=14)
    ax1.set_ylabel('N-Höhe [mm]', fontsize=14)
    ax1.set_title('Typ I and Typ II vs Dauer (min)', fontsize=16)
    ax1.legend(fontsize=12)
    plt.legend(loc='lower center', fontsize=12, bbox_to_anchor=(0.6, -0.3), bbox_transform=ax1.transAxes)

    # Set x-axis ticks for the main plot
    ax1.set_xticks(x[::step_size])
    ax1.set_xticklabels(Dauer[::step_size], fontsize=12, rotation=45, ha='right')
    ax1.yaxis.grid(True, linestyle='--', alpha=0.7)

    # Create a secondary y-axis for the cumulative rainfall
    ax2 = ax1.twinx()
    ax2.plot(x, Cumulative_Rainfall, color='black', label='kumulativer Niederschlagsprozentsatz',linestyle='--')

    # Set y-axis label and ticks for the secondary axis
    ax2.set_ylabel('kumulativer Niederschlagshöhe (mm)', fontsize=14)
    ax2.tick_params(axis='y', labelsize=12)
    #ax2.yaxis.grid(False, linestyle='--', alpha=0.7)

    # Create a secondary x-axis for the cumulative rainfall
    #ax3 = ax1.twiny()
    #ax3.set_xticks(x[::step_size])
    #ax3.set_xticklabels(Dauer[::step_size], fontsize=12, rotation=45, ha='right')
    #ax3.set_xlabel('Cumulative Rainfall', fontsize=14)
    # Move the legend to the bottom center outside the plot area
    plt.legend(loc='lower center', fontsize=12, bbox_to_anchor=(0.35, -0.28), bbox_transform=ax1.transAxes)

    # Move the legend to the bottom center
    #plt.legend(loc='lower center', fontsize=12)

    plt.tight_layout()
    plt.savefig('Euler_Typ_II_cumulative.png')
    #plt.show()

    # Show the plot in Streamlit
    st.pyplot(fig)
    # Create a button to download the plot as PNG
    #st.dataframe(Euler_2_df)

    # Check if the user clicked the download button
    st.download_button(
                label="Download Euler TypII data as CSV",
                data=Euler_2_df.to_csv(sep=';', index=True, encoding='utf-8'),
                file_name='Euler_typ_II.csv',
                mime='text/tab-separated-values',
            )

    #st.dataframe(Euler_2_df)
    return (Dauer,Typ_II)

def LARSIM_lila_file(selected_cell, Kostra_selected_cell_centroid_lon, Kostra_selected_cell_centroid_lat, Dauer, Typ_II):
        # Define the information to be written to the text file
        data = [
            "Station;KL-KOSTRA;",
            f"Stationsnummer;{selected_cell};alternativ Raster-ID",
            "Betreiber;RLP;",
            "Datenart;N;",
            "Datenursprung;mes;",
            "Dimension;mm;",
            "Zeitintervall;00:05;",
            "Zeitzone;UTC+1;",
            f"X-Koordinate;{Kostra_selected_cell_centroid_lon}; Koordiante des Rastermittelpunktes",
            f"Y-Koordinate;{Kostra_selected_cell_centroid_lat}; Koordiante des Rastermittelpunktes",
            "Hoehe;240.000; Höhe des Rastermittelpunktes",
            "Kommentar;Hinweis zu den Daten und der Verteilung z.B. KOSTRA_DWD_2020, Euler Typ II"
        ]

        # Define the file path
        file_path = "LARSIM.lila"

        # Write the data to the text file
        with open(file_path, "w") as file:
            # Write initial information
            for line in data:
                file.write(line + "\n")

            # Write the lists as two columns
            for item1, item2 in zip(Dauer, Typ_II):
                file.write(f"{item1};{item2}\n")



def generate_larsim_lila_content(selected_cell, Kostra_selected_cell_centroid_lon, Kostra_selected_cell_centroid_lat, Typ_II,selected_distribution):
    '''
    Generates content for LARSIM.lila file.

    Parameters:
    -----------
    selected_cell : str
        The selected raster cell index.
    Kostra_selected_cell_centroid_lon : float
        Longitude of the centroid of the selected raster cell.
    Kostra_selected_cell_centroid_lat : float
        Latitude of the centroid of the selected raster cell.
    Typ_II : Series
        Series containing Typ II values.
    selected_distribution : str
        The selected rainfall distribution.

    Returns:
    --------
    str
        Content for the LARSIM.lila file.

    Notes:
    ------
    - The function generates time values starting from the current time with a 5-minute interval for 4 days.
    - It ensures that the Typ_II values are aligned with the time values and fills zeros where necessary.
    - The generated content includes station details, coordinates, and comments about the data distribution.
    '''

    # Define the starting date and time
    day = st.date_input('Select Day:')
    hour = st.selectbox('Select Hour:', range(24))
    minute = st.selectbox('Select Minute:',range(0, 60, 5))
    # Calculate the difference in days between selected day and current day
    day_difference = (day - datetime.now().date()).days

    # Calculate the starting date and time
    start_date = datetime.now().replace(hour=int(hour), minute=int(minute), second=0, microsecond=0) + timedelta(days=day_difference)


    #start_date = datetime.now().replace(hour=0, minute=5, second=0, microsecond=0)

    # Define the number of days and the interval in minutes
    num_days = 4
    interval_minutes = 5

    # Create a list to store the time values
    time_list = []

    # Generate the time values
    current_time = start_date
    for _ in range(num_days * 24 * 60 // interval_minutes):
        time_list.append(current_time.strftime('%d.%m.%Y %H:%M'))
        current_time += timedelta(minutes=interval_minutes)

    # Convert Typ_II from a Pandas Series to a list
    Typ_II = Typ_II.tolist()
    # Read the Typ_II list and determine its length
    typ_II_length = len(Typ_II)

    # Determine the target length for Typ_II list (same as the time_list)
    target_length = len(time_list)

    # Append zeros to Typ_II list until it reaches the target length
    while len(Typ_II) < target_length:
        Typ_II.append(0)



    # Define the content
    content = StringIO()
    content.write("Station;KL-KOSTRA;\n")
    content.write(f"Stationsnummer;{selected_cell};alternativ Raster-ID\n")
    content.write("Betreiber;RLP;\n")
    content.write("Datenart;N;\n")
    content.write("Datenursprung;mes;\n")
    content.write("Dimension;mm;\n")
    content.write("Zeitintervall;00:05;\n")
    content.write("Zeitzone;UTC+1;\n")
    content.write(f"X-Koordinate;{Kostra_selected_cell_centroid_lon}; Koordiante des Rastermittelpunktes: EPSG 3035 \n")
    content.write(f"Y-Koordinate;{Kostra_selected_cell_centroid_lat}; Koordiante des Rastermittelpunktes:  EPSG 3035 \n")
    content.write("Hoehe;240.000; Höhe des Rastermittelpunktes\n")
    content.write(f"Kommentar;Hinweis zu den Daten und der Verteilung z.B. KOSTRA_DWD_2020, {selected_distribution}\n")

    # Write the values of Typ_II in the corresponding column, fill zeros when they finish
    current_time = start_date
    for time, item in zip(time_list, Typ_II):
        time = datetime.strptime(time, '%d.%m.%Y %H:%M')
        content.write(f"{time.strftime('%d.%m.%Y %H:%M')};{item}\n")


    return content.getvalue()




def main():



    # Display the title
    st.title("KOSTRA-DWD 2020 Data Extraction and Rainfall Conversion Tool")
    # Display a heading in the sidebar
    st.sidebar.header("Input Data")

    # Set the dark theme
    set_theme()

    #set_parameter=st.sidebar.button("Set parameters", type="secondary")


    # Load the KOSTRA shapefile to show on the map
    directory = 'Input_data_KOSTRA'
    KOSTRA = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D5.pkl'))

    # Read KOSTRA data for all the availabe durations as pickle files (geodataframe)
    gdf_KOSTRA_D5 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D5.pkl'))
    gdf_KOSTRA_D10 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D10.pkl'))
    gdf_KOSTRA_D15 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D15.pkl'))
    gdf_KOSTRA_D20 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D20.pkl'))
    gdf_KOSTRA_D30 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D30.pkl'))
    gdf_KOSTRA_D45 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D45.pkl'))
    gdf_KOSTRA_D60 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D60.pkl'))
    gdf_KOSTRA_D90 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D90.pkl'))
    gdf_KOSTRA_D120 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D120.pkl'))
    gdf_KOSTRA_D180 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D180.pkl'))
    gdf_KOSTRA_D240 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D240.pkl'))
    gdf_KOSTRA_D360 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D360.pkl'))
    gdf_KOSTRA_D540 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D540.pkl'))
    gdf_KOSTRA_D720 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D720.pkl'))
    gdf_KOSTRA_D1080 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D1080.pkl'))
    gdf_KOSTRA_D1440 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D1440.pkl'))
    gdf_KOSTRA_D2880 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D2880.pkl'))
    gdf_KOSTRA_D4320 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D4320.pkl'))
    gdf_KOSTRA_D5760 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D5760.pkl'))
    gdf_KOSTRA_D7200 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D7200.pkl'))
    gdf_KOSTRA_D8640 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D8640.pkl'))
    gdf_KOSTRA_D10080 = pd.read_pickle(os.path.join(directory, 'gdf_KOSTRA_D10080.pkl'))

    # Load the Bundesländer shapefile
    bundeslander = gpd.read_file(os.path.join(directory, 'vg2500_bld_3035.shp'))
    # Get the list of Bundesländer
    bundeslander_names = bundeslander['GEN'].unique()

    # Set the center coordinates for Germany
    germany_coords = [51.1657, 10.4515]

    # Create a sidebar dropdown for Bundesländer selection
    selected_bundesland = st.sidebar.selectbox('Select federal state', bundeslander_names)

    # Filter the shapefile based on the selected Bundesland
    # Show only KOSTRA data within the selected Bundesland to make the tool faster
    selected_shape = bundeslander[bundeslander['GEN'] == selected_bundesland].to_crs("EPSG:4326")

    # Retrieve the geometry of the selected polygon
    selected_geometry = selected_shape['geometry'].iloc[0]

    # Calculate the centroid of the selected polygon
    centroid = selected_geometry.centroid

    # Define the transformer to convert from EPSG:3035 to EPSG:4326
    #transformer = Transformer.from_crs("EPSG:3035", "EPSG:4326", always_xy=True)
    # Transform the coordinates of the centroid to EPSG:4326 (WGS84)
    # Extract the latitude and longitude of the centroid
    centroid_lat = centroid.y
    centroid_lon = centroid.x

    # Filter the shapefile based on the selected Bundesland
    selected_shape = selected_shape.to_crs("EPSG:3035")


    # Clip the Kostra dataset based on the selected shapefile
    clipped_KOSTRA = gpd.clip(KOSTRA, selected_shape.geometry)

    # Get the list of raster cell names within the selected bundesland
    cell_names = sorted(clipped_KOSTRA['INDEX_RC'].unique())

    # Create a sidebar dropdown for Cell index of Kostra selection
    #selected_cell = st.sidebar.selectbox('Select a raster cell', cell_names)

    # Create a sidebar dropdown for Cell index of Kostra selection
    selected_cell = st.sidebar.selectbox('Select a raster cell', options=cell_names)

    #KOSTRA_cell coordinates
    Kostra_selected_cell=clipped_KOSTRA[clipped_KOSTRA['INDEX_RC']==selected_cell]
    Kostra_selected_cell_centroid=Kostra_selected_cell['geometry'].iloc[0].centroid
    Kostra_selected_cell_centroid_lat = Kostra_selected_cell_centroid.y
    Kostra_selected_cell_centroid_lon = Kostra_selected_cell_centroid.x




    # Get the list of return periods in KOSTRA
    return_periods = clipped_KOSTRA.columns[2:11]

    # Create a sidebar dropdown for return period from KOSTRA
    selected_return_period = st.sidebar.selectbox('Select return period', return_periods)


    # Get the list of duration in KOSTRA
    durations = [5,10,15,20,30,45,60,90,120,180,240,360,540,720,1080,1440,2880,4320,5760,7200,8640,10080]

    # Create a sidebar dropdown for Cell index of Kostra selection
    selected_duration = st.sidebar.selectbox('Select duration (min)', durations)

    distributions=['Euler Typ II-Beginning(Anfang)','Euler Typ II-Middle (Mitte)','Euler Typ II-End(Ende)']
    # Create a sidebar dropdown for Cell index of Kostra selection
    selected_distribution = st.sidebar.selectbox('Select Euler distribution', distributions)    # Create a Streamlit checkbox to select a distribution
    if selected_distribution =='Euler Typ II-Beginning(Anfang)':
        peak_time=0.33
    if selected_distribution =='Euler Typ II-Middle (Mitte)':
        peak_time=0.5
    if selected_distribution =='Euler Typ II-End(Ende)':
        peak_time=0.67





    show_bundeslander = st.checkbox("Show federal states (Bundesländer) ", value=True)


    # Create a Streamlit checkbox to toggle the visibility of Bundesländer boundaries
    show_Kostra = st.checkbox("Show KOSTRA raster cells", value=False)


        # Create a Folium map centered around Germany
    m = folium.Map(location=[centroid_lat, centroid_lon], zoom_start=7)

    # Add the Bundesländer boundaries to the Folium map if the checkbox is checked
    if show_bundeslander:
        folium.GeoJson(
            bundeslander,
            style_function=lambda feature: {
                'color': 'black',         # Set boundary color to black
                'weight': 2,              # Set boundary weight (line thickness)
                'fillOpacity': 0          # Make the boundary transparent
            },
            tooltip=folium.features.GeoJsonTooltip(fields=["GEN"], labels=False, sticky=True)
        ).add_to(m)

    # Display the selected shape on the map
    if show_bundeslander:
        folium.GeoJson(
            selected_shape,
            style_function=lambda feature: {
                'color': 'red',         # Set boundary color to red
                'weight': 2,            # Set boundary weight (line thickness)
                'fillOpacity': 0        # Make the boundary transparent
            },
            tooltip=folium.features.GeoJsonTooltip(fields=["GEN"], labels=False, sticky=True)
        ).add_to(m)

    # Display the clipped Kostra dataset on the map
    if show_Kostra:
        folium.GeoJson(
            clipped_KOSTRA,
            style_function=lambda feature: {
                'color': 'blue',         # Set boundary color to blue
                'weight': 2,             # Set boundary weight (line thickness)
                'fillOpacity': 0         # Make the boundary transparent
            },
            tooltip=folium.features.GeoJsonTooltip(fields=["INDEX_RC"], labels=False, sticky=True)
        ).add_to(m)

    # Display the Folium map in Streamlit
    folium_static(m)

    #run_sim=st.sidebar.button("Run Tool", type="secondary")

    #if run_sim:






        # Create a checkbox to trigger the function
    if st.checkbox('Show rainfall depth table for all duration and return periods',value=False):
                Show_table_Niderschlagshoehe(selected_cell,gdf_KOSTRA_D5, gdf_KOSTRA_D10, gdf_KOSTRA_D15, gdf_KOSTRA_D20,
                                             gdf_KOSTRA_D30, gdf_KOSTRA_D45, gdf_KOSTRA_D60, gdf_KOSTRA_D90, gdf_KOSTRA_D120,
                                             gdf_KOSTRA_D180, gdf_KOSTRA_D240, gdf_KOSTRA_D360, gdf_KOSTRA_D540, gdf_KOSTRA_D720,
                                             gdf_KOSTRA_D1080, gdf_KOSTRA_D1440, gdf_KOSTRA_D2880, gdf_KOSTRA_D4320,
                                             gdf_KOSTRA_D5760, gdf_KOSTRA_D7200, gdf_KOSTRA_D8640, gdf_KOSTRA_D10080)


    if st.checkbox('Show extracted data from KOSTRA and Euler Typ II distribution',value=True):

                Dauer, Typ_II= show_extracted_data_based_on_user_input(selected_cell,selected_duration,selected_return_period,peak_time,gdf_KOSTRA_D5, gdf_KOSTRA_D10, gdf_KOSTRA_D15, gdf_KOSTRA_D20,
                                                 gdf_KOSTRA_D30, gdf_KOSTRA_D45, gdf_KOSTRA_D60, gdf_KOSTRA_D90, gdf_KOSTRA_D120,
                                                 gdf_KOSTRA_D180, gdf_KOSTRA_D240, gdf_KOSTRA_D360, gdf_KOSTRA_D540, gdf_KOSTRA_D720,
                                                 gdf_KOSTRA_D1080, gdf_KOSTRA_D1440, gdf_KOSTRA_D2880, gdf_KOSTRA_D4320,
                                                 gdf_KOSTRA_D5760, gdf_KOSTRA_D7200, gdf_KOSTRA_D8640, gdf_KOSTRA_D10080)



                if st.checkbox('Download Lila file for LARSIM',value=False):
                            content = generate_larsim_lila_content(selected_cell, Kostra_selected_cell_centroid_lon, Kostra_selected_cell_centroid_lat, Typ_II,selected_distribution)
                            if content is not None:  # Assuming content is the variable containing the data to download
                                    st.download_button(
                                        label="Download LARSIM.lila",
                                        data=content,
                                        file_name="LARSIM.lila",
                                        mime="text/plain"
                                    )








    #if st.checkbox('Show Euler Typ II distribution',value=False):
    #    Euler_typ_II(KOSTRA_df)
    #
    # Convert the 'geometry' column to a string format
    #KOSTRA['geometry_str'] = KOSTRA['geometry'].astype(str)

    # Drop the original 'geometry' column
    #KOSTRA = KOSTRA.drop(columns=['geometry'])

    # Display the DataFrame using st.dataframe()
    #st.dataframe(KOSTRA)




if __name__ == "__main__":
    main()
