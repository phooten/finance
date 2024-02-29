
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
        self.mOffset = 0
# End of UserInput


"""
GetUserInput

!@brief Gets input from the user about how to sort out entries in the csv file

@returns - Object that stores user selections
"""
def GetUserInput( ):
    # Default input object selection
    UserInputObj = UserInput()

    # TODO: Make this from user input
    # Choices:
    #   All:        doesn't filter anything at all
    #   Options:    Includes "Put", "Call"
    #   Put:        Only "Put"
    #   Call:       Only "Call"
    choices = [ "Options", "Put", "Call", "Stock"]
    print( "Select one of the following:" )
    for choice in choices:
        print( "\t" + choice )


    UserInputObj.mType = input( "Enter type to filter: " )
    # TODO: Update this with the message logger.
    if UserInputObj.mType not in choices:
        print( "Issue with user selection '" + str( UserInputObj.mType ) + "'. It's not in choices: " + str( choices ) + ". Exiting script." )
        exit( 1 )

    # TODO: Need to error check this
    ticker = input( "Enter ticker: " )
    if ticker != "":
        UserInputObj.mTickerList.append( ticker )

    # TODO: Need error checking
    if UserInputObj.mType == "Stock":
        user_input = input( "Enter any offset: " )
        try:
            UserInputObj.mOffset = float( user_input )
        except:
            print( "User input wasn't a float" )
            UserInputObj.mOffset = 0

    # UserInputObj.mTickerList = [ "TSLA", "AAPL" ]
    UserInputObj.mDateRange[ 0 ] = "2024/01/01"     # Date range should be everything possible
    UserInputObj.mDateRange[ 1 ] = "3000/12/31"
#    UserInputObj.mDateRange[ 0 ] = "2000/01/01"     # Date range should be everything possible
#    UserInputObj.mDateRange[ 1 ] = "3000/12/31"

    # Clean up terminal with extra spaces
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


def main():
    # Gets the user input of what the csv should filter
    UserInputObj = GetUserInput()

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
