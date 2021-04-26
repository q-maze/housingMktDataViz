from laiuserinput import *
from locationaffordabilityindex import *
import os

LAI = LocationAffordabilityIndex()
user_prof = get_filters()
LAI.add_user_prof(user_prof)
LAI.show_affordable_locations()

