
# Modules
import re
import sys
import math

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
                 'PRICE',
                 'COMMISSION',
                 'AMOUNT',
                 # Option specific
                 'DATE OF EXPIRATION',
                 'STRIKE PRICE' ]

        self.mOptionTypesActive = [ "Call",
                                    "Put" ]
        self.mOptionTypesPassive = [ "ASSIGNMENT",
                                     "EXPIRATION" ]
        self.mOtherTypes = [ "CLIENT REQUESTED ELECTRONIC FUNDING RECEIPT",
                             "FREE BALANCE INTEREST ADJUSTMENT",
                             "MARGIN INTEREST ADJUSTMENT",
                             "MANDATORY - EXCHANGE" ]
        self.mStockTypes = [ "QUALIFIED DIVIDEND" ]

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
        self._mPrice = self.mPlaceHolder
        self._mCommission = self.mPlaceHolder
        self._mAmount = self.mPlaceHolder
        # Option specific
        self._mExpDate = self.mPlaceHolder
        self._mStrike = self.mPlaceHolder

        # Sets output row to default values
        self.setOutputRow()

        # Checks the row was set correctly
        if len( self.mOutputRow ) is not len( self.mOutputHeaders ):
            msg.error( "DEVELOPER: Issue using csvFilter::__init__(). OutputRow cell count is not equal to OutputHeaders cell count", __name__ )
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
        self.mOutputRow[ 5 ] = self.getPrice()
        self.mOutputRow[ 6 ] = self.getCommission()
        self.mOutputRow[ 7 ] = self.getAmount()
        # Option Specific
        self.mOutputRow[ 8 ] = self.getExpDate()
        self.mOutputRow[ 9 ] = self.getStrike()

        return True


    def filterTdAmeritradeDetails( self, pRow ):
        """
        Description:    
        Arguments:      
        Returns:        
        """
        method_name = self.getMethodName()

        # Sets input row for the object to use
        self.setInputRow( pRow )

        # Sets the Quantity of the transaction
        passed = self.findQuantity()
        if not passed:
            msg.error( "Couldn't find 'Quantity'.", method_name )
            return False

        # Sets the Price of the transaction ( Stock price, cost / value of option )
        passed = self.findPrice()
        if not passed:
            msg.error( "Couldn't find 'Price'.", method_name )
            return False

        # Sets the Commission cost of the transaction
        passed = self.findCommission()
        if not passed:
            msg.error( "Couldn't find 'Commission'.", method_name )
            return False

        # Sets the date of the Transaction
        passed = self.findDateOfAction()
        if not passed:
            msg.error( "Couldn't find 'Date of Action'.", method_name )
            return False

        # Sets the type of transaction
        passed = self.findType()
        if not passed:
            msg.error( "Couldn't find 'Type'.", method_name )
            return False

        # Makes sure the type is set. After this point, filters depend on this.
        if self.getType() == self.mPlaceHolder:
            msg.error( "Cell type needs to be set before proceeding past this point.", method_name )
            return False

        # Sets the Action of the transaction
        passed = self.findAction()
        if not passed:
            msg.error( "Couldn't find 'Action'", method_name )
            return False

        # Only finds Expiration date if an option
        passed = self.findDateOfExpiration()
        if not passed:
            msg.error( "Couldn't find 'Date of Expiration'.", method_name )
            return False

        passed = self.findTicker()
        if not passed:
            msg.error( "Couldn't find 'Ticker'.", method_name )
            return False


        # Sets the output row
        self.setOutputRow()
        if not passed:
            msg.error( "Couldn't find 'Output Row.'", method_name )
            return False

        # Checks the output row
        # for curr in range( len( self.mOutputRow ) ):
        #     if self.mOutputRow[ curr ] == self.mPlaceHolder:
        #         msg.system( "NOTE: '" + self.mOutputHeaders[ curr ] + "' isn't set. Current value is: " + self.mOutputRow[ curr ], method_name )

        return self.mOutputRow


    def findType( self ):
        """
        Description:    
        Arguments:      
        Returns:        bool:   True for success, False for failure
        """
        method_name = self.getMethodName()

        passed, description_cell = self.getDescriptionCell()
        if not passed:
            msg.Error( "Couldn't find a description cell in the input.", method_name )
            return False

        # Returns type if 'put' or 'call'
        for curr in self.mOptionTypesActive:
            if curr in description_cell:
                self.setType( curr )
                return True

        # Assigns 'Assignment' or 'Expiration' to type 'Option', which is meant to be a place holder. The TD CSV isn't
        # clear about which call / put was associated to it the 'Assignment' / 'Expiration'. The final type will be
        # a 'Put' or a 'Call'
        for curr in self.mOptionTypesPassive:
            if curr in description_cell:
                self.setType( "Option" )
                return True


        # Sets 'Other' as anything else that is relativley unrelated to trades
        for curr in self.mOtherTypes:
            if curr in description_cell:
                self.setType( "Other" )
                return True

        # If the trade doesn't do with any options but still relates to trades, set it to 'Stock'
        for curr in self.mStockTypes:
            if curr in description_cell:
                self.setType( "Stock" )
                return True

        # Some of these will be assigned strikes. These will need to be handled elsewhere
        # Matchs: start>(bought | sold ), any length of numbers, any length of capital letter, @, then any length of numbers(including a floatingpoint)<end
        if re.match( r"^(Bought|Sold) [0-9]+ [A-Z]+ @ ?([0-9]*[.])?[0-9]+$", description_cell ):
            self.setType( "Stock" )
            return True

        msg.error( "Issue setting type. Wasn't '" + str( self.mOptionTypesActive ) + ", 'Option', 'Stock', or 'Other'. See description cell:\n" + str( description_cell ), method_name )
        return False


    def findAction( self ):
        """
        Description:    
        Arguments:      
        Returns:        bool:   True for success, False for failure
        """
        method_name = self.getMethodName()

        passed, description_cell = self.getDescriptionCell()
        if not passed:
            msg.Error( "Couldn't find a description cell in the input.", method_name )
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

        msg.error( "Couldn't find action '" + str( action_types ) + "' in description_cell '" + description_cell + "'.", method_name )
        return False


    def findQuantity( self ):
        """
        Description:    
        Arguments:      
        Returns:        bool:   True for success, False for failure
        """
        method_name = self.getMethodName()

        # Gets the row date and converts it to the correct format
        input_row = self.getInputRow()
        quantity = input_row[ 3 ]
        if math.isnan( quantity ):
            self.setQuantity( self.mNa )
            return True

        # Force into an int, then check
        quantity = int( quantity )
        if not quantity > 0:
            msg.error( __name__ + ": Input cell for 'Quantity' is less than 0. See input row:\n" + str( input_row ), method_name )
            return False

        self.setQuantity( quantity )
        return True


    def findPrice( self ):
        """
        Description:    
        Arguments:      
        Returns:        bool:   True for success, False for failure
        """
        method_name = self.getMethodName()

        # Gets the row date and converts it to the correct format
        input_row = self.getInputRow()
        price = input_row[ 5 ]
        if math.isnan( price ):
            self.setPrice( self.mNa )
            return True

        # Force into an int, then check
        if not price > 0:
            msg.error( __name__ + ": Input cell for 'Price' is less than 0. See input row:\n" + str( input_row ), method_name )
            return False

        self.setPrice( price )
        return True


    def findCommission( self ):
        """
        Description:    
        Arguments:      
        Returns:        bool:   True for success, False for failure
        """
        method_name = self.getMethodName()

        # Gets the row date and converts it to the correct format
        input_row = self.getInputRow()
        commission = input_row[ 6 ]
        if math.isnan( commission ):
            self.setCommission( self.mNa )
            return True

        # Force into an int, then check
        if not commission >= 0:
            msg.error( __name__ + ": Input cell for 'Commision' is less than 0. See input row:\n" + str( input_row ), method_name )
            return False

        self.setCommission( commission )
        return True


    def findTicker( self ):
        # TODO: Finish this function
        """
        Description:    
        Arguments:      
        Returns:        bool:   True for success, False for failure
        """
        method_name = self.getMethodName()

        # Gets the input row and description cell
        input_row = self.getInputRow()

        passed, description_cell = self.getDescriptionCell()
        if not passed:
            msg.Error( "Couldn't find a description cell in the input.", method_name )
            return False

        ticker_cell = str( input_row[ 4 ] )
        symbol_list = ticker_cell.split()
        if symbol_list[0] != "":
            msg.system( "found ticker: " + str( symbol_list[0] ), method_name )
            self.setTicker( symbol_list[ 0 ] )
            return True

        return True



    def findDateOfAction( self ):
        """
        Description:    Finds the date of action in the input row, then sets the member. Currently acts as a wrapper to
                        formatDate, but it might change so should be left as is.
        Arguments:      date [ string ]:    Optional. Only used if user wants to override this date.
        Returns:        bool:   True for success, False for failure
        """
        method_name = self.getMethodName()

        # Gets the row date and converts it to the correct format
        input_row = self.getInputRow()
        passed, action_date = self.formatDate( input_row[ 0 ] )
        if not passed:
            msg.error( "Couldn't set 'Date of Action'.", method_name )
            return False

        self.setActionDate( action_date )
        return True


    def findDateOfExpiration( self ):
        """
        Description:    Finds the date of expiration in the input row, then sets the member.
        Arguments:      date [ string ]:    Optional. Only used if user wants to override this date.
        Returns:        bool:   True for success, False for failure
        """
        method_name = self.getMethodName()

        if self.getType() not in self.mOptionTypesActive:
            self.setExpDate( self.mNa )
            return True

        # Gets the description cell
        passed, description_cell = self.getDescriptionCell()
        if not passed:
            msg.system( "Couldn't find a description cell in the input.", method_name )
            return False

        # If it's in the list, return the index of the month that's found
        description_list = description_cell.split()
        index = -1
        for month in self.mMonths:
            try:
                index = description_list.index( month[0] )
                break
            except ValueError:
                pass

        # Builds the expiration date if the index is okay
        if index == -1:
            msg.error( "Expiration date not found in '" + str( description_list ) + "'.", method_name )
            return False
        else:
            if index + 2 >= len( description_list ):
                msg.error( "Description cell has issues. No more agruments after the found month '" + description_list[ index ] + "'. See description list:\n" + str( description_list ), method_name )
                return False

            exp_date = description_list[ index ] + " " + description_list[ index + 1 ] + " " + description_list[ index + 2 ]
            passed, exp_date = self.formatDate( exp_date )
            if not passed:
                msg.error("Issue formatting Expiration date: '" + exp_date, method_name )
                return False

            self.setExpDate( exp_date )
        # TODO: Need a case for "assigned" and "expired"
        return True


    def formatDate( self, pDate ):
        """
        Description:    Takes an input date and formats it to an expected form
        Arguments:      pDate [ string ]:   Date to be formatted
        Returns:        bool:   True for success, False for failure
                        string: The input date but in the correct format
        """
        method_name = self.getMethodName()

        # Checks format is ##/##/##
        # Regex: '[0-9]' is any digit. '$' signifies end of the line. '^' signifies start of the line.
        if re.match( r"^[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]$", pDate ):
            return True, pDate

        # If not in '##/##/####' but has two '/', fail the check
        date_list = pDate.split()
        if len( date_list ) != 3:
            msg.error( "Format of input date should be '##/##/####' or 'ABC DD YYYY'", method_name )
            return False, pDate

        month = date_list[0]
        day = date_list[1]
        year = date_list[2]

        try:
            day = int( day )
        except ValueError:
            msg.error( "Day has to be a number. Input day is: '" + str( day ) + "'", method_name )
            return False, pDate

        try:
            year = int( year )
        except ValueError:
            msg.error( "Year has to be a number. Input year is: '" + str( year ) + "'", method_name )
            return False, pDate

        if day < 1 or day > 31:
            msg.error( "Day has to be between 31 and 1. Input day is: '" + str( year ) + "'", method_name )
            return False, pDate

        elif year < 2000 or year > 2100:
            msg.error( "Year has to be between 2100 and 2000. Input year is: '" + str( year ) + "'", method_name )
            return False, pDate

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
            msg.error( "date_list[0] not expected: " + month, method_name )
            return False, pDate


        # Formats days with leading 0
        day = str( day )
        year = str( year )
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
        method_name = self.getMethodName()

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
            msg.error( "Couldn't find 'DESCRIPTION' in TdHeader.", method_name )
            return False, "ERROR"

        # Position returned is greater than rows from intput
        input_row = self.getInputRow()
        if position > len( input_row ) - 1:
            msg.error( "Description cell found at position '" + str( position ) + "', but last position of input row is '" + str( len( input_row ) - 1 ) + "'.", method_name )
            return False, "ERROR"

        description_cell = input_row[ position ]

        return True, description_cell


    def getMethodName( self, class_name=__name__ ):
        """
        Description:    
        Arguments:      
        Returns:        
        """
        name = class_name
        name += "." + sys._getframe(1).f_code.co_name
        return name


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

    def getPrice( self ):
        return self._mPrice

    def setPrice( self, value ):
        self._mPrice = value
        return

    def getCommission( self ):
        return self._mCommission

    def setCommission( self, value ):
        self._mCommission = value
        return

    def getAmount( self ):
        return self._mAmount

    def setAmount( self, value ):
        self._mAmount= value
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



