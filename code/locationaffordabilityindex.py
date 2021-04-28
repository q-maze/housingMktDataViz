import numpy as np
import pandas as pd
from laiuser import *
# import geopandas


class LocationAffordabilityIndex:
    # constructor for class, takes one argument csv_file_path
    # if filepath variable is not supplied, retrieves fresh csv from URL
    def __init__(self, lai_data_loc='https://opendata.arcgis.com/datasets/8eaa0b89826244ae9246915199462328_0.csv',
                 fips_d_loc='https://www2.census.gov/programs-surveys/popest/geographies/2016/all-geocodes-v2016.xlsx'):
        self.lai_csv_file_path = lai_data_loc
        self.fips_data_file_path = fips_d_loc

        # read in LAI data from chosen data source
        self.df = pd.read_csv(self.lai_csv_file_path)

        # format the LAI data for state and county to match formatting from country fips data set
        self.df['BlockGroups_COUNTYFP10'] = self.df['BlockGroups_COUNTYFP10'].astype(str)
        self.df['BlockGroups_STATEFP10'] = self.df['BlockGroups_STATEFP10'].astype(str)
        self.df['BlockGroups_COUNTYFP10'] = self.df['BlockGroups_COUNTYFP10'].apply(lambda x: x.zfill(3))
        self.df['BlockGroups_STATEFP10'] = self.df['BlockGroups_STATEFP10'].apply(lambda x: x.zfill(2))
        # then add a column concat of the state and county
        self.df['State-County'] = self.df['BlockGroups_STATEFP10'] + self.df['BlockGroups_COUNTYFP10']

        # merge the two data sets
        fips = self.get_county_names()
        self.df = self.df.merge(fips, how='left',
                                on='State-County')
        self.user = None
        self.by_county = None

    # function to output current main dataframe to a csv file in the local directory
    def to_csv(self, filename='LAI.csv'):
        self.df.to_csv(filename)

    # function to create a smaller csv (500 lines) of random lines from df in the local directory
    def to_smaller_csv(self, filename='smaller_LAI.csv'):
        smaller_df = self.df.sample(n=500)
        smaller_df.to_csv(filename)

    def store_fips(self):
        fips = self.get_county_names()
        fips.to_excel('all-geocodes-v2016.xlsx')

    # Returns a dataframe containing FIPS State-County Code and associated county name
    def get_county_names(self):
        # read in the excel file from the supplied location or if none supplied, Census URL
        if self.fips_data_file_path.endswith('.xlsx'):
            fips_df = pd.read_excel(self.fips_data_file_path,
                                    header=None,
                                    index_col=None,
                                    engine='openpyxl')
        else:
            fips_df = pd.read_csv(self.fips_data_file_path)
        # rename the columns to something nice
        # NOTE: ALL COLUMNS LABELED IN CASE WE WANT TO ADD FINER DETAIL (PLACE, CITY) TO APPLICATION LATER
        fips_df.columns = ['Sum_Lvl', 'State',
                           'County', 'Subdivision',
                           'Place', 'City',
                           'Area_Name']
        fips_df = fips_df.iloc[6:].reset_index()  # chop off the info rows at top of document

        # Queries the dataframe to only show the county names (can be removed for places later if needed)
        fips_df = fips_df.query('Sum_Lvl == "050" & Subdivision == "00000" & Place == "00000" & City == "00000"')
        fips_df = fips_df.iloc[:, 1:8].reset_index()
        # creates a state-county concatenation to search in LAI data
        fips_df['State-County'] = fips_df['State'] + fips_df['County']
        # returns only the state-county and area_name, which in this config is only the county names
        fips_df = fips_df[['State-County', 'Area_Name']].copy()
        return fips_df

    # adds a user profile column indicating if each area is affordable for the user to live in
    # we defined affordability to be if the median income in the area for the users classification was less than
    # 120% of the users income
    def add_user_prof(self, user):
        self.user = user
        self.by_county = self.df.groupby(['SF1_BlockGroups_ST_ABBREV','State-County']).mean().reset_index()
        self.by_county['affordable_area'] = np.where(
            self.by_county['hh_' + self.user.classification + '_income'] > self.user.income * 1.2,
            'na',
            'a')

    def show_affordable_locations(self):
        global_result_columns = ['SF1_BlockGroups_STATE_NAME',
                                 'SF1_BlockGroups_ST_ABBREV',
                                 'Area_Name',
                                 'affordable_area',
                                 'residential_density',
                                 'gross_hh_density',
                                 'block_denstiy',
                                 'intersection_density',
                                 'employment_access_index',
                                 'job_diversity_index',
                                 'average_median_commute_distance',
                                 'per_capita_income',
                                 'State-County']
        result_df = self.by_county
        result_df = result_df[result_df['SF1_BlockGroups_ST_ABBREV'] == self.user.state]
        result_df = result_df[result_df['affordable_area'] == 'a']
        user_classification_cols = [col for col in result_df.columns if self.user.classification in col]
        result_columns = global_result_columns + user_classification_cols
        result_df = result_df[result_df.columns & result_columns]
        result_df['county'] = result_df['State-County'].str[-3:]
        result_df = result_df.sort_values(by='per_capita_income')
        print(result_df.head(25))
