import numpy as np
import pandas as pd


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


    def add_user_prof(self, user):
        # classifies user into one of the following types:
        #  type 1 - Typical HH - "Median Household" > 80%, < 150%
        #  type 2 - Moderate HH - < 80%, > 50%
        #  type 3 - Dual Income HH - > 150%
        #  type 4 - Low Income HH - < 50%
        #  type 5 - Single Very Low Income  < 11880
        #  type 6 - Single Professional HH - > 135%
        #  type 7 - Single Worker HH - < 50%
        #  type 8 - Retirees - 80% Median
        self.user = user
        # if user is retired, fill classification column with type_8
        if self.user.classification == 'retired':
            self.df['classification'] = 'type_8'
        else:
            # else if not retired and single, compare income to criteria set out above
            # np.where does nothing if the user does not meet the criteria for each row.
            if user.classification == 'single':
                if self.user.income < 11880:
                    self.df['classification'] = 'type_5'
                else:
                    self.df['classification'] = np.where(self.df['per_capita_income'] > self.user.income * (1 / 1.35),
                                                         'type_6', self.df['classification'])
                    self.df['classification'] = np.where(self.df['per_capita_income'] < self.user.income * (1 / 1.35),
                                                         'type_7', self.df['classification'])
            # else if not retired and dual income, compare income to criteria set out above
            # np.where does nothing if the user does not meet the criteria for each row.
            else:
                self.df['classification'] = np.where(self.df['per_capita_income'] > self.user.income * (1 / 0.5),
                                                     'type_4', self.df['classification'])
                self.df['classification'] = np.where(
                    self.user.income * (1 / 0.5) > self.df['per_capita_income'] > self.user.income * (1 / 0.8),
                    'type_3', self.df['classification'])
                self.df['classification'] = np.where(self.df['per_capita_income'] > self.user.income * 1.5,
                                                     'type_2', self.df['classification'])

        
# class for describing the user input
class LAIUser:

    def __init__(self, state, income, living, work, household, transport):
        self.state = state
        self.income = income
        self.living = living
        self.work = work
        self.household = household
        self.transport = transport
        self.classification = None
# classifies a user as single, retired or dual income.        
    def classify_user(self):
        if self.work == 'no':
            if self.household == 'single':
                self.classification = 'single'
            else:
                self.classification = 'dual'
        else:
            self.classification = 'retired'


# Function to take inputs from the user and validate the values
def get_filters():
    STATE_DATA = {'alabama': 'AL', 'alaska': 'AK', 'arizona': 'AZ', 'arkansas': 'AZ', 'california': 'CA',
                  "colorado": 'CO', 'connecticut': 'CT', 'delaware': 'DE', 'florida': 'FL', 'georgia': 'GA',
                  'hawaii': 'HI', 'idaho': 'ID', 'illinois': 'IL', 'indiana': 'IN', 'iowa': 'IA', 'kansas': 'KS',
                  'kentucky': 'KY', 'louisiana': 'LA', 'maine': 'ME', 'maryland': 'MD',
                  'massachusetts': 'MA', 'michigan': 'MI', 'minnesota': 'MN', 'mississippi': 'MS', 'missouri': 'MO',
                  'montana': 'MT', 'nebraska': 'NE', 'nevada': 'NV', 'New Hampshire': 'NH',
                  'new jersey': 'NJ', 'new mexico': 'NM', 'new york': 'NY', 'north carolina': 'NC',
                  'north dakota': 'ND', 'ohio': 'OH', 'oklahoma': 'OK', 'oregon': 'OR',
                  'pennsylvania': 'PA', 'rhode island': 'RI', 'south carolina': 'SC', 'south dakota': 'SD',
                  'tennesee': 'TN', 'texas': 'TX', 'utah': 'UT', 'vermont': 'VT', 'virginia': 'VA', 'washington': 'WA',
                  'west virginia': 'WV', 'wisconsin': 'WI', 'wyoming': 'WY', 'washington dc': 'dc'}
    # Grab all inputs of the user
    print('Hello! Let\'s find you an affordable place!')
    # Get user's State
    while True:
        try:
            state = str(input('Please enter a State you are interested in: ').lower())
            if state in STATE_DATA.keys():
                state = STATE_DATA.get(state)
                break
            print("Please enter a valid state")
        except Exception as e:
            print(e)

    # Get user income level
    while True:
        try:
            income = int(input('Please enter your income: '))
            if income >= 0:
                break
            print("Please enter a valid income")
        except Exception as e:
            print(e)

    # Are you planning on owning a home or renting
    while True:
        try:
            living = str(input('Are you planning on Renting or Owning a Home?\
            \nEnter Renting or Owning: ').lower())
            if living == 'renting' or living == 'owning':
                break
            print("Invalid Answer Entered")
        except Exception as e:
            print(e)

    # Are you Retired or Working
    while True:
        try:
            work = str(input('Are you Retired?\
            \nEnter Yes or No: ').lower())
            if work == 'yes' or work == 'no':
                break
            print("Invalid Answer Entered")
        except Exception as e:
            print(e)

    # If not retired, type of household
    if work == 'no':
        while True:
            try:
                household = str(input('Single or Dual Income?\
                \nEnter Single or Dual: ').lower())
                if household == 'single' or household == 'dual':
                    break
                print("Invalid Answer Entered")
            except Exception as e:
                print(e)
    else:
        household = 'retired'

    # Prefer Public Transit or Driving
    while True:
        try:
            transport = str(input('Do you prefer Public Transit or Driving?\
            \nEnter Public Transit or Driving: ').lower())
            if transport == 'public transit' or transport == 'driving':
                break
            print("Invalid Answer Entered")
        except Exception as e:
            print(e)

    print('-' * 40)

    user = LAIUser(state, income, living, work, household, transport)
    user.classify_user()

    return user

if __name__ == '__main__':
    LAI = LocationAffordabilityIndex(lai_data_loc='smaller_LAI.csv',)
    user_prof = get_filters()
    LAI.add_user_prof(user_prof)
    print(LAI.df['classification'].nunique())
    print(LAI.df['classification'].head(5))
