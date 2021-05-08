# Location Affordability Tool 
q-maze, suozzi-matt, ewp4x

## Introduction and Overview
The team was interested in studying housing data for our project and we were able to find census data on affordability ratings of various cities.

## The Data
The dataset we chose is the [US Department of Housing and Urban Development's location affordability index](https://hudgis-hud.opendata.arcgis.com/datasets/location-affordability-index-v-3?geometry=-17.263%2C-52.642%2C17.894%2C85.381). This dataset combines housing affordability data with transportation costs for all localities within the United States.

There is a dropdown menu to download the Full Dataset in multiple formats.  We focused on the [spreadsheet format](https://opendata.arcgis.com/datasets/b7ffe3607e8c4212bf7cf2428208dbb6_0.csv).

## Report

Find the final report in the report folder - [Final Report](https://github.com/q-maze/location-affordability-tool/blob/main/Report/Final-Report.md)
[Presentation](https://github.com/q-maze/location-affordability-tool/blob/main/Report/CS%20Project%20Presentation.pdf)

## Code and Usage

All code is in the [code folder](https://github.com/q-maze/location-affordability-tool/tree/main/code) 

### General Data Exploration

The main data exploration can be done with the [CS_Semester_Project.ipynb file](https://github.com/q-maze/location-affordability-tool/blob/main/code/CS_Semester_Project.ipynb).  Here you can see some of the data cleaning and general analysis of the state data, correlation of specific datafields, and visualizations.  This downloads the spreadsheet from the site so loading the data can take time (>200MB).

### Affordability Data for User

The user needs to download all the shape files from the [data folder](https://github.com/q-maze/location-affordability-tool/tree/main/data) and update their path inside the main interactive file called [Geopandas_for_User_Output](https://github.com/q-maze/location-affordability-tool/blob/main/code/Geopandas_for_User_Output.ipynb).

Once you have the shape files loaded into a path update this line of code:
![Path line for update!](https://github.com/q-maze/location-affordability-tool/blob/main/Report/Figures/Update%20Path%20for%20Shape%20Files.png)
