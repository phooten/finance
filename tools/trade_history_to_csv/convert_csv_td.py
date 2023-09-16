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

    # This needs to corrolate with                                                                                                                                                                                        
    def makeRow( pExpDate="NAN", pType="NAN", pAction="NAN", pTicker="NAN", pStrike="NAN", pAmount="NAN", pPrice="NAN", pCommission="NAN" ): #, pDividend="NAN" ):
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
            print( "DEVELOPER: Issue using csvFilter::makeRow()" )
            exit(1)

        return row


def initialCsvFileCheck( csv_path ):
    """
    Description:    
    Arguments:      
    Returns:        
    """

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
    if col_count != len( csvFilter().td_headers ):
        msgPrint( "File has [" + str(col_count) + "] headers but expects [" + str( len( csvFilter().td_headers ) ) + "].", "error", "TODO" )
        return False

    # Checks the names of the headers in Csv
    for name in column_names:
        if name not in csvFilter().td_headers:
            msgPrint( "Header [" + name + "] is not in td_headers:\n" + str(csvFilter().td_headers), "error", "TODO" )
            return False

    return True

def transferCsvContents( input_csv, output_csv ):
    """
    Description:    
    Arguments:      
    Returns:        

    """

    # Gets characteristics of CSV 
    df = pd.read_csv( input_csv, sep=',' )
    row_count, col_count = df.shape
    column_names = list(df.columns)

    new_csv = pd.DataFrame( columns=csvFilter().output_headers )

    # Outputs the dataframe into a csv
    new_csv.to_csv( output_csv, index=False )



    # TODO: Compare this to "index = False"
    new_csv.to_csv( str(output_csv + ".tmp" ) )


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
    csv_input_path = '../../sensitive_files/transactions_2022.csv'
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

    csv_output_path =  'output.csv'
    passed = transferCsvContents( csv_input_path, csv_output_path )
    if not passed:
        msgPrint( "Exiting script.", sys, "TODO" )
        exit(1)

    exit(1)




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
