
# Modules
import re

# Project Modules
from messages import class_messages

msg = class_messages.messages()

class csvFilter:


    def __init__( self ):

        self.mPlaceHolder = "PLACE-HOLDER"
        self.mNa = "NA"

        self.mMonths = [
                ( 'Jan', 1 ),
                ( 'Feb', 2 ),
                ( 'Mar', 3 ),
                ( 'Apr', 4 ),
                ( 'May', 5 ),
                ( 'Jun', 6 ),
                ( 'Jul', 7 ),
                ( 'Aug', 8 ),
                ( 'Sep', 9 ),
                ( 'Oct', 10 ),
                ( 'Nov', 11 ),
                ( 'Dec', 12 ) ]

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

        self.mOptionTypes = [ "Call", "Put" ]
        self.mStockTypes = [ "", "" ]

        self._mInputRow = []
        self.mOutputRow = []
        for curr in self.mOutputHeaders:
            self.mOutputRow.append( self.mPlaceHolder )

        # Sets each value to default, then is put into the output row
        self._mActionDate = self.mPlaceHolder
        self._mTicker = self.mPlaceHolder
        self._mType = self.mPlaceHolder
        self._mAction = self.mPlaceHolder
        self._mQuantity = self.mPlaceHolder
        self._mCost = self.mPlaceHolder
        self._mCommission = self.mPlaceHolder
        # Option specific
        self._mExpDate = self.mPlaceHolder
        self._mStrike = self.mPlaceHolder

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

    def filterTdAmeritradeDetails( self, pRow ):
        """
        Description:    
        Arguments:      
        Returns:        
        """

        # Sets input row for the object to use
        self.setInputRow( pRow )

        # Sets the Quantity of the transaction
        passed = self.findQuantity()
        if not passed:
            msg.error( __name__ + ": Couldn't set 'Quantity.'", "TODO" )
            return False

        # Sets the date of the Transaction
        passed = self.findDateOfAction()
        if not passed:
            msg.error( __name__ + ": Couldn't set 'Date of Action.'", "TODO" )
            return False

        # Sets the type of transaction
        passed = self.findType()
        if not passed:
            msg.error( __name__ + ": Couldn't set 'Type'", "TODO" )
            return False

        # Makes sure the type is set. After this point, filters depend on this.
        if self.getType() == self.mPlaceHolder:
            msg.error( __name__ + ": Cell type needs to be set before proceeding past this point.", "TODO" )
            return False

        # Sets the Action of the transaction
        passed = self.findAction()
        if not passed:
            msg.error( __name__ + ": Couldn't set 'Action'", "TODO" )
            return False

        # Only finds Expiration date if an option
        if self.getType() in self.mOptionTypes:
            passed = self.findDateOfExpiration()
            if not passed:
                msg.error( __name__ + ": Couldn't set 'Date of Expiration.'", "TODO" )
                return False
        else:
            self.setExpDate( self.mNa )

        # Sets the output row
        self.setOutputRow()
        if not passed:
            msg.error( __name__ + ": Couldn't set 'Output Row.'", "TODO" )
            return False

        # Checks the output row
        # for curr in range( len( self.mOutputRow ) ):
        #     if self.mOutputRow[ curr ] == self.mPlaceHolder:
        #         msg.system( "NOTE: '" + self.mOutputHeaders[ curr ] + "' isn't set. Current value is: " + self.mOutputRow[ curr ], "TODO" )

        return self.mOutputRow


    def findType( self ):
        # TODO: Write Unit test for this function
        """
        Description:    
        Arguments:      
        Returns:        bool:   True for success, False for failure
        """

        passed, description_cell = self.getDescriptionCell()
        if not passed:
            msg.Error( "Couldn't find a description cell in the input.", "TODO" )
            return False

        for curr in self.mOptionTypes:
            if curr in description_cell:
                self.setType( curr )
                return True

        # TODO: Figure out how this is associated with call / put, and don't hard code it
        if "OPTION" in description_cell:
            self.setType( "Option" )
            return True


        other_types = [ "FREE BALANCE INTEREST ADJUSTMENT",
                        "CLIENT REQUESTED ELECTRONIC FUNDING RECEIPT",
                        "MARGIN INTEREST ADJUSTMENT",
                        "MANDATORY - EXCHANGE"
                        ]
        for curr in other_types:
            if curr in description_cell:
                self.setType( "Other" )
                return True

        self.setType( "Stock" )
        return True


    def findAction( self ):
        # TODO: Write Unit test for this function
        """
        Description:    
        Arguments:      
        Returns:        bool:   True for success, False for failure
        """

        passed, description_cell = self.getDescriptionCell()
        if not passed:
            msg.Error( "Couldn't find a description cell in the input.", "TODO" )
            return False

        # Capitalization matters
        action_types = [
                    "ASSIGNMENT",
                    "EXPIRATION",
                    "Bought",
                    "Sold" ]
        for curr in action_types:
            if curr in description_cell:
                self.setAction( curr.lower().capitalize() )
                return True

        # TODO: Don't hard code this. Fix this in the findType() too.
        if "CLIENT REQUESTED ELECTRONIC FUNDING RECEIPT" in description_cell:
            self.setAction( "Fund Transfer" )
            return True
        elif "MARGIN INTEREST ADJUSTMENT" in description_cell:
            self.setAction( "Interest Adjustment: Margin" )
            return True
        elif "FREE BALANCE INTEREST ADJUSTMENT" in description_cell:
            self.setAction( "Interest Adjustment: Free Balance" )
            return True
        

        # TODO: Don't hard code this 'other' portion. Fix it in the type too.
        if self.getType() == "Other":
            self.setAction( self.mNa )
            return True

        msg.error( "Couldn't find action '" + str( action_types ) + "' in description_cell '" + description_cell + "'.", "TODO" )
        return False


    def findQuantity( self ):
        # TODO: Write unit test for this function
        """
        Description:    
        Arguments:      
        Returns:        bool:   True for success, False for failure
        """

        # Gets the row date and converts it to the correct format
        # TODO: Get rid of the hard coded value
        quantity = self._mInputRow[ 3 ]
        if quantity == "":
            self.setQuantity( self.mNa )
            return True

        try:
            quantity = int( quantity )
        except ValueError:
            msg.error( __name__ + ": Input cell for 'Quantity' is not a number and is not blank: '" + str( quantity ) + "'", "TODO" )
            return False

        if not quantity > 0:
            msg.error( __name__ + ": Input cell for 'Quantity' is less than 0.", "TODO" )
            return False

        self.setQuantity( quantity )

        return True

`
    def findDateOfAction( self ):
        """
        Description:    Finds the date of action in the input row, then sets the member. Currently acts as a wrapper to
                        formatDate, but it might change so should be left as is.
        Arguments:      date [ string ]:    Optional. Only used if user wants to override this date.
        Returns:        bool:   True for success, False for failure
        """

        # Gets the row date and converts it to the correct format
        # TODO: Get rid of the hard coded value
        passed, action_date = self.formatDate( self._mInputRow[ 0 ] )
        if not passed:
            msg.error( __name__ + ": Couldn't set 'Date of Action.'", "TODO" )
            return False

        self.setActionDate( action_date )
        return True


    def findDateOfExpiration( self ):
        # TODO: Write Unit test for this function
        """
        Description:    Finds the date of expiration in the input row, then sets the member.
        Arguments:      date [ string ]:    Optional. Only used if user wants to override this date.
        Returns:        bool:   True for success, False for failure
        """


        passed, description_cell = self.getDescriptionCell()
        if not passed:
            msg.system( "Couldn't find a description cell in the input.", "TODO" )
            return False

        description_list = description_cell.split()
        index = -1
        for month in self.mMonths:
            try:
                index = description_list.index( month[0] )
                break
            except ValueError:
                # TODO: Except is required, but not sure what to put
                index = -1

        # TODO: Don't hard code -1
        if index == -1:
            msg.error( "Expiration date not found in " + __name__ + ".", "TODO" )
            return False
        else:
            exp_date = description_list[ index ] + " " + description_list[ index + 1 ] + " " + description_list[ index + 2 ]
            passed, exp_date = self.formatDate( exp_date )
            if not passed:
                msg.error("Issue formatting Expiration date: '" + exp_date, "TODO" )
                return False

            self.setExpDate( exp_date )

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
        self._mType = value
        return

    def getAction( self ):
        return self._mAction

    def setAction( self, value ):
        self._mAction = value
        return

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
