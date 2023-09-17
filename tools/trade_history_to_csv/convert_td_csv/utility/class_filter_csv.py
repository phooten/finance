
# Modules
#   NA

# Project Modules
from messages import class_messages

msg = class_messages.messages()

class csvFilter:
   def __init__(self, x, y):

        # TD Ameritrade Column Names
        self.td_headers = [
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
        self.output_headers = [
                'DATE OF ACTION',
                'DATE OF EXPIRATION',
                'TYPE',
                'ACTION',
                'TICKER',
                'STRIKE PRICE',
                'AMOUNT',
                'COST',
                'TOTAL COMMISION',
                'DIVIDEND',
                'ORIGINAL ROW',
                'ASSIGNMENT' ]

        self.output_row = []


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

    def filterDescriptionColumn( self, pRow ):
        """
        Description:    
        Arguments:      
        Returns:        
        """

        col_desc = self.td_headers[ 2 ]
        print( "Target Cell: '" + str( pRow[ col_desc ] ) + "'" )

        filterForOptions()


        return self.output_row


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
            msg.error( "date_list[0] not expected: " + month)
            msg.quit_script()

        # Formats days with leading 0
        if len(day) < 2:
            day = int(day)
            day = str(day).zfill(2)

        # Finalize date format
        date += '/' + day + '/' + year

        return date


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
