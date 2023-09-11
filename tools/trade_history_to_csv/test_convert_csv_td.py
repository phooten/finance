import unittest
import convert_csv_td

class TestInputCsvName( unittest.TestCase ):

    def test_incorrect_file_extension( self ):
        # File doesn't have .csv
        self.assertEqual( convert_csv_td.checkInputCsv("transactions_2022.cs"), False )
        self.assertEqual( convert_csv_td.checkInputCsv("transactions_2022csv"), False )
        self.assertEqual( convert_csv_td.checkInputCsv("transactions_2022.csvs"), False )
        self.assertEqual( convert_csv_td.checkInputCsv("transactions.csv_2022"), False )
        self.assertEqual( convert_csv_td.checkInputCsv("../../sensitive_files/transactions_2022.csv"), True )

        # This should be true, but issue comes up in the next test case because it doesn't exist
        #self.assertEqual( convert_csv_td.checkInputCsv("transactions_2022.csv")

    def test_input_exists( self ):
        # File doesn't exist
        result = convert_csv_td.checkInputCsv( "transactions_2022.csv" )
        self.assertEqual( result, False )

if __name__ == "__main__":
    unittest.main()
