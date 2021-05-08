# CS 5010 Project
---
- Quinton Mays (rub9ez)
- Matt Suozzi (mds5dd)
- Eric Pratsch (ewp4x)
- [GitHub Repo](https://github.com/q-maze/location-affordability-tool)
- [Presentation](https://github.com/q-maze/location-affordability-tool/blob/main/Report/CS%20Project%20Presentation.pdf)
---
## Introduction
Our team was interested in learning more about patterns in housing affordability in the continental US.  We wanted to learn about overall trends in housing affordability across different geographic regions and to use this knowledge to create an application for users to identify affordable places based on a target state at the county level.

This has many benefits for users as affordable living is often difficult to find and depends on many factors like proximity to the most developed part of the area and transportation.

## The Data

The dataset that our team selected for this application was the Location Affordability Index from the United States Department of Housing and Urban Development (United States Department of Housing and Urban Development, 2019). The data set contains data on differenet affordability criteria for each census tract in the United States including:

* Transportation Cost Data
* Housing Cost Data
* Population and Geoprofile Data
* Employment Data
* Detailed Household Profile Data

The location affordability index contains over 200,000 rows and 123 columns and is over 200MB in size. More information, including a data dictionary and download access, can be found here: [Location Affordability Index v.3 page](https://www.hudexchange.info/programs/location-affordability-index/).

The second dataset, the 2016 County and Place Federal Information Processing Standard (FIPS) codes, used comes from the United States Census Bureau (United States Census Bureau, 2017) and contains the county names FIPs codes from the Location Affordability Index dataset. The dataset can be found here: [2016 FIPS Codes](https://www.census.gov/geographies/reference-files/2016/demo/popest/2016-fips.html). This dataset was joined to the Location Affordability Index on the county level FIPS code.

Based on initial analysis of the data there are eight types of households that are classified in the data set:

*  type 1 - Typical HH
*  type 2 - Moderate HH 
*  type 3 - Dual Income HH
*  type 4 - Low Income HH
*  type 5 - Single Very Low Income
*  type 6 - Single Professional HH
*  type 7 - Single Worker HH
*  type 8 - Retirees

See technical documentation on HUD website for more information on household types: [Location Affordability Index v.3 page](https://www.hudexchange.info/programs/location-affordability-index/).

The dataset provides 13 columns that contain data unique to each household classifcation including:

* Household Income
* Household Size
* Household Number of Commuters
* Household Housing-Transportation Costs
* Household Housing Costs
* Household Owners Housing-Transportation Cost
* Household Owners Housing Costs
* Household Renters Housing-Transportation Costs
* Household Renters Housing Costs
* Household Transportation Costs
* Autos Per Household
* Annual Miles Per Household
* Annual Transit Trips Per Household

For data cleaning and processing we executed the following steps:

* The data for the Single Very Low Income (type 5) had little variability due to the fact that is based off of the national poverty level, which is consistent across all states, and therefore was not helpful in the analysis so it was removed. `<data_cont = data.drop(data[(data['State']=='Hawaii') | (data['State']== 'Alaska') | (data['State']== 'District of Columbia')].index)>`
* The data in states like Hawaii, Alaska, and Washington DC were also removed due to being outliers in population density and other factors. `<data = data.drop(data.columns[69:82], axis=1)>`
* Filtered for NaN Data `<data = data.dropna()>`

## Experimental Design
*The following is our step-by-step process from obtaining the data to finding results.*
1. Obtain datasets from Department of Housing and Urban Development (HUD) (United States Department of Housing and Urban Development, 2019) and Census Bureau (United States Census Bureau, 2017) websites via webscraping download links.
2. Read the two CSV files into 2 pandas (McKinney, W., & others. 2010) dataframes in Python
3. Merge county names column from the Census Bureau into the HUD dataset on the FIPS code column.
5. Examine & clean the data
6. Query and analyze the data (including Unit Testing of our code) in the following ways:
   * Visualizations
   * Descriptive Statistics

Once the analysis was complete, we used our knowledge to build an application to visualize affordability based on user input. See section Beyond the Original Specifications.

## Results

There are multiple fields that are characteristics of the locations:
* residential density
* employment access index
* job diversity index
* Median commute distance
* Per capita Income

Per capita Income
*This does not have a high correlation with any of the other variables which seems to indicate there is income avaiability regardless of things like employment access, job diversity, and residential density

![Figure 2](https://github.com/q-maze/location-affordability-tool/blob/main/Report/Scatter%20Plot%20of%20Main%20Measurements.png)

Highest Per Capita Income -The top 25 areas with the highest income appear to be concentrated in a few states.
* FL - 8
* NY - 7
* CA - 4

![Figure 3](https://github.com/q-maze/location-affordability-tool/blob/main/Report/Highest%20Income%20Per%20Capita.png)

Lowest Per Capita Income - The lowest 25 areas with smallest income are more spread out across more states.
![Figure 4](https://github.com/q-maze/location-affordability-tool/blob/main/Report/Lowest%20Income%20Per%20Capita.png)

Average of Per Capita Income, Typical Income, Housing Cost, Transportation Cost:
* Transportation Cost vs. Income & Housing
   * Clear negative correlation between Transportation cost and income (-.917433) and housing cost (-.532232).
   * Houses further from cities tend to be cheaper so more cost in transportation 
   * Higher percentage of income dedicated to trasnportation cost vs. equity in a house

![Figure 5](https://github.com/q-maze/location-affordability-tool/blob/main/Report/correlation%20plot.png)
![Figure 6](https://github.com/q-maze/location-affordability-tool/blob/main/Report/State%20Mean%20Data%20Scatterplot.png)

## Beyond the Original Specifications

For this project, we wanted to create a tool that provided the user to visualize the affordable locations in a given area. To accomplish this we created an application composed of two classes:

* class LocationAffordabilityIndex
  * Application class which contains the dataset stored in a pandas (McKinney, W., & others. 2010) dataframe and different methods to allow the user to manipulate and visualize this data, including the creation of a user-specific location affordability index.
* class LAIUser
  * Representation of the user's profile including desired state, income, work status, household profile, and transportation profile.

The application begins by creating an instance of the LocationAffordabilityIndex using data scraped from the download links, or from a local file. It then calls a method to prompt the user to supply information to build their profile. It then classifies the user based on their input and returns a pandas (McKinney, W., & others. 2010) dataframe that contains the affordable areas for the user to live in. This dataframe was then visualized using geopandas (Jordahl, K. 2014), which uses the state and country FIPS codes from the LocationAffordabilityIndex dataframe, and combines them with a county shape file that allows for visualization of the affordability of each location. 

![Figure 1](https://github.com/q-maze/location-affordability-tool/blob/main/Report/User%20Input%20Code.png)

This is an export for California based resident making $100,000.  The chart shows the least affordable locations based on income per capita.
![Figure 12](https://github.com/q-maze/location-affordability-tool/blob/main/Report/Figures/California%20Output.png)

Red represents highest median income and blue is lowest

![Figure 13](https://github.com/q-maze/location-affordability-tool/blob/main/Report/Figures/California.png)

## Testing

The following testing was conducted on this project:

1. Testing on the LAIUser class to ensure that the user profile is correctly set-up based on the provided user input. 
2. Testing on the LocationAffordabilityIndex class to ensure that the application is properly intialized from the supplied data source (scraped or from local file) and that the methods for assigning a user profile object (LAIUser) and returning the correct result dataframe are written correctly.

Sample output from our testing can be seen below:
![Figure 7](https://github.com/q-maze/location-affordability-tool/blob/main/Report/Figures/Testing%20Output.png)

## Conclusions
1. Key Findings and Use Cases
   1. Income is negatively correlated with Transportation costs (-.917433) meaning wealthier people tend to live closer to the city center and have less transportation costs overall.
   2. Transportation is also negatively correlated with housing cost (-.532232) just not as closely correlated.  Cheaper houses are further out which then require more transportation cost.  
   4. There are certain states that tend to have pockets of some of the wealthiest areas like Florida, New York, and California.
   5. This tool could be very useful to users that are interested in relocating to different areas of the country for work or personal reasons. It could also be useful to public officials that are interested in visualizing the affordable locations in their district, in order to promote new residents moving to those areas.

2. Future Improvements
   1. Find more recent data to do a comparison of how specific metropolitan areas fluctuated since 2016.
   2. Create a more accurate user input system to map users to the optimal household type. Currently we only map to 3 of the 8 household types.
   3. Utilize algorithms to identify similar affordability areas close to the user supplied desired location.
   4. Create affordability mapping down to the census tract level. Currently we only map to the county level, but if different shape files were acquired and utilized, we could map affordability to the census tract level.

## Bibliography

Jordahl, K. (2014). GeoPandas: Python tools for geographic data. URL: Https://Github. Com/Geopandas/Geopandas.

McKinney, W., & others. (2010). Data structures for statistical computing in python. In Proceedings of the 9th Python in Science Conference (Vol. 445, pp. 51–56).

United States Department of Housing and Urban Development. (2019). Location Affordability Index V3.0. United States Department of Housing and Urban Development. https://www.hudexchange.info/programs/location-affordability-index/

United States Census Bureau. (2017, May 5). 2016 FIPS Codes. https://www.census.gov/geographies/reference-files/2016/demo/popest/2016-fips.html


