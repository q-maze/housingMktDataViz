#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 05:49:53 2021

@author: Pratsch
"""

import pandas as pd


STATE_DATA = { 'alabama':'AL','alaska':'AK','arizona':'AZ','arkansas':'AZ','california':'CA'
              ,'colorado':'CO','connecticut':'CT','delaware':'DE','florida':'FL','georgia':'GA'
              ,'hawaii':'HI','idaho':'ID','illinois':'IL','indiana':'IN','iowa':'IA','kansas':'KS'
              ,'kentucky':'KY','louisiana':'LA','maine':'ME','maryland':'MD',
              'massachusetts':'MA','michigan':'MI','minnesota':'MN','mississippi':'MS','missouri':'MO'
              ,'montana':'MT','nebraska':'NE','nevada':'NV','New Hampshire':'NH'
              ,'new jersey':'NJ','new mexico':'NM','new york':'NY','north carolina':'NC'
              , 'north dakota':'ND','ohio':'OH','oklahoma':'OK','oregon':'OR',
              'pennsylvania':'PA','rhode island':'RI','south carolina':'SC','south dakota':'SD'
              ,'tennesee':'TN','texas':'TX','utah':'UT','vermont':'VT',
              'virginia':'VA','washington':'WA','west virginia':'WV','wisconsin':'WI'
              ,'wyoming':'WY','washington dc':'dc'}

#Function to take inputs from the user and validate the values
def get_filters():
    #Grab all inputs of the user
    print('Hello! Let\'s find you an affordable place!')
    # Get user's State
    while True:
        try:
            state = str(input('Please enter a State you are interested in: ').lower())
            if state in STATE_DATA.keys():
                state=STATE_DATA.get(state)
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
            
    #If not retired, type of household
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
            
    
    #Prefer Public Transit or Driving     
    while True:
        try:
            transport = str(input('Do you prefer Public Transit or Driving?\
            \nEnter Public Transit or Driving: ').lower())
            if transport == 'public transit' or transport == 'driving':
                break
            print("Invalid Answer Entered")
        except Exception as e:
            print(e)
            
    print('-'*40)
    
    return state, income, living, work, household, transport



state, income, living, work, household, transport = get_filters()
print(state)
print(income)
print(living)
print(work)
print(household)
print(transport)


filename = '/Users/Pratsch/CS_Project/Location_Affordability_Index_v_1.0.csv'
df = pd.DataFrame(pd.read_csv(filename))

dfstate = df.loc[df['SF1_BlockGroups_ST_ABBREV'] == state]
print(dfstate['per_capita_income'].describe())
