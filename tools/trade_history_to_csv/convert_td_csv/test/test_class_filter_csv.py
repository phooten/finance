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


    def test_setOutpuRow( self ):
        """
        Description:    Tests the setOuputRow member function. Currently there are no checks and will always return
                        true.
        """
        # Case: Nominal
        self.assertEqual( self.filter.setOutputRow(), True )


    #def test_filterTdAmeritradeDetails( self ):
        """
        Description:    Tests checks for this function, but not for other member functions that alreaddy have unit
                        tests. This would be redundant.
        """
        # TODO: Nothing to check right now.


    def test_findType( self ):
        """
        Description:    
        """

        # Depenedant on:
        #   getDescriptionRow / InputRow

        # Case: Failure, unkown
        nominal_other = [ "Charles just bought TdAmeritrade" ]
        for curr in nominal_other:
            self.filter.setInputRow( ["tmp", "tmp", curr ] )
            self.assertEqual( self.filter.findType(), False )

        # Case: Nominal for Options
        nominal_other = [ "REMOVAL OF OPTION DUE TO EXPIRATION (0CPNG.FA20013500)",
                            "Bought 1 PYPL May 6 2022 104.0 Call @ 0.01" ]
        for curr in nominal_other:
            self.filter.setInputRow( ["tmp", "tmp", curr ] )
            self.assertEqual( self.filter.findType(), True )

        # Case: Nominal for Stock
        nominal_other = [ "Bought 100 AMD @ 95",
                            "QUALIFIED DIVIDEND (MSFT)" ]
        for curr in nominal_other:
            self.filter.setInputRow( ["tmp", "tmp", curr ] )
            self.assertEqual( self.filter.findType(), True )

        # Case: Nominal for Other
        nominal_other = [ "FREE BALANCE INTEREST ADJUSTMENT",
                            "MARGIN INTEREST ADJUSTMENT",
                            "CLIENT REQUESTED ELECTRONIC FUNDING RECEIPT (FUNDS NOW)" ]
        for curr in nominal_other:
            self.filter.setInputRow( ["tmp", "tmp", curr ] )
            self.assertEqual( self.filter.findType(), True )


    def test_findQuantity( self ):
        """
        Description:    
        """
        # Failure
        # Case: Quantity is less than 0
        self.filter.setInputRow( ["tmp", "tmp", "tmp", -1 ] )
        self.assertEqual( self.filter.findQuantity(), False )

        # Case: Nominal
        self.filter.setInputRow( ["tmp", "tmp", "tmp", 10 ] )
        self.assertEqual( self.filter.findQuantity(), True)


    def test_findDateOfExpiration( self ):
        """
        Description:    
        """

        # Depenedant on:
        #   getDescriptionRow / InputRow
        #   formatDate()

        # Failure
        # Case: No month ( Jan, Feb, etc. ) doesn't exist
        self.filter.setInputRow( ["tmp", "tmp", "tmp" ] )
        self.assertEqual( self.filter.findDateOfExpiration(), False )

        # Case: Incorrect arguments after 'Month'
        self.filter.setInputRow( ["tmp", "tmp", "Jan" ] )
        self.assertEqual( self.filter.findDateOfExpiration(), False )
        self.filter.setInputRow( ["tmp", "tmp", "Jan 1" ] )
        self.assertEqual( self.filter.findDateOfExpiration(), False )
        self.filter.setInputRow( ["tmp", "tmp", "Jan 1 202" ] )
        self.assertEqual( self.filter.findDateOfExpiration(), False )

        # Case: Nominal
        self.filter.setInputRow( ["tmp", "tmp", "Jan 1 2023" ] )
        self.assertEqual( self.filter.findDateOfExpiration(), True )


    def test_findDateOfAction(self):
        """
        Description:    Place holder, since it currently acts as a wrapper to formatDate(). This needs to be updated if
                        the function ever changes.
        """
        # Failure
        # Case: Incorrect inputs
        dates = [ ( "001/31/2023" ),
                  ( "01/031/2023" ),
                  ( "1/31/20233" ) ] # Could keep going, but will be the same as test_formatDate()
        for date in dates:
            self.filter.setInputRow( date )
            self.assertEqual( self.filter.findDateOfAction(), False )

        # Case: Nominal
        self.filter.setInputRow( [ "01/31/2023" ] )
        self.assertEqual( self.filter.findDateOfAction(), True )


    def test_formatDate( self ):
        """
        Description:    Tests the formatDate member function
        """

        # Bad formats
        dates = [   "001/31/20233",
                    "1/31/20233",
                    "01/001/2023",
                    "01/31/20233",
                    "01/31/202",
                    "1/3/1",
                    "Jane 1 2023",
                    "Jan 1 1",
                    "Jan 1 1997",
                    "underline_here",
                    "underline_goes_here",
                    "dot.here",
                    "dot.goes.here",
                    "space here",
                    "space goes here" ]
        for date in dates:
            self.assertEqual( self.filter.formatDate( date ), ( False, date ) )

        # Good formats: Already in a good format
        dates = [ "01/31/2023" ]
        for date in dates:
            self.assertEqual( self.filter.formatDate( date ), ( True, date ) )

        # Good format: ( input, expected )
        dates = [ ("Mar 12 2021", "03/12/2021"),
                 ("Jan 29 2035", "01/29/2035") ]
        for date in dates:
            self.assertEqual( self.filter.formatDate( date[0] ), ( True, date[1] ) )


    def test_getDescriptionCell( self ):
        # Case: Description column doesn't exist in mTdHeaders
        self.filter.mTdHeaders = [  'DATE',
                                    'TRANSACTION ID',
                                    'ERROR_DESCRIPTION',
                                    'QUANTITY',
                                    'SYMBOL',
                                    'PRICE',
                                    'COMMISSION',
                                    'AMOUNT',
                                    'REG FEE',
                                    'SHORT-TERM RDM FEE',
                                    'FUND REDEMPTION FEE',
                                    ' DEFERRED SALES CHARGE' ]
        row = []
        for num in range( len( self.filter.mTdHeaders ) ):
            row.append( str( num ) )
        self.filter.setInputRow( row )
        self.assertEqual( self.filter.getDescriptionCell(), ( False, "ERROR" ) )

        # Case: Description column is past what is expected for input row / 
        self.filter.mTdHeaders = [  'DATE',
                                    'TRANSACTION ID',
                                    'DESCRIPTION',
                                    'QUANTITY',
                                    'SYMBOL',
                                    'PRICE',
                                    'COMMISSION',
                                    'AMOUNT',
                                    'REG FEE',
                                    'SHORT-TERM RDM FEE',
                                    'FUND REDEMPTION FEE',
                                    ' DEFERRED SALES CHARGE' ]
        # Intensionally making row too short
        row = [ "ONE", "TWO" ]
        self.filter.setInputRow( row )
        self.assertEqual( self.filter.getDescriptionCell(), ( False, "ERROR" ) )

        # Case: Nominal
        row = []
        for num in range( len( self.filter.mTdHeaders ) ):
            row.append( str( num ) )
        self.filter.setInputRow( row )
        self.assertEqual( self.filter.getDescriptionCell(), ( True, row[ 2 ] ) )
    @classmethod


    def tearDownClass(cls):
        print("\ntearDownClass method: Runs after all tests...")


if __name__ == "__main__":
    unittest.main()
