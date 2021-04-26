# Class for defining a user profile for Location Affordability Index Tool

class LAIUser:
    # receives user input from strings and saves them to instance variables
    def __init__(self, state, income, living, work, household, transport):
        self.state = state
        self.income = income
        self.living = living
        self.work = work
        self.household = household
        self.transport = transport
        self.classification = None

    # classifies a user as single, retired or dual income.
    # classifies user into one of the following types:
    # type 1 - Dual Income
    # type 7 - Single Worker
    # type 8 - Retirees
    def classify_user(self):
        if self.work == 'no':
            if self.household == 'single':
                self.classification = 'type7'
            else:
                self.classification = 'type1'
        else:
            self.classification = 'type8'
