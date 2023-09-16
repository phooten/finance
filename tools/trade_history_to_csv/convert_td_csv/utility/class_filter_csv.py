
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

    def makeRow( pExpDate="NAN", pType="NAN", pAction="NAN", pTicker="NAN", pStrike="NAN", pAmount="NAN", pPrice="NAN", pCommission="NAN" ): #, pDividend="NAN" ):
        """
        Description:    
        Arguments:      
        Returns:        
        """
        # Variables
        row = []

        # Makes List
        row.append( pExpDate )
        row.append( pType )
        row.append( pAction )
        row.append( pTicker )
        row.append( pStrike )
        row.append( pAmount )
        row.append( pPrice )
        row.append( pCommission )
        # row.append( pDividend )

        if len(row) is not len(output_headers):
            msg.error( "DEVELOPER: Issue using csvFilter::makeRow()", "TODO")
            msg.quit_script()

        return row

    def filterDescriptionColumn( pColLen, pCell, pRow ):
        """
        Description:    
        Arguments:      
        Returns:        
        """
        # Variables: General
        f_row = []
        row_str = pCell.split()

        # Variable: Filters 
        f_assignment = 'REMOVAL OF OPTION DUE TO ASSIGNMENT'
        f_expiration = 'REMOVAL OF OPTION DUE TO EXPIRATION'
        f_exchange = 'MANDATORY - EXCHANGE'
        f_balance = 'FREE BALANCE INTEREST ADJUSTMENT'
        f_funding = 'CLIENT REQUESTED ELECTRONIC FUNDING RECEIPT'
        f_margin = 'MARGIN INTEREST ADJUSTMENT'
        f_div = 'QUALIFIED DIVIDEND'
        f_bought = 'Bought'
        f_sold = 'Sold'
        f_call = 'Call'
        f_put = 'Put'
        f_list_option = [ f_call, f_put ]
        f_list_stock = [ f_sold, f_bought ]
        f_list_ticker = [ f_sold, f_bought ]


        # Filters out 'removal due to expiration'
        if f_expiration in pCell:
            description = pCell.split()

            # Selections portion of list with ticker in it
            description = description[ 6 ]

            # Selects text surrounding ticker
            start_text = "(0"
            end_text = "."

            # Locations surrounding ticker
            start_loc = description.find( start_text ) + len( start_text )
            end_loc = description.find( end_text )

            # Finds ticker
            ticker = description[ start_loc:end_loc ]
            price = NaN     # Expired worthless, so no need to track cost
            commission = 0  # Expiration has no cost, no comission

            f_row = makeRow( NaN, "Expiration", NaN, ticker, NaN, NaN, price, commission )
            # f_row = []  # TODO: Pretty sure we don't need anything from here, but just in case I'll leave it

        # Filters out 'removal due to assignment'
        elif f_assignment in pCell:
            pass
            # IGNORING:
            # This was taken place in a seperate option transaction:
            # TODO:
            #   Coordinate these cases with the stock buys / sells
            # ----------------------------------------------------------------------
            # # SPECIAL CASE:
            # # 03/16/2022,41381062742,REMOVAL OF OPTION DUE TO ASSIGNMENT (RBLX Mar 18 2022 80.0 Put),1,RBLX Mar 18 2022 80.0 Put,,,0.00,,,,

            # # NORMAL CASE:
            # description = pCell.split()
            # description = description[ 6 ]

            # start_text = "(0"
            # end_text = "."
            # start_loc = description.find( start_text ) + len( start_text )
            # end_loc = description.find( end_text )
            # substring = description[ start_loc:end_loc ]

            # ticker = "NOT DONE"
            # price = 0       # Assigned, so no need to track cost
            # commission = 0  # Assigned so has no cost, no comission

            # f_row = makeRow( NaN, "Assignment", NaN, ticker, NaN, NaN, price, commission )
            # ----------------------------------------------------------------------

        # Filters out 'balance adjustments'
        elif any( x in pCell for x in ( f_balance, f_margin ) ):
            # f_row = makeRow()
            f_row = []

        # Filters out 'all options'
        elif any( x in pCell for x in f_list_option ):
            # Saving values
            action = row_str[ 0 ]
            amount = row_str[ 1 ]  
            ticker = row_str[ 2 ]
            exp_date = row_str[ 3 ] + ' ' + row_str[ 4 ] + ' ' + row_str[ 5 ]
            strike = row_str[ 6 ]
            opt_type = row_str[ 7 ]
            # row_str[ 8 ] is not important
            price = row_str[ 9 ]
            commission = pRow[ 6 ]

            # Convert date to MM/DD/YYY
            converted_exp_date = dateFormatConversion( exp_date )

            # Creating a new row
            f_row = makeRow( converted_exp_date, opt_type, action, ticker, strike, amount, price, commission )

        # Filters out 'Manditory Exchange'
        elif f_exchange in pCell:
            # f_row = makeRow()
            f_row = []

        # Filters out 'any stock buy/sell' 
        elif any( x in row_str[ 0 ] for x in f_list_stock ):
            # TODO: New case for stocks bought not in groups of 100, i.e. BMBL from
            action = row_str[ 0 ]
            amount = row_str[ 1 ]  
            ticker = row_str[ 2 ]
            # row_str[3] = '@'
            price = row_str[ 4 ]

            f_row = makeRow( NaN, "Stock", action, ticker, NaN, amount, price)

        # Filters out funding receipts 
        # TODO: Double check this works
        elif f_funding in pCell:
            f_row = makeRow( NaN, "Funding", NaN, NaN, NaN, NaN, pRow[ 7 ])

        # Filters out dividends
        # elif f_div in pCell:
        #     f_row = makeRow( NaN, "Dividend", NaN, NaN, NaN, NaN, NaN, NaN )

        # Error if anything else
        else:
            print( global_error + "Nothing found. Issue in this cell: '" + pCell + "'")
            f_row = []

        return f_row


    def dateFormatConversion( pDate ):
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

