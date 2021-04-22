import pandas as pd  # for storing the data
import laiuser
import numpy as np


# class for representing a data object containing all aspects of Location Affordability Index (LAI) data
# contains methods for merging county names from Federal Information Processing Standards (FIPS) dataset


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
        fips_df = pd.read_excel(self.fips_data_file_path,
                                header=None, index_col=None)
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

    #  type 1 - Typical HH - "Median Household" > 80%, < 150%
    #  type 2 - Moderate HH - < 80%, > 50%
    #  type 3 - Dual Income HH - > 150%
    #  type 4 - Low Income HH - < 50%
    #  type 5 - Single Very Low Income  < 11880
    #  type 6 - Single Professional HH - > 135%
    #  type 7 - Single Worker HH - < 50%
    #  type 8 - Retirees - 80% Median
    def add_user_prof(self, user):
        self.user = user
        self.df['classification'] = 'type_8'

        if user.classification == 'single':
            if self.user.income < 11880:
                self.df['classification'] = 'type_5'
            else:
                self.df['classification'] = np.where(self.df['per_capita_income'] > self.user.income * (1 / 1.35),
                                                     'type_6')
                self.df['classification'] = np.where(self.df['per_capita_income'] < self.user.income * (1 / 1.35),
                                                     'type_7')
        else:
            self.df['classification'] = np.where(self.df['per_capita_income'] > self.user.income * (1 / 0.5),
                                                 'type_4')
            self.df['classification'] = np.where(self.user.income * (1 / 0.5) > self.df['per_capita_income'] > self.user.income * (1 / 0.8), 'type_3')
            self.df['classification'] = np.where(self.df['per_capita_income'] > self.user.income * 1.5, 'type_2')


if __name__ == "__main__":
    # THIS CODE TAKES A LONG TIME TO EXECUTE IF INTERNET SPEED ISN'T GOOD (> 1MIN)
    # will provide local copies of all the files in your current directory
    # run this code and then add the file names to the class constructor
    # LAI.csv/smaller_LAI.csv and all-geocodes-v2016.xlsx
    data = LocationAffordabilityIndex()
    data.to_csv()
    data.to_smaller_csv()
    data.store_fips()
