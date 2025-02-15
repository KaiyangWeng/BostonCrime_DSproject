# BostonCrime_DSproject
#### Geographic Crime Analysis (Boston)
 
Boston, like many metropolitan cities, experiences varying crime rates across different neighborhoods. Understanding these patterns can help law enforcement agencies allocate resources efficiently and perform city planning decision makings. However, raw crime data is often overwhelming and difficult to interpret. A **visual, interactive dashboard** is needed to make sense of this data.

## Introduction:  
This project presents an **interactive crime analysis dashboard** that enables users to:
- Analyze the frequency and patterns of various types of crimes.
- Explore time-based trends to determine peak hours for criminal activity.
- Provide actionable insights to law enforcement and policymakers for better decision-making.

## Benefits  
 - Real-time Data Exploration – Users can interact with crime statistics dynamically.  
 - Geospatial Visualization – Map-based representations of crime trends help identify high-risk areas.  
 - Crime Trend Analysis – Users can filter crimes by type, time of day, and location.  
 - Data-Driven Decision Making – Insights generated can inform law enforcement strategies and urban safety improvements.

## How to use the Interative Dashboard:
#### Step1: Load the Dashboard
Open 'Interactive_Dashboard_Sankey_Diagram' folder in the GitHub and then download all the files inside and crime2023.csv as well. Furthermore, open Bokeh_matplotlib_sankey_dashboard.py file and run it. Once loaded, Dashboard can generate prperly.

![Dashboard Preview](https://github.com/KaiyangWeng/BostonCrime_DSproject/blob/main/plots/Interactive_dashboard.png)

#### Step2: Select Crime Type & Min Occurence:
Use the Search Menu to select a specific offense and adjust the min_num slider to change the visualizations and tables, which can be used to analyze crime frequency by hour.
 - The searchable visualization and table will update dynamically with relevant crime statistics.

 ![Dashboard Preview](https://github.com/KaiyangWeng/BostonCrime_DSproject/blob/main/plots/offense_select.png)
 
### Step 3: Crime Association Analysis:
 - This section highlights correlations between different crime types, number of crime, and time periods.
 - Use interactive charts to filter data and explore relationships dynamically.

![Dashboard Preview](https://github.com/KaiyangWeng/BostonCrime_DSproject/blob/main/plots/Associations.png)

### Step 4: Sankey Diagram (Crime Flow Analysis):
 - The Sankey Diagram visually represents how different crimes change across different time periods.
 - It helps us to understand the distribution of different between crime type and hour.
 - Users can change the variables in the Search menu to see the changes between different Sankey Diagrams.

![Dashboard Preview](https://github.com/KaiyangWeng/BostonCrime_DSproject/blob/main/plots/Interactive_dashboard.png)

### Step 5: Visualization of Crime Data:
This dashboard provides two ways to explore crime data visually: 
 - View an interactive map that highlights the distribution different a specific crime type and hours across Boston.

![Dashboard Preview](https://github.com/KaiyangWeng/BostonCrime_DSproject/blob/main/plots/visualization.png)

### Step 6: Crime Data Table:
The Crime Table displays hourly crime counts, helping identify peak crime times. 
 - **HOUR** column: Crime occurences by hour
 - **crime_count** column: Total crimes per hour

![Dashboard Preview](https://github.com/KaiyangWeng/BostonCrime_DSproject/blob/main/plots/crime_table.png)

## Geographic Crime Analysis in Jupyter Notebooks
The Jupyter notebooks within the codes folder in this project provide a geographic and statistical analysis of Boston crime data using GeoPandas and Matplotlib. They include visualizations of crime hotspots, identifying the top five most frequent crimes and mapping high-crime streets and districts in the dataframe. Through data filtering and aggregation, the notebooks highlight patterns in crime occurrences, offering insights into location-based trends. 
![Dashboard Preview](https://github.com/KaiyangWeng/BostonCrime_DSproject/blob/main/plots/crime_districts.png)
![Dashboard Preview](https://github.com/KaiyangWeng/BostonCrime_DSproject/blob/main/plots/crime_streets.png)

## Geopandas and Geographic Analysis
The Geopandas library was used in this project to analyze and visualize crime data geographically, and eventually labeled the target street in the map of Boston. By importing shapefiles and crime2023 data, we plotted the distribution of crimes across different Boston streets and districts. Key analyses include identifying hotspots for violent crimes, mapping the top 5 crime locations, and visualizing shooting-related incidents. The integration of Geopandas enabled the project to highlight high-risk areas, which can be useful for law enforcement and policy-making. 
![Dashboard Preview](https://github.com/KaiyangWeng/BostonCrime_DSproject/blob/main/plots/Geopanda1.png)
![Dashboard Preview](https://github.com/KaiyangWeng/BostonCrime_DSproject/blob/main/plots/Geopanda2.png)

