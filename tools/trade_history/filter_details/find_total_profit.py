
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
# End of UserInput


"""
GetUserInput

!@brief Gets input from the user about how to sort out entries in the csv file

@returns - Object that stores user selections
"""
def GetUserInput( arguments ):
    # Default input object selection
    UserInputObj = UserInput()

    # Setting date range
    UserInputObj.mDateRange[ 0 ] = arguments.start_date
    UserInputObj.mDateRange[ 1 ] = arguments.end_date

    # Setting type to sort by
    UserInputObj.mType = arguments.sort_type

    # Setting ticker list
    ticker_list = list( arguments.ticker_list.split( " " ) )

    # Setting Offset
    UserInputObj.mOffset = float( arguments.offset )

    time.sleep(60)
    exit(1)
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
    sensitive_path = '/Users/phoot/code/finance/sensitive_files/'
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
def FilterDate( date_selection, csv_object ):
    start_date = date_selection[0]
    end_date = date_selection[1]

    # Makes index the date of action so it can be filtered
    #csv_object.set_index( "DATE OF ACTION", inplace = True )

    # Filters out the rows based on start / end date
    #return csv_object.loc[ start_date:end_date ]
    mask = ( csv_object[ 'DATE OF ACTION' ] > start_date) & ( csv_object[ 'DATE OF ACTION' ] <= end_date )
    return csv_object.loc[ mask ]
# End of FilterDate


"""
FilterType

!@brief - 

@param
@param

@returns - Returns CSV object with only the type that has the same type as the selection
"""
def FilterType( type, csv_object ):
    if type == "Options":
        csv_object = csv_object.loc[ ( csv_object[ 'TYPE' ] == "Put" ) | ( csv_object[ 'TYPE' ] == "Call" ) ]
    
    elif type == "All":
        pass
        # Do nothing, no filtering
    else:
        # NOTE: This might result in a blank csv if it's not found
        try:
            csv_object = csv_object.loc[ csv_object[ 'TYPE' ] == type ]

        # TODO: Need to update this with the logger
        except KeyError:
            print( "Can't find type: '" + type + "'" )
            exit( 1 )

    return csv_object
# End of Filter Type


"""
FilterTicker

!@brief - 

@param
@param

@returns - 
"""
def FilterTicker( ticker_list, csv_object ):
    filtered_df = pd.DataFrame( columns = csv_object.columns )
    for ticker in ticker_list:
        try:
            print( "Ticker: " + ticker )
            curr_df = csv_object.loc[ csv_object[ 'TICKER' ] == ticker ]
            filtered_df = pd.concat( [ filtered_df, curr_df ] )

        # TODO: Need to update this with the logger
        except KeyError:
            print( "Can't find ticker: '" + ticker + "'" )
            exit( 1 )

    return filtered_df
# End of FilterTicker

"""
SumAmountFloat

!@brief - 

@param
@param

@returns - 
"""
def SumAmountFloat( csv_object ):
    # TODO: Need to update this with the logger / add in a try / except
    total_sum = csv_object[ "AMOUNT" ].astype( float ).sum( axis=0 )

    return total_sum
# End of SumAmountFloat


"""
SumAmountInt

!@brief - 

@param
@param

@returns - 
"""
def SumAmountInt( csv_object ):
    # TODO: Delete this, but really good to see all the dataframe
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     print( bought_df )

    # Drops all indexes not labeled "Bought" then sums the "QUANTITY" row
    index_df = csv_object[ csv_object['ACTION'] != "Bought" ].index
    bought_df = csv_object.drop( index_df )
    sum_bought = bought_df[ 'QUANTITY' ].astype( int ).sum( axis=0 )

    # Drops all indexes not labeled "Sold" then sums the "QUANTITY" row
    index_df = csv_object[ csv_object['ACTION'] != 'Sold' ].index
    sold_df = csv_object.drop( index_df )
    sum_sold = sold_df[ 'QUANTITY' ].astype( int ).sum( axis=0 )

    # Prints out results
    difference = int( sum_bought - sum_sold )

    return difference
# End of SumAmountInt

def getArguments():
    parser = argparse.ArgumentParser( description='' )

    parser.add_argument( '--start_date',
                        metavar='Start Date',
                        dest='start_date',
                        default="01-01-2000",
                        required=False,
                        type=str,
                        help='Start date of what the user wants to parse. Will be 2000 by default.' )

    parser.add_argument( '--end_date',
                        metavar='End Date',
                        dest='end_date',
                        default="12-31-3000",
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
                        help='The type which will define how the CSV is filtered.' )

    parser.add_argument( '-m',
                        help='available so we can debug in vscode' )

    return parser.parse_args()
# End of getArguments

def main():
    # Gets arguments from user
    args = getArguments()

    # Gets the user input of what the csv should filter
    UserInputObj = GetUserInput( args )

    # Turns the master trade history into a pandas data frame to work with
    df = pd.read_csv( GetMasterCsv(), sep=',' )

    # Filters based on ticker
    if len( UserInputObj.mTickerList ) != 0:
        df = FilterTicker( UserInputObj.mTickerList, df )

    # Filters based on date
    df = FilterDate( UserInputObj.mDateRange, df )

    # Filter based on type
    df = FilterType( UserInputObj.mType, df )

    # TODO: This works for options. What about Stocks?
    # TODO: Think I want to put this into it's own function to handle tha outputs / final results
    # Prints out the total sum of filtered dataframe
    print( df )
    total_cost = round( SumAmountFloat( df ), 2 ) + float( UserInputObj.mOffset )
    print( "Offset Entered: $" + str( UserInputObj.mOffset ) )
    print( "Total Cost:     $" + str( total_cost ) )

    if UserInputObj.mType == "Stock":
        total_amount = SumAmountInt( df )
        print( "Total Amount:    " + str( total_amount ) )

        if total_amount != 0:
            cost_per_share = abs( round( ( total_cost / total_amount ), 2 ) )
            print( "Cost per share:  $" + str( cost_per_share ) )
        else:
            cost_per_share = "[ No shares owned. ]"


    return

if __name__ == "__main__":
    main()
