
# Modules
import re
import sys
import math

# Project Modules
from phootlogger import logger
msg = logger.messages( __name__ )

class csvFilter:


    def __init__( self ):

        self.mPlaceHolder = "*** ERROR ***"
        self.mNa = "-"

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
        # TODO: Connect strings to enums...? Somehow change the hardcoded numbers to associate with strings
        self.mOtherTypes = [ "CASH ALTERNATIVES INTEREST",
                             "CASH ALTERNATIVES PURCHASE",
                             "CASH ALTERNATIVES REDEMPTION",
                             "CASH MOVEMENT OF INCOMING ACCOUNT TRANSFER",
                             "CLIENT REQUESTED ELECTRONIC FUNDING DISBURSEMENT",
                             "CLIENT REQUESTED ELECTRONIC FUNDING RECEIPT",
                             "FREE BALANCE INTEREST ADJUSTMENT",
                             "MANDATORY - EXCHANGE",
                             "MANDATORY REORGANIZATION FEE",
                             "MANDATORY REVERSE SPLIT",
                             "MARGIN INTEREST ADJUSTMENT",
                             "MISCELLANEOUS JOURNAL ENTRY",
                             "OFF-CYCLE INTEREST",
                             "TRANSFER OF SECURITY OR OPTION IN" ]
        self.mStockTypes = [ "QUALIFIED DIVIDEND",
                             "ORDINARY DIVIDEND" ]

        self._mInputRow = []
        self.mOutputRow = []
        for curr in self.mOutputHeaders:
            self.mOutputRow.append( self.mPlaceHolder )

        # Sets each value to default, then is put into the output row
        self.setActionDate( self.mPlaceHolder )
        self.setTicker( self.mPlaceHolder )
        self.setType( self.mPlaceHolder )
        self.setAction( self.mPlaceHolder )
        self.setQuantity( self.mPlaceHolder )
        self.setPrice( self.mPlaceHolder )
        self.setCommission( self.mPlaceHolder )
        self.setAmount( self.mPlaceHolder )
        # Option specific
        self.setExpDate( self.mPlaceHolder )
        self.setStrike( self.mPlaceHolder )

        # Sets output row to default values
        self.setOutputRow()

        # Checks the row was set correctly
        if len( self.mOutputRow ) is not len( self.mOutputHeaders ):
            msg.error( "DEVELOPER: Issue using csvFilter::__init__(). OutputRow cell count is not equal to OutputHeaders cell count" )
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

        # Sets input row for the object to use. pRow is
        self.setInputRow( pRow )


        # Sets the Price of the transaction ( Stock price, cost / value of option )
        passed = self.findPrice()
        if not passed:
            msg.error( "Couldn't find 'Price'." )
            return False

        # Sets the Commission cost of the transaction
        passed = self.findCommission()
        if not passed:
            msg.error( "Couldn't find 'Commission'." )
            return False

        passed = self.findAmount()
        if not passed:
            msg.error( "Couldn't find 'Amount'." )
            return False

        # Sets the date of the Transaction
        passed = self.findDateOfAction()
        if not passed:
            msg.error( "Couldn't find 'Date of Action'." )
            return False

        # Sets the type of transaction
        passed = self.findType()
        if not passed:
            msg.error( "Couldn't find 'Type'." )
            return False

        # Makes sure the type is set. After this point, filters depend on this.
        if self.getType() == self.mPlaceHolder:
            msg.error( "Cell type needs to be set before proceeding past this point." )
            return False

        # Sets the Quantity of the transaction
        passed = self.findQuantity()
        if not passed:
            msg.error( "Couldn't find 'Quantity'." )
            return False

        passed = self.findStike()
        if not passed:
            msg.error( "Couldn't find 'Amount'." )
            return False

        # Sets the Action of the transaction
        passed = self.findAction()
        if not passed:
            msg.error( "Couldn't find 'Action'" )
            return False

        # Only finds Expiration date if an option
        passed = self.findDateOfExpiration()
        if not passed:
            msg.error( "Couldn't find 'Date of Expiration'." )
            return False

        passed = self.findTicker()
        if not passed:
            msg.error( "Couldn't find 'Ticker'." )
            return False


        # Sets the output row
        self.setOutputRow()
        if not passed:
            msg.error( "Couldn't find 'Output Row.'" )
            return False

        # Checks the output row
        # for curr in range( len( self.mOutputRow ) ):
        #     if self.mOutputRow[ curr ] == self.mPlaceHolder:
        #         msg.system( "NOTE: '" + self.mOutputHeaders[ curr ] + "' isn't set. Current value is: " + self.mOutputRow[ curr ] )

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
            msg.error( "Couldn't find a description cell in the input." )
            return False

        # TODO: FIX THIS!
        # 02-23-2024: TD has updated one of the assignment cells to now include 'call' / 'put' so the assignment needs
        #             to be first or the put / call will be declared it's type. script will call out false if
        # Returns type if 'put' or 'call'
        for curr in self.mOptionTypesActive:
            if curr in description_cell:

                passive = False
                for item in self.mOptionTypesPassive:
                    if item in description_cell:
                        passive = True

                if not passive:
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

        msg.error( "Issue setting type. Wasn't '" + str( self.mOptionTypesActive ) + ", 'Option', 'Stock', or 'Other'. See description cell:\n" + str( description_cell ) )
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
            msg.error( "Couldn't find a description cell in the input." )
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
        if self.mOtherTypes[ 0 ] in description_cell:   # CASH ALTERNATIVES INTEREST
            self.setAction( "Cash Alternatives Interestt" )
            return True
        elif self.mOtherTypes[ 1 ] in description_cell:   # CASH ALTERNATIVES PURCHASE
            self.setAction( "Cash Alternatives Purchase" )
            return True
        elif self.mOtherTypes[ 2 ] in description_cell:  # CASH ALTERNATIVES REDEMPTION
            self.setAction( "Cash Alternatives Redemption" )
            return True
        elif self.mOtherTypes[ 3 ] in description_cell:  # CASH MOVE OF INCOMING TRANSFER
            self.setAction( "Cash Move of Incoming Transfer" )
            return True
        elif self.mOtherTypes[ 4 ] in description_cell: # CLIENT REQUESTED ELECTRONIC FUNDING DISBURSEMENT
            self.setAction( "Funding Disbursement" )
            return True
        elif self.mOtherTypes[ 5 ] in description_cell: # CLIENT REQUESTED ELECTRONIC FUNDING RECEIPT
            self.setAction( "Funding Transfer" )
            return True
        elif self.mOtherTypes[ 6 ] in description_cell: # FREE BALANCE INTEREST ADJUSTMENT
            self.setAction( "Interest Adjustment: Free Balance" )
            return True
        elif self.mOtherTypes[ 7 ] in description_cell: # MANDATORY EXCHANGE
            self.setAction( "Mandatory - Exchange" )
            return True
        elif self.mOtherTypes[ 8 ] in description_cell: # MANDATORY REORGANIZATION FEE
            self.setAction( "Mandatory Reorganization Fee" )
            return True
        elif self.mOtherTypes[ 9 ] in description_cell: # MANDATORY REVERSE SPLIT
            self.setAction( "Mandatory Reverse Split" )
            return True
        elif self.mOtherTypes[ 10 ] in description_cell: # MARGIN INTEREST ADJUSTMENT
            self.setAction( "Interest Adjustment: Margin" )
            return True
        elif self.mOtherTypes[ 11 ] in description_cell: # MISCELLANEOUS JOURNAL ENTRY
            self.setAction( "Miscellaneous Journal Entry" )
            return True
        elif self.mOtherTypes[ 12 ] in description_cell: # OFF-CYCLE INTEREST
            self.setAction( "Off-cycle Interest" )
            return True
        elif self.mOtherTypes[ 13 ] in description_cell: # TRANSFER OF SECURITY OR OPTION IN
            self.setAction( "Transfer of Security / Option" )
            return True

        # TODO: Don't hard code this 'other' portion. Fix it in the type too.
        if self.getType() == "Other":
            self.setAction( self.mNa )
            return True

        # Sets dividend
        for curr in self.mStockTypes:
            if curr in description_cell:
                self.setAction( "Dividend" )
                return True

        msg.error( "Couldn't find any of the following actions in the description cell '" + description_cell + "'\n" + str( action_types ) + "\n" + str( self.mOtherTypes ) + "\n" + str( self.mStockTypes ) )
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
        quantity = input_row[3]
        if math.isnan( quantity ):
            self.setQuantity( self.mNa )
            return True

        # Force into an float or int, then check
        if not quantity.is_integer():
            quantity = float( quantity )
        else:
            quantity = int( quantity )

        if not quantity > 0:
            msg.error( __name__ + ": Input cell for 'Quantity' is less than 0. See input row:\n" + str( input_row ) )
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
            msg.error( __name__ + ": Input cell for 'Price' is less than 0. See input row:\n" + str( input_row ) )
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
            msg.error( __name__ + ": Input cell for 'Commision' is less than 0. See input row:\n" + str( input_row ) )
            return False

        # makeing Integers look nice
        if commission.is_integer():
            commission = int( commission )

        self.setCommission( commission )
        return True


    def findStike( self ):
        # TODO: Finish this function
        """
        Description:    
        Arguments:      
        Returns:        bool:   True for success, False for failure
        """
        method_name = self.getMethodName()

        if self.getType() not in self.mOptionTypesActive:
            self.setStrike( self.mNa )
            return True

        # Gets the row date and converts it to the correct format
        input_row = self.getInputRow()
        strike_cell = str( input_row[ 4 ] )
        strike = strike_cell.split()
        strike = strike[ 4 ]

        # TODO: Seems to be setting a strike, then continuing to set value until the a ne call / put comes along
        # TODO: Top right value is still a place holder. Doesn't seem to change
        self.setStrike( strike )
        return True


    def findAmount( self ):
        # TODO: Finish this function
        """
        Description:    
        Arguments:      
        Returns:        bool:   True for success, False for failure
        """
        method_name = self.getMethodName()

        # Gets the row date and converts it to the correct format
        input_row = self.getInputRow()
        amount = input_row[ 7 ]
        if math.isnan( amount ) or amount == 0:
            self.setAmount( self.mNa )
            return True

        self.setAmount( amount )
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
            msg.error( "Couldn't find a description cell in the input." )
            return False

        # Uses the first item in the list to get the ticker
        ticker_cell = str( input_row[ 4 ] )
        symbol_list = ticker_cell.split()
        first_symbol = str( symbol_list[ 0 ] )

        # If it's not an option / stock AND not in symbol column, set to 'NA'
        ticker_type = [ "Option", "Stock" ]
        for curr in self.mOptionTypesActive:
            ticker_type.append( str( curr ) )

        if self.getType() not in ticker_type:
            # When the cell is blank, the string appears as "nan"
            if first_symbol != "nan":
                self.setTicker( first_symbol )
                return True
            else:
                self.setTicker( self.mNa )
                return True

        if self.getType() not in self.mOptionTypesPassive and\
            self.getType() not in "Options":
            self.setTicker( first_symbol )
            return True


        # Special for Assignment / Expiration. Two possible types:
        #       Entry:  (0MVIS.AAAAAAAAAA)
        #       Regex:  .*(0<WE WANT THIS>\..*)
        #
        #       Entry: (TSLA Feb 2 2024 205.0 Put) 
        #       Regex:  .*(<WANT-THIS> .*)

        # Replaces the text before the ticker
        ticker_cell = description_cell
        ticker = ticker_cell
        if re.search( '^.*\(0.*\..*\)$', ticker_cell ):
            # Matched with first regex
            ticker = re.sub( '^.*\(0', '', ticker_cell )
            if ticker == ticker_cell:
                msg.error( "Couldn't replace the text before the ticker with regex.\n"\
                            "ticker_cell:      '" + str( ticker_cell ) + "'\n"\
                            "description_cell: '" + description_cell + "'" )
                return False

            # Replaces the text after the ticker
            ticker_cell = ticker
            ticker = re.sub('\..*\)$', '', ticker_cell )
            if ticker == ticker_cell:
                msg.error( "Couldn't replace the text after the ticker with regex.\n"\
                            "ticker_cell:      '" + str( ticker_cell ) + "'\n"\
                            "description_cell: '" + description_cell + "'" )
                return False

        elif re.search( '^.*\(.* .*\)$', ticker_cell ):
            # Matched with second regex
            ticker = re.sub( '^.*\(', '', ticker_cell )
            if ticker == ticker_cell:
                msg.error( "Couldn't replace the text before the ticker with regex.\n"\
                            "ticker_cell:      '" + str( ticker_cell ) + "'\n"\
                            "description_cell: '" + description_cell + "'" )
                return False

            # Replaces the text after the ticker
            ticker_cell = ticker
            ticker = re.sub(' .*\)$', '', ticker_cell )
            if ticker == ticker_cell:
                msg.error( "Couldn't replace the text after the ticker with regex.\n"\
                            "ticker_cell:      '" + str( ticker_cell ) + "'\n"\
                            "description_cell: '" + description_cell + "'" )
                return False
        else:
            msg.error( "No regex pattern found..\n"\
                        "ticker_cell:      '" + str( ticker_cell ) + "'\n"\
                        "description_cell: '" + description_cell + "'" )
            return False


        # Sets the remaining text
        self.setTicker( ticker )
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
            msg.error( "Couldn't set 'Date of Action'." )
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
            msg.system( "Couldn't find a description cell in the input." )
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
            msg.error( "Expiration date not found in '" + str( description_list ) + "'." )
            return False
        else:
            if index + 2 >= len( description_list ):
                msg.error( "Description cell has issues. No more agruments after the found month '" + description_list[ index ] + "'. See description list:\n" + str( description_list ) )
                return False

            exp_date = description_list[ index ] + " " + description_list[ index + 1 ] + " " + description_list[ index + 2 ]
            passed, exp_date = self.formatDate( exp_date )
            if not passed:
                msg.error("Issue formatting Expiration date: '" + exp_date )
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

        # Checks format is ##/##/#### and switches to YYYY/MM/DD
        # Regex: '[0-9]' is any digit. '$' signifies end of the line. '^' signifies start of the line.
        if re.match( r"^[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]$", pDate ):
            # Changes the order to YYYY + / + MM + / + DD
            tmp = pDate
            pDate = tmp[6:] + "/" + tmp[:2] + "/" + tmp[3:5]
            return True, pDate

        # If not in '##/##/####' but has two '/', fail the check
        date_list = pDate.split()
        if len( date_list ) != 3:
            msg.error( "Format of input date should be '##/##/####' or 'ABC DD YYYY'" )
            return False, pDate

        month = date_list[0]
        day = date_list[1]
        year = date_list[2]

        try:
            day = int( day )
        except ValueError:
            msg.error( "Day has to be a number. Input day is: '" + str( day ) + "'" )
            return False, pDate

        try:
            year = int( year )
        except ValueError:
            msg.error( "Year has to be a number. Input year is: '" + str( year ) + "'" )
            return False, pDate

        if day < 1 or day > 31:
            msg.error( "Day has to be between 31 and 1. Input day is: '" + str( year ) + "'" )
            return False, pDate

        elif year < 2000 or year > 2100:
            msg.error( "Year has to be between 2100 and 2000. Input year is: '" + str( year ) + "'" )
            return False, pDate

        # Assign number for month
        if month == 'Jan':
            month = '01'
        elif month == 'Feb':
            month = '02'
        elif month == 'Mar':
            month = '03'
        elif month == 'Apr':
            month = '04'
        elif month == 'May':
            month = '05'
        elif month == 'Jun':
            month = '06'
        elif month == 'Jul':
            month = '07'
        elif month == 'Aug':
            month = '08'
        elif month == 'Sep':
            month = '09'
        elif month == 'Oct':
            month = '10'
        elif month == 'Nov':
            month = '11'
        elif month == 'Dec':
            month = '12'
        else:
            msg.error( "date_list[0] not expected: " + month )
            return False, pDate

        # Formats days with leading 0
        day = str( day )
        year = str( year )
        if len(day) < 2:
            day = int(day)
            day = str(day).zfill(2)

        # Finalize date format
        new_date = year + '/' + month + '/' + day

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
            msg.error( "Couldn't find 'DESCRIPTION' in TdHeader." )
            return False, "ERROR"

        # Position returned is greater than rows from intput
        input_row = self.getInputRow()
        if position > len( input_row ) - 1:
            msg.error( "Description cell found at position '" + str( position ) + "', but last position of input row is '" + str( len( input_row ) - 1 ) + "'." )
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



