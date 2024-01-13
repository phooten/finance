
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


# Input Object
class UserInput():
    """
    !@brief Creates a new object that stores user input

    @param mDateRange - 
    @param mType - 
    """
    def __init__( self ):
        self.mDateRange = ( "01/01/2000", "01/01/2100" )
        self.mType = "NA"


"""
GetUserInput

!@brief Gets input from the user about how to sort out entries in the csv file

@returns - Object that stores user selections
"""
def GetUserInput( ):
    # Default input object selection
    UserInput UserInputObj()

    UserInputObj.mType = "options"
    UserInputObj.mDateRange[ 0 ] = "01/01/2018"
    UserInputObj.mDateRange[ 1 ] = "01/01/2024"

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
    master_file = sensitive_path + "global_transactions.csv"
    return master_csv_path


"""
FilterDate

!@brief - 

@param
@param

@returns - CSV object with only items that falls between the date selection
"""
def FilterDate( date_selection, csv_object ):
    return


"""
FilterType

!@brief - 

@param
@param

@returns - Returns CSV object with only the type that has the same type as the selection
"""
def FilterType( type, csv_object ):
    return

def main():
    UserInput InputObj() = GetUserInputObj()

    return

if __name__ == "__main__":
    main()
    return
