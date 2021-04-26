from laiuserinput import *
from locationaffordabilityindex import *
import os

LAI = LocationAffordabilityIndex(
    lai_data_loc='C:/Users/qpmay/PycharmProjects/location-affordability-tool/data/smaller_LAI.csv',
    fips_d_loc='C:/Users/qpmay/PycharmProjects/location-affordability-tool/data/all-geocodes-v2016.xlsx')
user_prof = get_filters()
LAI.add_user_prof(user_prof)
LAI.show_affordable_locations()

