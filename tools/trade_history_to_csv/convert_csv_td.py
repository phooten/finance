#!/bin/

# Overview:
#   Every year, download a TD Ameritrade history of my trades. At any point,
#   download the current year to add to the list. 
#


# Libraries
import csv
import os
import pandas as pd
import sys
import inspect


# TODO: Make a library for personal use
# Global Variables
global_error = "\nERROR: \n"
NaN = "NaN"
global_commission = 0.65
DEBUG = True



# This needs to corrolate with 
def makeRow( pExpDate=NaN, pType=NaN, pAction=NaN, pTicker=NaN, pStrike=NaN, pAmount=NaN, pPrice=NaN, pCommission=NaN ): #, pDividend=NaN ):
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

    return row


# Converts 'MM DD YYYY' ( month day year ) to 'MM/DD/YYYY' 
def dateFormatConversion( pDate ):
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



def filterDescriptionColumn( pColLen, pCell, pRow ):
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


def initialCsvFileCheck( csv_path ):

    # Checks the correct extension, which should only ever be .csv
    extension = csv_path[ len(csv_path)-4: ]
    if ".csv" != extension:
        msgPrint( "File isn't .csv: '" + csv_path + "'", "error", "TODO")
        return False


    # Check the file exists
    if not os.path.isfile( csv_path ):
        msgPrint( "File doesn't exist: '" + csv_path + "'", "error", "TODO" )
        return False


    # Check the file isn't empty
    if os.stat( csv_path ).st_size == 0:
        msgPrint( "File is empty: '" + csv_path + "'", "error", "TODO" )
        return False

    return True


def contentsCsvFileCheck( csv_path ):
    """
    Description:    Checks the input CSV for basic contents to make sure it can be parsed. Includes header contents,
                    counts for columns and count for rows.
    Arguments:      String - Path to a a CSV to be parsed
    Returns:        Boolean - True for success, False for failure
    """

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


    # Gets characteristics of CSV 
    df = pd.read_csv( csv_path, sep=',' )
    row_count, col_count = df.shape
    column_names = list(df.columns)

    # Checks the amount of rows in the given csv
    row_minimum = 2             # Header doesn't count as a row
    if row_count < row_minimum:
        msgPrint( "File has [" + str(row_count) + "] rows. Need to have at least [" + str(row_minimum) + "].", "error", "TODO" )
        return False

    # Checks the amount of columns in given csv
    if col_count != len( td_headers ):
        msgPrint( "File has [" + str(col_count) + "] headers but expects [" + str( len( td_headers ) ) + "].", "error", "TODO" )
        return False

    # Checks the names of the headers in Csv
    for name in column_names:
        if name not in td_headers:
            msgPrint( "Header [" + name + "] is not in td_headers:\n" + str(td_headers), "error", "TODO" )
            return False

    # print( df.columns )
    # print( df.shape )
    # print( df.dtypes )

    return True

def transferCsvContents( input_csv, output_csv ):
    """
    Description:    
    Arguments:      
    Returns:        

    """

    return True

def msgPrint( msg, choice, func_name ):
    """
    Description:    Prints out message to the user
    Arguments:      msg     - (string) to be printed out to user
                    choice  - (string) defines which type of message is used.
                              i.e. general system, error, etc.
                    func_name - (function) function called that figures out what the 
                            name of the previous funcion is
    Returns:        Void
    """

    if choice == "error":
        print( "\n" )
        print( "--------------------" )
        print( "ERROR:" )
        print( func_name + ": " + msg )
        print( "--------------------" )

    elif choice == "sys":
        print( "\n" )
        print( func_name + ": " + msg )

    else:
        print( "\n" )
        print( "Issue using '" + __name__ + "'." )
        print( "Exiting." )
        exit(1)


def main():

    # Intial checks for the csv file
    csv_input_path = 'unittest/blank.csv'
#    csv_input_path = '../../sensitive_files/transactions_2022.csv'
    passed = initialCsvFileCheck( csv_input_path )
    if not passed:
        msgPrint( "Exiting script.", sys, "TODO" )
        exit(1)



    # TODO: Before doing anything else:
    #       2. Make sure unit tests are structed correctly
    passed = contentsCsvFileCheck( csv_input_path )
    if not passed:
        msgPrint( "Exiting script.", sys, "TODO" )
        exit(1)

    csv_output_path =  'output/output.csv'
    passed = transferCsvContents( csv_input_path, csv_output_path )
    if not passed:
        msgPrint( "Exiting script.", sys, "TODO" )
        exit(1)

    exit(1)

    # Header names of new CSV file
    # TODO: NOTE, if this changes, makeRow inside filterDescriptionColumn needs to too 
    header = [ 'DATE OF ACTION',
               'DATE OF EXPIRATION',
               'TYPE',
               'ACTION',
               'TICKER',
               'STRIKE',
               'AMOUNT',
               'COST',
               'TOTAL COMMISION',
            #    'DIVIDEND',
               'ORIGINAL ROW' ]
            #    TODO: Make a 'Assigment = true / false / NA' column
    total_columns = len( header )
    base_coumns = 8
    extra_columns = len( header ) - base_coumns
    new_csv = pd.DataFrame( columns=header )

    exit( 1 )

    # Filters information from the 'descripton' column in every row
    df[ col_num ] = 0
    refined_csv_row = 0
    for row in range( len_row ):
        if row != len_row - 1:
            tmp_row = filterDescriptionColumn( len( header ) - extra_columns, df.loc[ row, col_desc ], df.loc[ row ] )

            #if DEBUG:
            #    print( __name__ + ": tmp_row: " + tmp_row )

            if len( tmp_row ) == len( header ) - extra_columns:
                # Adding in date of action
                tmp_row.insert( 0, df.loc[ row, col_date ] )

                # Adding original row it was pulled from
                tmp_row.append( row + 2 )

                # Insert new row in DataFrame
                new_csv.loc[ refined_csv_row ] = tmp_row
                refined_csv_row += 1


    # Handle the output file
    # try:
    #     os.remove( csv_output_path )
    # except:
    #     print( "No files in this path: ", csv_output_path )
    # df.to_csv( csv_output_path )
    
    # new_csv.set_index( 'INDEX' )
    try:
        os.remove( csv_output_path )
    except:
        print( "No files in this path: ", csv_output_path )
    new_csv.to_csv( csv_output_path, index=False )




if __name__ == "__main__":
    main()
