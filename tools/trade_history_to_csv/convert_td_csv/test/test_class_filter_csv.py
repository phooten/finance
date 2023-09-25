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
        self.assertEqual( self.filter.setOutputRow(), True )


    #def test_filterTdAmeritradeDetails( self ):
        """
        Description:    Tests checks for this function, but not for other member functions that alreaddy have unit
                        tests. This would be redundant.
        """
        # TODO: Nothing to check right now.


    def test_findDateOfAction(self):
        """
        Description:    Place holder, since it currently acts as a wrapper to formatDate(). This needs to be updated if
                        the function ever changes.
        """
        # TODO: When the inputRow gets updated from being hardcoded to 0, this will also need to change because we're also
        #       Hardcoding the column to '0' here was well.
        # Bad Formats
        dates = [ ( "001/31/2023" ),
                  ( "1/31/20233" ) ] # Could keep going, but will be the same as test_formatDate()
        for date in dates:
            self.filter.setInputRow( date )
            self.assertEqual( self.filter.findDateOfAction(), False )

        # Good format
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
                    "underline_here",
                    "underline_goes_here",
                    "dot.here",
                    "dot.goes.here",
                    "space here",
                    "space goes here" ]
        for date in dates:
            self.assertEqual( self.filter.formatDate( date ), ( False, date ) )

        # Good formats: Already in a good format
        dates = [   "01/31/2023" ]
        for date in dates:
            self.assertEqual( self.filter.formatDate( date ), ( True, date ) )

        # Good format: ( input, expected )
        dates = [ ("Mar 12 2021", "03/12/2021"),
                 ("Jan 29 1997", "01/29/1997") ]
        for date in dates:
            self.assertEqual( self.filter.formatDate( date[0] ), ( True, date[1] ) )


    def test_getDescriptionCell( self ):
        # Description column doesn't exist in mTdHeaders
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

        # Description column is past what is expected for input row
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

        # Correct Case
        row = []
        for num in range( len( self.filter.mTdHeaders ) ):
            row.append( str( num ) )
        self.filter.setInputRow( row )
        # TODO: Don't like this hard coded
        self.assertEqual( self.filter.getDescriptionCell(), ( True, row[ 2 ] ) )
    @classmethod


    def tearDownClass(cls):
        print("\ntearDownClass method: Runs after all tests...")


if __name__ == "__main__":
    unittest.main()
