# CS 5010 Group Project
---
- Quinton Mays (rub9ez)
- Matt Suozzi (mds5dd)
- Eric Pratsch (ewp4x)
---
## Introduction
The team was interested in learning more about patterns in housing affordability in the continental US.  We wanted to learn about overall trends as well as create an application for users to identify affordable places based on a target state at the county level.  

Users can be assisted in finding affordable locations based on a variety of factors like income, whether they rent or own, their household type like retired or dual income, and the state of choice.

## The Data
The team was able to find an open data set on US Department of Housing and Urban Development (HUD) website that focuses on location afforadbility data.  We were able to download the data (>200MB) from this [Location Affordability Index v.3 page](https://hudgis-hud.opendata.arcgis.com/datasets/location-affordability-index-v-3?geometry=-82.653%2C-52.642%2C83.284%2C85.381)  This data is as of 2016 and new information is added on an annual basis.

Based on initial analysis of the data there are eight types of households that are classified in the data set.   
*  type 1 - Typical HH - "Median Household" > 80%, < 150%
*  type 2 - Moderate HH - < 80%, > 50%
*  type 3 - Dual Income HH - > 150%
*  type 4 - Low Income HH - < 50%
*  type 5 - Single Very Low Income  < 11880
*  type 6 - Single Professional HH - > 135%
*  type 7 - Single Worker HH - < 50%
*  type 8 - Retirees - 80% Median

The data for the Single Very Low Income had little variability so was not helpful in the analysis so that was removed.  
`<data_cont = data.drop(data[(data['State']=='Hawaii') | (data['State']== 'Alaska') | (data['State']== 'District of Columbia')].index)>`

The data in states like Hawaii, Alaska, and Washington DC were also removed due to being outliers in population density and other factors.
`<data = data.drop(data.columns[69:82], axis=1)>`

Filtered for NaN Data
`<data = data.dropna()>`

## Top Level Analysis
There are multiple fields that are characteristics of the locations:
* residential density
* employment access index
* job diversity index
* Median commute distance
* Per capita Income

Per capita Income
*This does not have a high correlation with any of the other variables which seems to indicate there is income avaiability regardless of things like employment access, job diversity, and residential density

![Figure 1](https://github.com/q-maze/location-affordability-tool/blob/main/Report/Scatter%20Plot%20of%20Main%20Measurements.png)

Highest Per Capita Income -The top 25 areas with the highest income appear to be concentrated in a few states.
*FL - 8
*NY - 7
*CA - 4
![Figure 2](https://github.com/q-maze/location-affordability-tool/blob/main/Report/Highest%20Income%20Per%20Capita.png)

Lowest Per Capita Income - The lowest 25 areas with smallest income are more spread out 
![Figure 3](https://github.com/q-maze/location-affordability-tool/blob/main/Report/Lowest%20Income%20Per%20Capita.png)
Average of Per Capita Income, Typical Income, Housing Cost, Transportation Cost:
*Transportation Cost vs. Income & Housing
   *Clear negative correlation between Transportation cost and income (-.917433) and housing cost (-.532232.
   *Houses further from cities tend to be cheaper so more cost in transportation 
   *Higher percentage of income dedicated to trasnportation cost vs. equity in a house
![Figure 4](https://github.com/q-maze/location-affordability-tool/blob/main/Report/correlation%20plot.png)
![Figure 5](https://github.com/q-maze/location-affordability-tool/blob/main/Report/State%20Mean%20Data%20Scatterplot.png)

## Experimental Design
*The following is our step-by-step process from obtaining the data to finding
results.*
1. Obtain data

2. Examine & clean the data
   1. 
3. Read the two CSV files into 2 dataframes in Python
4. Append a column to the dataframe with the number of Starbucks within an x (ex: 5) mile radius of each apartment.
5. Query and analyze the data (including Unit Testing of our code) in the
following ways:
   1. Regression analysis with price as the dependent variable
   2. Visualize and descriptive statistics
   3. Prediction models for determining which city a listing is in based on price, bedrooms, bathrooms, and square feet
   4. Prediction models for the number of bedrooms based on price and bathrooms
   5. Determine general relationship between the number of bedrooms and number of bathrooms in apartments
   6. General bar and scatter plots to understand relationship between variables using df display GUI
6. Write up our results with tables & visualizations


## Results


## Conclusions
1. Key Findings and Use Cases
   1. It was interesting to see that population density and 

2. Future Improvements (if we had more time)
   1. Find more recent data to do a comparison of how specific metropolitan areas fluctuated since 2016.
   2. Create a more accurate user input system to map users to the optimal household type.  Most of the analysis was based on the type 1 - Typical HH - "Median Household"
