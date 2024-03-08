
# Script will take user input and filter out certain details from the master csv trade history
# User input:
#   - Stock
#       * Will be hard coded at first. Eventually would like a GUI menu for this where a drop down list
#         or input from user. The script will check that this is valid in the list of known stocks
#   - Date:
#       * Enter a start / stop date. Checks that there is at least one date within the range.
#         if not, show an error
#   - Type:
#       * Options:
#           Will be put and call combinations
#       * Put / Call:
#           Not in use.
#       * Stock:
#           Not in use.
#       * Combination:
#           Not in use.

import os
from datetime import datetime
import pandas as pd
import argparse
import time

# Input Object
class UserInput():
    """
    !@brief Creates a new object that stores user input

    @param mDateRange - 
    @param mType - 
    """
    def __init__( self ):
        self.mTickerList = [ ]  # Blank List
        self.mDateRange = [ "01/01/2000", "01/01/2100" ]
        self.mType = [ ] # Blank List
        self.mOffset = 0.0
        self.mMacro = ""
# End of UserInput


"""
GetUserInput

!@brief Gets input from the user about how to sort out entries in the csv file

@returns - Object that stores user selections
"""
def GetUserInput( arguments, dataframe ):
    # Default input object selection
    UserInputObj = UserInput()

    # TODO: format needs to be converted into the csv date format
    # TODO: Don't like this hardcoded
    # Setting date range
    UserInputObj.mDateRange[ 0 ] = str( datetime.strptime( arguments.start_date, "%Y-%m-%d" ).strftime('%Y/%m/%d') )
    UserInputObj.mDateRange[ 1 ] = str( datetime.strptime( arguments.end_date, "%Y-%m-%d" ).strftime('%Y/%m/%d') )

    # Setting type to sort by
    UserInputObj.mType = arguments.sort_type

    # Setting ticker list
    UserInputObj.mTickerList = list( arguments.ticker_list.split( " " ) )
    if "All" == UserInputObj.mTickerList[0]:
        # Gets all tickers regaurdless of date selections
        # Remove any tickers with symbols in it
        UserInputObj.mTickerList = [ item for item in dataframe['TICKER'].unique() if not '-' in item ]

    # Setting Offset
    UserInputObj.mOffset = float( arguments.offset )

    # Setting Offset
    UserInputObj.mMacro = arguments.macro

    print( "Widget Input Details:")
    print( "_________________________________" )
    print( "Start Date:  " + str( UserInputObj.mDateRange[ 0 ] ) )
    print( "End Date:    " + str( UserInputObj.mDateRange[ 1 ] ) )
    print( "Ticker List: " + str( UserInputObj.mTickerList ) )
    print( "Type:        " + str( UserInputObj.mType ) )
    print( "Offset:      " + str( UserInputObj.mOffset ) )
    print( "Macro:       " + str( UserInputObj.mMacro ) )
    print( "\n\n" )
    return UserInputObj
# End of GetUserInput


"""
GetMasterCsv

!@brief - Gets the name of the mastter list of TD Ameritrade history, and performs
          basic checks about the file 

@returns - The path and name of the master list of TD Ameritrade history
"""
def GetMasterCsv():
    # Gets file to convert
    sensitive_path = str( os.environ[ 'SENSITIVE_FILES_PATH' ] )
    master_csv_path = sensitive_path + "global_transactions.csv"
    return master_csv_path
# End of GetMasterCsv


"""
FilterDate

!@brief - 

@param
@param

@returns - CSV object with only items that falls between the date selection
"""
def FilterDate( date_selection, dataframe ):
    filtered_df = dataframe
    start_date = date_selection[0]
    end_date = date_selection[1]

    # Makes index the date of action so it can be filtered
    #dataframe.set_index( "DATE OF ACTION", inplace = True )

    # Filters out the rows based on start / end date
    #return dataframe.loc[ start_date:end_date ]
    mask = ( filtered_df[ 'DATE OF ACTION' ] > start_date) & ( filtered_df[ 'DATE OF ACTION' ] <= end_date )
    return filtered_df.loc[ mask ]
# End of FilterDate


"""
FilterType

!@brief - 

@param
@param

@returns - Returns CSV object with only the type that has the same type as the selection
"""
def FilterType( type, dataframe ):
    filtered_df = dataframe
    if type == "options":
        filtered_df = filtered_df.loc[ ( filtered_df[ 'TYPE' ] == "Put" ) | ( filtered_df[ 'TYPE' ] == "Call" ) ]
    
    elif type == "stock":
        filtered_df = filtered_df.loc[ ( filtered_df[ 'TYPE' ] == "Stock" ) ]

    elif type == "all":
        pass
        # Do nothing, no filtering
    else:
        print( "Error: Unhandled FilterType")
        exit( 1 )
        # NOTE: This might result in a blank csv if it's not found
        # try:
        #     filtered_df = filtered_df.loc[ dataframe[ 'TYPE' ] == type ]

        # # TODO: Need to update this with the logger
        # except KeyError:
        #     print( "Can't find type: '" + type + "'" )
        #     exit( 1 )

    return filtered_df
# End of Filter Type


"""
FilterTicker

!@brief - 

@param
@param

@returns - 
"""
def FilterTicker( ticker, dataframe ):
    filtered_df = pd.DataFrame( columns = dataframe.columns )
    try:
        # print( "Ticker: " + str( ticker.split( " " ) ) )
        curr_df = dataframe.loc[ dataframe[ 'TICKER' ] == ticker ]
        filtered_df = pd.concat( [ filtered_df, curr_df ] )

    # TODO: Need to update this with the logger
    except KeyError:
        print( "Can't find ticker: '" + ticker + "'" )
        exit( 1 )

    return filtered_df
# End of FilterTicker

"""
SumAmount

!@brief - 

@param
@param

@returns - 
"""
def SumAmount( dataframe ):
    # TODO: Need to update this with the logger / add in a try / except
    total_sum = dataframe[ "AMOUNT" ].astype( float ).sum( axis=0 )

    return total_sum
# End of SumAmount


"""
SumQuantity

!@brief - 

@param
@param

@returns - 
"""
def SumQuantity( dataframe ):
    # TODO: Delete this, but really good to see all the dataframe
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     print( bought_df )

    # Drops all indexes not labeled "Bought" then sums the "QUANTITY" row
    index_df = dataframe[ dataframe['ACTION'] != "Bought" ].index
    bought_df = dataframe.drop( index_df )
    sum_bought = bought_df[ 'QUANTITY' ].astype( int ).sum( axis=0 )

    # Drops all indexes not labeled "Sold" then sums the "QUANTITY" row
    index_df = dataframe[ dataframe['ACTION'] != 'Sold' ].index
    sold_df = dataframe.drop( index_df )
    sum_sold = sold_df[ 'QUANTITY' ].astype( int ).sum( axis=0 )

    # Prints out results
    difference = int( sum_bought - sum_sold )

    return difference
# End of SumQuantity

def SumDividend( dataframe ):
    # Drops all indexes not labeled "Dividend" then sums the "QUANTITY" row
    index_df = dataframe[ dataframe['ACTION'] != "Dividend" ].index
    dividend_df = dataframe.drop( index_df )
    dividend_total = dividend_df[ 'AMOUNT' ].astype( float ).sum( axis=0 )

    return dividend_total
# End of SumDividend

def getArguments():
    parser = argparse.ArgumentParser( description='' )

    parser.add_argument( '--start_date',
                        metavar='Start Date',
                        dest='start_date',
                        default="2000-01-01",
                        required=False,
                        type=str,
                        help='Start date of what the user wants to parse. Will be 2000 by default.' )

    parser.add_argument( '--end_date',
                        metavar='End Date',
                        dest='end_date',
                        default="3000-12-31",
                        required=False,
                        type=str,
                        help='End date of what the user wants to parse. Will be 3000 by default.' )

    parser.add_argument( '--offset',
                        metavar='Offset',
                        dest='offset',
                        required=False,
                        default=0.0,
                        type=float,
                        help='Offset in dollars that will be added to the bottom line.' )

    parser.add_argument( '--ticker_list',
                        metavar='Ticker List',
                        dest='ticker_list',
                        required=False,
                        default="All",
                        type=str,
                        help='List of stock tickers in quotes, separated by spaces. example: "TSLA AAPL BA"' )

    parser.add_argument( '--sort_type',
                        choices=[ 'all', 'options', 'puts', 'calls', 'stock' ],
                        metavar='Sort Type',
                        dest='sort_type',
                        required=False,
                        default="Options",
                        type=str,
                        help='The type which will define how the CSV is filtered. Note: If \'all\' is selected,'\
                             'all tickers existing in global transactions will be selected regaurdless of date,'\
                             ' selection.' )

    parser.add_argument( '--macro',
                        choices=[ 'none', 'stock_report' ],
                        metavar='Macro',
                        dest='macro',
                        required=False,
                        default="none",
                        type=str,
                        help='Macros' )

    parser.add_argument( '-m',
                        help='available so we can debug in vscode' )

    return parser.parse_args()
# End of getArguments

def BuildStockProfile( dataframe, ticker_list ):
    status = True

    # unique_tickers = dataframe['TICKER'].unique()
    for ticker in ticker_list:
        # Initializing values:
        dividend_total = 0
        options_premium = 0
        stock_cost = 0
        owned_shares = 0
        cost_basis = 0
        adjusted_cost_basis = 0

        # Filtering out ticker
        ticker_dataframe = FilterTicker( ticker, dataframe )

        # Creating dataframes
        stock_dataframe = FilterType( "stock", ticker_dataframe )
        options_datafame = FilterType( "options", ticker_dataframe )

        # Calculating values
        dividend_total = SumDividend( stock_dataframe )
        options_premium = SumAmount( options_datafame )
        stock_cost = SumAmount( stock_dataframe )
        owned_shares = SumQuantity( stock_dataframe )

        if 0 < owned_shares:
            if stock_cost <= 0:
                cost_basis = abs( stock_cost ) / owned_shares
                adjusted_cost_basis = ( abs( stock_cost ) - options_premium ) / owned_shares
            else:
                # TODO: Use logger
                print( "Error: Stock cost non-negative" )
                exit( 1 )

        elif 0 > owned_shares:
            # TODO: Use logger
            print( "Error: can't have negative shares" )
            exit( 1 )


        print( "" )
        print( "==== " + str( ticker ) + " ===========================" )
        print( "Owned shares:       " + str( owned_shares ) )
        print( "Dividend total:     ${:.2f}".format( dividend_total ) )
        print( "Options Premium:    ${:.2f}".format( options_premium ) )
        if owned_shares != 0:
            print( "Stock cost:         ${:.2f}".format( stock_cost ) )
            print( "Cost Basis:         ${:.2f}".format( cost_basis ) )
            print( "Cost basis ( adj ): ${:.2f}".format( adjusted_cost_basis ) )
        else:
            print( "Total Profit:       ${:.2f}".format( stock_cost ) )
            print( " -- No costbasis. No shares owned. --" )


    return status
# End of BuildStock Profile

def main():
    # Gets arguments from user
    args = getArguments()

    # TODO: Vscode isn't finding this path while debugging...
    # Turns the master trade history into a pandas data frame to work with
    df = pd.read_csv( GetMasterCsv(), sep=',' )

    # Gets the user input of what the csv should filter
    UserInputObj = GetUserInput( args, df )

    if "stock_report" == UserInputObj.mMacro:
        if not BuildStockProfile( df, UserInputObj.mTickerList ):
            # TODO: Replace with logger
            print( "Error: issue building stock profile" )
            exit( 1 )

    elif "funding" == UserInputObj.mMacro:
        if True:
            # TODO: Replace with logger
            print( "Error: add function to calculate funding" )
            exit( 1 )

    elif "none" == UserInputObj.mMacro:
        # TODO: Clean this up, maybe move into a function
        # Filters based on ticker
        if len( UserInputObj.mTickerList ) != 0:
            for ticker in UserInputObj.mTickerList:
                df = FilterTicker( ticker, df )

        # Filters based on date
        df = FilterDate( UserInputObj.mDateRange, df )

        # Filter based on type
        df = FilterType( UserInputObj.mType, df )

        # TODO: This works for options. What about Stocks?
        # TODO: Think I want to put this into it's own function to handle tha outputs / final results
        # Prints out the total sum of filtered dataframe
        print( df )
        total_cost = round( SumAmount( df ), 2 ) + float( UserInputObj.mOffset )
        print( "Offset Entered: $" + str( UserInputObj.mOffset ) )
        print( "Total Cost:     $" + str( total_cost ) )

        if UserInputObj.mType == "Stock":
            total_amount = SumQuantity( df )
            print( "Total Amount:    " + str( total_amount ) )

            if total_amount != 0:
                cost_per_share = abs( round( ( total_cost / total_amount ), 2 ) )
                print( "Cost per share:  $" + str( cost_per_share ) )
            else:
                cost_per_share = "[ No shares owned. ]"
    else:
        # TODO: Replace with logger
        print( "Error: Unhandled macro choice" )
        exit( 1 )
    # End macro choice


    return

if __name__ == "__main__":
    main()
