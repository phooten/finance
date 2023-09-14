import unittest
import convert_csv_td

class TestInputCsvName( unittest.TestCase ):

    def test_incorrect_file_extension( self ):
        # File doesn't have .csv
        self.assertEqual( convert_csv_td.initialCsvFileCheck("unittest/transactions_2022.cs"), False )
        self.assertEqual( convert_csv_td.initialCsvFileCheck("unittest/transactions_2022csv"), False )
        self.assertEqual( convert_csv_td.initialCsvFileCheck("unittest/transactions_2022.csvs"), False )
        self.assertEqual( convert_csv_td.initialCsvFileCheck("unittest/transactions.csv_2022"), False )
        self.assertEqual( convert_csv_td.initialCsvFileCheck("unittest/transactions_2022.csv"), True )

        # This should be true, but issue comes up in the next test case because it doesn't exist
        #self.assertEqual( convert_csv_td.initialCsvFileCheck("transactions_2022.csv")

    def test_input_exists( self ):
        # File doesn't exist
        self.assertEqual( convert_csv_td.initialCsvFileCheck("unittest/does_not_exist.csv" ), False )
        self.assertEqual( convert_csv_td.initialCsvFileCheck("unittest/blank.csv"), False )
        self.assertEqual( convert_csv_td.initialCsvFileCheck("unittest/transactions_2022.csv"), True )

# TODO: Figure out how to structure unit code
class TestCsvContents( unittest.TestCase ):
    def test_contents_of_csv_check( self ):
        self.assertEqual( convert_csv_td.contentsCsvFileCheck("unittest/no_rows.csv"), False )
        self.assertEqual( convert_csv_td.contentsCsvFileCheck("unittest/one_row.csv"), True )


if __name__ == "__main__":
    unittest.main()
