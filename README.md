# KOSTRA-DWD 2020 Data Extraction and Rainfall Conversion Tool
KOSTRA-DWD refers to Coordinated Heavy Rainfall Regionalization and Evaluation by the German Weather Service (DWD), which has been regularly compiled for over 30 years. The data, based on heavy rainfall, has been released in various updates such as KOSTRA-DWD-2000 (1951-2000) and KOSTRA-DWD-2010 (1951-2010). A revision known as KOSTRA-DWD-2010R was conducted at the request of individual state authorities. Between 2018 and 2022, the dataset underwent substantial revision and updates under the project "Methodische Untersuchungen zur Novellierung der Starkregenstatistik für Deutschlandy" (MUNSTAR), resulting in the introduction of KOSTRA-DWD-2020 (1951-2020). These data relate to precipitation amounts and rates calculated based on precipitation duration and return periods and have been transferred onto a nationwide grid. They are used for the design of water management structures, drainage systems, and also for assessing damage events. The data is available and can be downloaded free of charge as (excel, shapefile or ascii) (https://www.dwd.de/DE/leistungen/kostra_dwd_rasterwerte/kostra_dwd_rasterwerte.html).

![streamlit-Stream_lit_improving-2024-03-08-08-03-96-ezgif com-video-to-gif-converter](https://github.com/omarseleem92/KOSTRA_Data_tool/assets/57235564/71967cf7-1d7a-40b5-aaaa-b47de196a5af)






## Installation Options for the KOSTRA Tool

Users have the option to:
1. install the tool on their own computer and use it
2. use it online via the following link: KOSTRA Tool Online (https://huggingface.co/spaces/Omarseleem/KOSTRA).

The online option is slower but better if the user does not want to use python. If you prefer to use it on your own computer, follow the steps below:



### Run the tool from your computer

To run the Python script successfully, it is recommended to create a new environment in Anaconda and install the following Python packages. Afterwards, make this environment the active environment.

To create a new environment in Anaconda, use the following command:

```bash
conda create --name KOSTRA_Euler
```
To activate the created environment in Anaconda, use the following command:

```bash
conda activate KOSTRA_Euler
```
To install the necessary python packages, use the following commands:

1. **numpy**: Provides support for large, multi-dimensional arrays and matrices, along with a large collection of mathematical functions to operate on these arrays.
    ```bash
    pip install numpy
    ```

2. **pandas**: Provides data structures and data analysis tools.
    ```bash
    conda install anaconda::pandas
    ```
3. **matplotlib**: Provides plotting functionality.
    ```bash
    pip install matplotlib
    ```

4. **geopandas**: Extends the datatypes used by pandas to allow spatial operations on geometric types.
    ```bash
    pip install geopandas
    ```

5. **streamlit**: Allows for the creation of interactive web apps with simple Python scripts.
    ```bash
    pip install streamlit
    ```

6. **folium**: Provides tools for creating interactive maps.
    ```bash
    pip install folium
    ```

7. **streamlit_folium**: Integrates Folium maps into Streamlit apps.
    ```bash
    pip install streamlit_folium
    ```



8. **pyproj**: Provides Python interfaces to PROJ (cartographic projections and coordinate transformations library).
    ```bash
    pip install pyproj
    ```
Navigate to the directory where the script is located. This directory must contain a folder named Input_data_KOSTRA, which includes the files utilized by the tool. These files consist of KOSTRA files for various durations saved as pickles, making them easily accessible via pandas, as well as a shapefile depicting the federal states in Germany (Bundesländer).

Afterwards, in the command line, type the following command:

 ```bash
streamlit run Stream_lit.py
```

The webpage should then open in your browser, as illustrated below:

![image](https://github.com/omarseleem92/KOSTRA_Data_tool/assets/57235564/7105f06f-6a16-4c65-a872-78efdf9bd4d0)




## How does the tool work?

![image](https://github.com/omarseleem92/KOSTRA_Data_tool/assets/57235564/ee6de770-971b-444f-87ee-67a2435969a5)

The tool allows users to input the Bundesland (federal state), select a raster cell from the map, and specify the desired return period and event duration, along with one of three Euler distributions: Anfang (beginning), Mittel (middle), or Ende (end), where peak rainfall occurs at 0.33, 0.5, and 0.67 of the rainfall event duration, respectively. 

![image](https://github.com/omarseleem92/KOSTRA_Data_tool/assets/57235564/e7fde9f5-b8a6-4e99-b5be-a147c645fa05)


Subsequently, the tool displays a table showcasing all rainfall depths (for various durations and return periods) included in the KOSTRA dataset, alongside the rainfall distribution based on the selected Euler distribution. Additionally, users have the option to download the data as a CSV file for further analysis.

![image](https://github.com/omarseleem92/KOSTRA_Data_tool/assets/57235564/dcb34762-ddbb-444c-b13e-1a339c87d8c6)

The tool presents a graph illustrating Euler distributions types I and II, alongside cumulative rainfall depth, as depicted below. Users have the option to download the data from the graph as a CSV file by clicking the download button. Additionally, the tool provides the capability for users to download rainfall data as a LILA file, which is utilized by the LARSIM model—a widely used model by various authorities in Germany.

![image](https://github.com/omarseleem92/KOSTRA_Data_tool/assets/57235564/c3e62cee-3962-45ed-aeef-21a017380be9)


## Useful links: 
1. Detailed documentation by the DWD (Deutscher Wetterdienst) regarding KOSTRA data: https://www.dwd.de/DE/leistungen/kostra_dwd_rasterwerte/kostra_dwd_rasterwerte.html
2. KOSTRA interactive map allows to explore KOSTRA data, easily select specific raster cells and download KOSTRA data.: https://www.openko.de/maps/kostra_dwd_2020.html#7/50.573/10.397
