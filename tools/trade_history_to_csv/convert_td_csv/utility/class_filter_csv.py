
# Modules
#   NA

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
        self.mActionDate = self.mNa
        self.mTicker = self.mNa
        self.mType = self.mNa
        self.mAction = self.mNa
        self.mQuantity = self.mNa
        self.mCost = self.mNa
        self.mCommission = self.mNa
        # Option specific
        self.mExpDate = self.mNa
        self.mStrike = self.mNa

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
        self.mOutputRow[ 0 ] = self.mActionDate
        self.mOutputRow[ 1 ] = self.mTicker
        self.mOutputRow[ 2 ] = self.mType
        self.mOutputRow[ 3 ] = self.mAction
        self.mOutputRow[ 4 ] = self.mQuantity
        self.mOutputRow[ 5 ] = self.mCost
        self.mOutputRow[ 6 ] = self.mCommission
        # Option Specific
        self.mOutputRow[ 7 ] = self.mExpDate
        self.mOutputRow[ 8 ] = self.mStrike

        return True

    def filterDescriptionColumn( self, pRow ):
        """
        Description:    
        Arguments:      
        Returns:        
        """

        # Sets input row for the object to use
        self.mInputRow = pRow

        # Setting Dates
        passed = self.setDateOfAction()
        if not passed:
            msg.error( __name__ + ": Couldn't set 'Date of Action.'", "TODO" )
            return False

        # Filters out description cell
        col_desc = self.mTdHeaders[ 2 ]
        print( "Target Cell: '" + str( pRow[ col_desc ] ) + "'" )


        return self.mOutputRow

    def setDateOfAction( self, date="no_input" ):
        """
        Description:    Finds the date of action in the input row, then sets the member
        Arguments:      date [ string ]:    Optional. Only used if user wants to override this date.
        Returns:        bool:   True for success, False for failure
        """

        # User can override this value
        if date == "no_input":
            mActionDate = date
            return True

        # Gets the row date and converts it to the correct format
        passed, self.mActionDate = self.formatData( mInputRow[ 0 ] )
        if not passed:
            msg.error( __name__ + ": Couldn't set 'Date of Action.'", "TODO" )
            return False

        return True


    def formatDate( self, pDate ):
        """
        Description:    Takes an input date and formats it to an expected form
        Arguments:      pDate [ string ]:   Date to be formatted
        Returns:        bool:   True for success, False for failure
                        string: The input date but in the correct format
        """

        # Variables
        date_list = pDate.split()
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
        elif new_month == 'Dec':
            new_date = '12'
        else:
            msg.error( "date_list[0] not expected: " + month)
            return False, new_date

        # Formats days with leading 0
        if len(day) < 2:
            day = int(day)
            day = str(day).zfill(2)

        # Finalize date format
        new_date += '/' + day + '/' + year

        return True, new_date


    def filterForOptions():
        """
        Description:    Filters the following from the description:
                            *   Puts:   Buy / Sell / Assigned / Expired
                            *   Calls:  Buy / Sell / Assigned / Expired
        Arguments:      
        Returns:        
        """

        return

    def filterForStocks():
        return

    def filterForOther():
        return
