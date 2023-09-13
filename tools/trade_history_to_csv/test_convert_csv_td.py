import unittest
import convert_csv_td

class TestInputCsvName( unittest.TestCase ):

    def test_incorrect_file_extension( self ):
        # File doesn't have .csv
        self.assertEqual( convert_csv_td.initialCsvFileCheck("transactions_2022.cs"), False )
        self.assertEqual( convert_csv_td.initialCsvFileCheck("transactions_2022csv"), False )
        self.assertEqual( convert_csv_td.initialCsvFileCheck("transactions_2022.csvs"), False )
        self.assertEqual( convert_csv_td.initialCsvFileCheck("transactions.csv_2022"), False )
        self.assertEqual( convert_csv_td.initialCsvFileCheck("../../sensitive_files/transactions_2022.csv"), True )

        # This should be true, but issue comes up in the next test case because it doesn't exist
        #self.assertEqual( convert_csv_td.initialCsvFileCheck("transactions_2022.csv")

    def test_input_exists( self ):
        # File doesn't exist
        self.assertEqual( convert_csv_td.initialCsvFileCheck( "transactions_2022.csv" ), False )
        self.assertEqual( convert_csv_td.initialCsvFileCheck("../../sensitive_files/transactions_2022.csv"), True )

# TODO: Figure out how to structure unit code
#class TestCsvContents( unittest.TestCase ):
#    def test_contents_of_csv_check:
#        self.assetEqual( convert_csv_td.contentsCsvFileCheck( ), )



if __name__ == "__main__":
    unittest.main()
