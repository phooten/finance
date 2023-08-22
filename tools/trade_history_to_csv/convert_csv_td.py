#!/bin/

# Overview:
#   Goals of this script:
#       - convert the .csv of option trades from TD trade history to readable format
#       - show data in some sort of QT format. Maybe display the data and allow user customization?
#
#

# Outline / Plan:
#   - take in newest input file, OR argument file
#   - ensure argument exists if applicable
#   - filter through excel, and append to a new file
#   - 

# Concerns Important note:
#   - This script is written with the assumption that only single legs are being
#     performed. It's already getting complicated / tedious dealing with just this. 
#     Not sure what it would look like trying to connect which options were performed
#     together. Maybe utilizing the same date would be benefitial? but what if I 
#     made two or more scalps on the same day with the same tickers? 

# Libraries
import csv
import os
import pandas as pd
import sys

# TODO: Make a library for personal use
# Global Variables
global_error = "ERROR: "
NaN = "NaN"
global_commission = 0.65

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
        print( global_error + "Nothing found." + " " + pCell)
        f_row = []

    return f_row


# Main:
def main():
    # TODO: find the newest file by default
    # TODO: make this runable from anywhere

    # Variables: CSV files
    io_path = "../io/"
    # csv_input_name = 'transactions.csv'

    # TODO: 2021 has alot of specifics in it
    csv_input_name = 'transactions'
    csv_year = 2022
    csv_year_str = str( csv_year )
    csv_extra = ".csv"
    csv_input_name += "_" + csv_year_str + csv_extra
    csv_input_path = io_path + 'input/' + csv_input_name # input/transactions_20xx.csv

    csv_input_path = '../io/input/' + csv_input_name
    csv_output_name = 'output.csv'
    csv_output_path = io_path + 'output/' + csv_output_name


    # Checking first argument of python script
    if len( sys.argv ) == 2:
        if ".csv" not in sus.argv[1]:
            print( global_error + "first argument is not .csv" )
            return -1
        else:
            csv_input_path = sys.argv[1]
    

    # Column Names
    col_price = 'PRICE'
    col_desc = 'DESCRIPTION'
    col_date = 'DATE'
    col_qaun = 'QUANTITY'
    col_tick = 'SYMBOL'
    col_num = 'NUMBER'
    col_div = 'DIVIDEND'
    col_id = 'TRANSACTION ID'


    # Characteristics of CSV 
    df = pd.read_csv( csv_input_path, sep=',' )
    len_row, len_col = df.shape
    # print( df.columns )
    # print( df.shape )
    # print( df.dtypes )
    
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
            #    TODO: Make a 'Assigment = true / false' column
    total_columns = len( header )
    base_coumns = 8
    extra_columns = len( header ) - base_coumns
    new_csv = pd.DataFrame( columns=header )


    # Filters information from the 'descripton' column in every row
    df[ col_num ] = 0
    refined_csv_row = 0
    for row in range( len_row ):
        if row != len_row - 1:
            tmp_row = filterDescriptionColumn( len( header ) - extra_columns, df.loc[ row, col_desc ], df.loc[ row ] )
            
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
