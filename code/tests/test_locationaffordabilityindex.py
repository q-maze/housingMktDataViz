from locationaffordabilityindex import *
import laiuser
import unittest


class TestLAI(unittest.TestCase):
    def setUp(self):
        self.LAI = LocationAffordabilityIndex()

        self.LAI2 = LocationAffordabilityIndex()

        self.user = laiuser.LAIUser('utah', 100000, 'renting', 'yes', 'retired', 'driving')
        self.user.classify_user()

        self.LAI2.add_user_prof(self.user)

    def test_init(self):
        # check to make sure the file locations are stored properly
        self.assertNotEqual(self.LAI.lai_csv_file_path, None)
        self.assertNotEqual(self.LAI.fips_data_file_path, None)
        # check to make sure the df instance variable is initialized correctly
        self.assertNotEqual(len(self.LAI.df.columns), 0)
        self.assertEqual(len(self.LAI.df.columns), 127)
        # check to make sure the user and by_county are blank until a profile is added
        self.assertEqual(self.LAI.user, None)
        self.assertEqual(self.LAI.by_county, None)

    def test_add_user_prof(self):
        # check to make sure the user object has been added
        self.assertNotEqual(self.LAI2.user, None)
        # check to make sure the length of the by_counties df is correct
        self.assertNotEqual(len(self.LAI2.by_county.columns), 0)

    def test_show_affordable_locations(self):
        # check to make sure the length of the by_counties df is correct
        self.assertNotEqual(len(self.LAI2.show_affordable_locations().columns), 0)
        self.assertEqual(len(self.LAI2.show_affordable_locations().columns), 24)



