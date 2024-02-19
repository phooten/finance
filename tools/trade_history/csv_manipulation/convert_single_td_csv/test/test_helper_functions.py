import unittest
from utility import helper_functions

class TestInputCsvName( unittest.TestCase ):

    def test_incorrect_file_extension( self ):
        # File doesn't have .csv
        self.assertEqual( helper_functions.initialCsvFileCheck("test/csv_cases/transactions_2022.cs"), False )
        self.assertEqual( helper_functions.initialCsvFileCheck("test/csv_cases/transactions_2022csv"), False )
        self.assertEqual( helper_functions.initialCsvFileCheck("test/csv_cases/transactions_2022.csvs"), False )
        self.assertEqual( helper_functions.initialCsvFileCheck("test/csv_cases/transactions.csv_2022"), False )
        self.assertEqual( helper_functions.initialCsvFileCheck("test/csv_cases/correct_transactions.csv"), True )

        # This should be true, but issue comes up in the next test case because it doesn't exist
        #self.assertEqual( helper_functions.initialCsvFileCheck("transactions_2022.csv")

    def test_input_exists( self ):
        # File doesn't exist
        self.assertEqual( helper_functions.initialCsvFileCheck("test/csv_cases/does_not_exist.csv" ), False )
        self.assertEqual( helper_functions.initialCsvFileCheck("test/csv_cases/blank.csv"), False )
        self.assertEqual( helper_functions.initialCsvFileCheck("test/csv_cases/correct_transactions.csv"), True )

class TestCsvContents( unittest.TestCase ):
    def test_contents_of_csv_check( self ):
        # Row checks
        self.assertEqual( helper_functions.contentsCsvFileCheck("test/csv_cases/rows_none.csv"), False )
        self.assertEqual( helper_functions.contentsCsvFileCheck("test/csv_cases/rows_no_eof.csv"), False )
        self.assertEqual( helper_functions.contentsCsvFileCheck("test/csv_cases/rows_one.csv"), True )
        # TODO: case for too many rows

        # Column Checks
        self.assertEqual( helper_functions.contentsCsvFileCheck("test/csv_cases/headers_none.csv"), False )
        self.assertEqual( helper_functions.contentsCsvFileCheck("test/csv_cases/headers_incorrect.csv"), False )
        self.assertEqual( helper_functions.contentsCsvFileCheck("test/csv_cases/headers_one.csv"), False )
        self.assertEqual( helper_functions.contentsCsvFileCheck("test/csv_cases/headers_fifteen.csv"), False )
        self.assertEqual( helper_functions.contentsCsvFileCheck("test/csv_cases/headers_correct.csv"), True )


if __name__ == "__main__":
    unittest.main()
