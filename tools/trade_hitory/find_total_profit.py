
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
        self.mTickerList = [ "" ]
        self.mDateRange = [ "01/01/2000", "01/01/2100" ]
        self.mType = "NA"
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
    UserInputObj.mType = "Options"                  # No specific types, should be everything
    UserInputObj.mTickerList = [ "TSLA" ]
    # UserInputObj.mTickerList = [ "TSLA", "AAPL" ]
    UserInputObj.mDateRange[ 0 ] = "2000/01/01"     # Date range should be everything possible
    UserInputObj.mDateRange[ 1 ] = "3000/12/31"

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

        except KeyError:
            print( "Can't find ticker: '" + ticker + "'" )
            exit( 1 )

    return filtered_df
# End of FilterTicker

"""
FilterTicker

!@brief - 

@param
@param

@returns - 
"""
def SumAmountFloat( csv_object ):
    total_sum = csv_object[ "AMOUNT" ].astype( float ).sum( axis=0 )

    return total_sum
# End of SumAmount


"""
FilterTicker

!@brief - 

@param
@param

@returns - 
"""
def SumAmountInt( csv_object ):
    #tmp = csv_object.where( csv_object[ 'ACTION' ] == 'Bought', csv_object[ 'QUANTITY' ] )
    tmp = csv_object.where( csv_object[ 'ACTION' ] == 'Bought' )
    print( tmp )
    # In "ACTION" column, if cell == Bought
    #   add
    # else if == Sold
    #   subtract
    # else
    #   ignore / error

    return tmp
# End of SumAmount


def main():
    # Gets the user input of what the csv should filter
    UserInputObj = GetUserInput()

    # Turns the master trade history into a pandas data frame to work with
    df = pd.read_csv( GetMasterCsv(), sep=',' )

    # Filters based on ticker
    df = FilterTicker( UserInputObj.mTickerList, df )

    # Filters based on date
    df = FilterDate( UserInputObj.mDateRange, df )

    # Filter based on type
    df = FilterType( UserInputObj.mType, df )

    # TODO: This works for options. What about Stocks?
    # Prints out the total sum of filtered dataframe
    print( "Total Cost:  $" + str( round( SumAmountFloat( df ), 2 ) ) )
    print( "Total Amount: " + str( SumAmountInt( df ) ) )

    return

if __name__ == "__main__":
    main()
