# Modules
import unittest

# Local Modules
from utility import class_filter_csv


class TestClassFilterCsv( unittest.TestCase ):
    @classmethod
    def setUpClass( cls ):
        print("\nsetUpClass method: Runs before all tests...")

    def setUp( self ):
        print("\nRunning setUp method...")
        self.filter = class_filter_csv.csvFilter()

    def tearDown(self):
        print("Running tearDown method...")

    def test_set_output_row( self ):
        # No checks currently. Will always return true
        self.assertEqual( self.filter.setOutputRow(), True )

    def test_format_date( self ):
        # Bad formats
        dates = [   "001/31/20233",
                    "1/31/20233",
                    "01/31/20233",
                    "01/31/202",
                    "underline_here",
                    "space here" ]
        for date in dates:
            self.assertEqual( self.filter.formatDate( date ), ( False, date ) )

        # Good formats
        dates = [   "01/31/2023",
                    "Mar 12 2021" ]
        for date in dates:
            self.assertEqual( self.filter.formatDate( date ), ( True, date ) )


    @classmethod

    def tearDownClass(cls):
        print("\ntearDownClass method: Runs after all tests...")

if __name__ == "__main__":
    unittest.main()
