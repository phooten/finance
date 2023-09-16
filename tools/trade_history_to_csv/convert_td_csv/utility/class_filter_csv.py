
# Modules
#   NA

# Project Modules
from messages import class_messages

msg = class_messages.messages()

class csvFilter:
    # TD Ameritrade Column Names
    td_headers = [  'DATE',
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

    # Headers for the new output csv                  EXAMPLE FORMAT    IF APPLICABLE       DESCRITPION
    output_headers = [  'DATE OF ACTION',           # DD-MM-YYYY
                        'DATE OF EXPIRATION',       # DD-MM-YYYY        ( Options / NA )
                        'TYPE',                     # Option / Stock / Other
                        'ACTION',                   # Buy / Sell / Assignment / Expiration / Other
                        'TICKER',                   # ZZZZ
                        'STRIKE PRICE',             # XX.XX             ( Options / NA )
                        'AMOUNT',                   # ##                                    Number of ( Shares / Options / NA )
                        'COST',
                        'TOTAL COMMISION',          # Commision ( 0.65 cents * Num of Trades )
                        'DIVIDEND',                 # ( True / False / NA ) ( Stocks )
                        'ORIGINAL ROW',
                        'ASSIGNMENT'                # ( True / False / NA ) ( Options )
                        ]

    output_row = []


    # public
    def makeRow( self, pExpDate="NAN", pType="NAN", pAction="NAN", pTicker="NAN", pStrike="NAN", pAmount="NAN", pPrice="NAN", pCommission="NAN" ): #, pDividend="NAN" ):
        """
        Description:    
        Arguments:      
        Returns:        
        """

        # Makes List
        output_row.append( pExpDate )
        output_row.append( pType )
        output_row.append( pAction )
        output_row.append( pTicker )
        output_row.append( pStrike )
        output_row.append( pAmount )
        output_row.append( pPrice )
        output_row.append( pCommission )
        # row.append( pDividend )

        if len( output_row ) is not len( output_headers ):
            msg.error( "DEVELOPER: Issue using csvFilter::makeRow()", "TODO")
            msg.quit_script()

        return row

    def filterDescriptionColumn( self, pColDescription, pRow ):
        """
        Description:    
        Arguments:      
        Returns:        
        """
        # TODO: FINISH This function
        # print( "description: " + pColDescription + "    row: " + str( pRow ) )

        return output_row


    def dateFormatConversion( self, pDate ):
        """
        Description:    
        Arguments:      
        Returns:        
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
            date = '01'
        elif month == 'Feb':
            date = '02'
        elif month == 'Mar':
            date = '03'
        elif month == 'Apr':
            date = '04'
        elif month == 'May':
            date = '05'
        elif month == 'Jun':
            date = '06'
        elif month == 'Jul':
            date = '07'
        elif month == 'Aug':
            date = '08'
        elif month == 'Sep':
            date = '09'
        elif month == 'Oct':
            date = '10'
        elif month == 'Nov':
            date = '11'
        elif month == 'Dec':
            date = '12'
        else:
            print( global_error + "date_list[0] not expected: " + month)

        # Formats days with leading 0
        if len(day) < 2:
            day = int(day)
            day = str(day).zfill(2)

        # Finalize date format
        date += '/' + day + '/' + year

        return date

