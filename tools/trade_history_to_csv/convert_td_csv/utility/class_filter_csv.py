
# Modules
import re

# Project Modules
from messages import class_messages

msg = class_messages.messages()

class csvFilter:


    def __init__( self ):

        self.mNa = "NA"

        # TD Ameritrade Column Names
        self.mTdHeaders = [
                'DATE',
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

        # Headers for the new output csv
        self.mOutputHeaders = [
                 'DATE OF ACTION',
                 'TICKER',
                 'TYPE',     # Call, Put, Stock, Other
                 'ACTION',   # Buy, Sell, Assigned, Exercised, Dividend
                 'QUANTITY',
                 'COST',
                 'COMMISSION',
                 # Option specific
                 'DATE OF EXPIRATION',
                 'STRIKE PRICE' ]

        self.mInputRow = []
        self.mOutputRow = []
        for curr in self.mOutputHeaders:
            self.mOutputRow.append( self.mNa )

        # Sets each value to default, then is put into the output row
        self._mActionDate = self.mNa
        self._mTicker = self.mNa
        self._mType = self.mNa
        self._mAction = self.mNa
        self._mQuantity = self.mNa
        self._mCost = self.mNa
        self._mCommission = self.mNa
        # Option specific
        self._mExpDate = self.mNa
        self._mStrike = self.mNa

        # Sets output row to default values
        self.setOutputRow()

        # Checks the row was set correctly
        if len( self.mOutputRow ) is not len( self.mOutputHeaders ):
            msg.error( "DEVELOPER: Issue using csvFilter::__init__(). OutputRow cell count is not equal to OutputHeaders cell count", "TODO")
            msg.quit_script()

        return


    def setOutputRow( self ):
        """
        Description:    Sets the output row to cetain class value
        Arguments:      None.
        Returns:        Bool - True for Success, False for Failure
        """

        # Makes List
        self.mOutputRow[ 0 ] = self.getActionDate()
        self.mOutputRow[ 1 ] = self.getTicker()
        self.mOutputRow[ 2 ] = self.getType()
        self.mOutputRow[ 3 ] = self.getAction()
        self.mOutputRow[ 4 ] = self.getQuantity()
        self.mOutputRow[ 5 ] = self.getCost()
        self.mOutputRow[ 6 ] = self.getCommission()
        # Option Specific
        self.mOutputRow[ 7 ] = self.getExpDate()
        self.mOutputRow[ 8 ] = self.getStrike()

        return True

    def filterDescriptionColumn( self, pRow ):
        """
        Description:    
        Arguments:      
        Returns:        
        """

        # Sets input row for the object to use
        self.setInputRow( pRow )

        # Setting Dates
        passed = self.findDateOfAction()
        if not passed:
            msg.error( __name__ + ": Couldn't set 'Date of Action.'", "TODO" )
            return False

        passed = self.setDateOfExpiration()
        if not passed:
            msg.error( __name__ + ": Couldn't set 'Date of Expiration.'", "TODO" )
            return False

        # Filters out description cell
        col_desc = self.mTdHeaders[ 2 ]
        print( "Target Cell: '" + str( pRow[ col_desc ] ) + "'" )

        # Sets the output row
        self.setOutputRow()
        if not passed:
            msg.error( __name__ + ": Couldn't set 'Output Row.'", "TODO" )
            return False

        # Checks the output row
        for curr in range( len( self.mOutputRow ) ):
            if self.mOutputRow[ curr ] == self.mNa:
                msg.system( "NOTE: '" + self.mOutputHeaders[ curr ] + "' isn't set. Current value is: " + self.mOutputRow[ curr ], "TODO" )

        return self.mOutputRow


    def findDateOfAction( self ):
        """
        Description:    Finds the date of action in the input row, then sets the member. Currently acts as a wrapper to
                        formatDate, but it might change so should be left as is.
        Arguments:      date [ string ]:    Optional. Only used if user wants to override this date.
        Returns:        bool:   True for success, False for failure
        """

        # Gets the row date and converts it to the correct format
        # TODO: Get rid of the hard coded value
        passed, self.mActionDate = self.formatDate( self.mInputRow[ 0 ] )
        if not passed:
            msg.error( __name__ + ": Couldn't set 'Date of Action.'", "TODO" )
            return False

        return True


    def findDateOfExpiration( self ):
        """
        Description:    Finds the date of expiration in the input row, then sets the member.
        Arguments:      date [ string ]:    Optional. Only used if user wants to override this date.
        Returns:        bool:   True for success, False for failure
        """

        passed, description_cell = self.getDesciptionCell()
        if not passed:
            msg.system( "Couldn't find a description cell in the input.", "TODO" )
            return False

        # TODO: Write code to find the expiration date.


        return True


    def formatDate( self, pDate ):
        """
        Description:    Takes an input date and formats it to an expected form
        Arguments:      pDate [ string ]:   Date to be formatted
        Returns:        bool:   True for success, False for failure
                        string: The input date but in the correct format
        """

        # Checks format is ##/##/##
        # Regex: '[0-9]' is any digit. '$' signifies end of the line. '^' signifies start of the line.
        if re.match( r"^[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]$", pDate ):
            return True, pDate

        # If not in '##/##/####' but has two '/', fail the check
        date_list = pDate.split()
        if len( date_list ) != 3:
            msg.error( "Format of input date should be '##/##/####' or 'Abc DD YYYY'", "TODO" )
            return False, pDate

        month = date_list[0]
        day = date_list[1]
        year = date_list[2]

        # TODO: Don't like the hard coding
        # TODO: switch statement isn't supported in python?
        # Assign number for month
        if month == 'Jan':
            new_date = '01'
        elif month == 'Feb':
            new_date = '02'
        elif month == 'Mar':
            new_date = '03'
        elif month == 'Apr':
            new_date = '04'
        elif month == 'May':
            new_date = '05'
        elif month == 'Jun':
            new_date = '06'
        elif month == 'Jul':
            new_date = '07'
        elif month == 'Aug':
            new_date = '08'
        elif month == 'Sep':
            new_date = '09'
        elif month == 'Oct':
            new_date = '10'
        elif month == 'Nov':
            new_date = '11'
        elif month == 'Dec':
            new_date = '12'
        else:
            msg.error( "date_list[0] not expected: " + month, "TODO" )
            return False, pDate

        # Formats days with leading 0
        if len(day) < 2:
            day = int(day)
            day = str(day).zfill(2)

        # Finalize date format
        new_date += '/' + day + '/' + year

        return True, new_date


    def getDescriptionCell( self ):
        """
        Description:    Finds the expected cell in the input row
        Arguments:      none
        Returns:        bool:   True for success, False for failure
                        string: The input date but in the correct format
        """

        # Gets the position of the expected cell
        position = 0
        found = False
        for header in self.mTdHeaders:
            if header == "DESCRIPTION":
                found = True
                break
            position += 1

        # Couldn't find header
        if not found:
            msg.error( "Couldn't find 'DESCRIPTION' in TdHeader.", "TODO" )
            return False, "ERROR"

        # Position returned is greater than rows from intput
        input_row = self.getInputRow()
        if position > len( input_row ) - 1:
            msg.error( "Description cell found at position '" + str( position ) + "', but last position of input row is '" + str( len( input_row ) - 1 ) + "'.", "TODO" )
            return False, "ERROR"

        description_cell = input_row[ position ]

        return True, description_cell


    def filterForOptions( self ):
        """
        Description:    Filters the following from the description:
                            *   Puts:   Buy / Sell / Assigned / Expired
                            *   Calls:  Buy / Sell / Assigned / Expired
        Arguments:      
        Returns:        
        """

        return

    def filterForStocks( self ):
        return

    def filterForOther( self ):
        return

# Getters / Setters
    def getActionDate( self ):
        return self._mActionDate

    def setActionDate( self, value ):
        self._mActionDate = value
        return

    def getTicker( self ):
        return self._mTicker

    def setTicker( self, value ):
        self._mTicker = value
        return

    def getType( self ):
        return self._mType

    def setType( self, value ):
        self._mTicker = value
        return

    def getAction( self ):
        return self._mAction

    def setAction( self, value ):
        self._mAction = value
        reutrn

    def getQuantity( self ):
        return self._mQuantity

    def setQuantity( self, value ):
        self._mQuantity = value
        return

    def getCost( self ):
        return self._mCost

    def setCost( self, value ):
        self._mCost = value
        return

    def getCommission( self ):
        return self._mCommission

    def setCommision( self, value ):
        self._mCommission = value
        return

    def getExpDate( self ):
        return self._mExpDate

    def setExpDate( self, value ):
        self._mExpDate = value
        return

    def getStrike( self ):
        return self._mStrike

    def setStrike( self, value ):
        self._mStrike = value
        return

    def getInputRow( self ):
        return self._mInputRow

    def setInputRow( self, value ):
        self._mInputRow = value
        return
