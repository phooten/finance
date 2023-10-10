#!/bin/

# Modules
import csv
import os
import pandas as pd
import sys
import inspect

# Project modules
from utility import class_filter_csv
from messages import class_messages

# Classes
msg = class_messages.messages()
csv_filter = class_filter_csv.csvFilter()
file_name = os.path.basename( __file__ )

def initialCsvFileCheck( csv_path ):
    """
    Description:    
    Arguments:      
    Returns:        
    """

    #file_name = sys._getframe(  ).f_code.co_file_name
    func_name= initialCsvFileCheck.__name__
    location = file_name + ":" + func_name

    # Checks the correct extension, which should only ever be .csv
    extension = csv_path[ len(csv_path)-4: ]
    if ".csv" != extension:
        msg.error( "File isn't .csv: '" + csv_path + "'", location )
        return False


    # Check the file exists
    if not os.path.isfile( csv_path ):
        msg.error( "File doesn't exist: '" + csv_path + "'", location )
        return False


    # Check the file isn't empty
    if os.stat( csv_path ).st_size == 0:
        msg.error( "File is empty: '" + csv_path + "'", location )
        return False

    return True


def contentsCsvFileCheck( csv_path ):
    """
    Description:    Checks the input CSV for basic contents to make sure it can be parsed. Includes header contents,
                    counts for columns and count for rows.
    Arguments:      csv_path [ string ] - Path to a a CSV to be parsed
    Returns:        Boolean - True for success, False for failure
    """

    #file_name = sys._getframe(  ).f_code.co_file_name
    func_name = contentsCsvFileCheck.__name__
    location = file_name + ":" + func_name

    # Gets characteristics of CSV
    df = pd.read_csv( csv_path, sep=',' )
    row_count, col_count = df.shape
    column_names = list(df.columns)

    # Checks the amount of rows in the given csv
    row_minimum = 2             # Header doesn't count as a row
    if row_count < row_minimum:
        msg.error( "File has [" + str(row_count) + "] rows. Need to have at least [" + str(row_minimum) + "].", location )
        return False

    # Checks the amount of columns in given csv
    if col_count != len( csv_filter.mTdHeaders ):
        msg.error( "File has [" + str(col_count) + "] headers but expects [" + str( len( csv_filter.mTdHeaders ) ) + "].", location )
        return False

    # Checks the names of the headers in csv
    for name in column_names:
        if name not in csv_filter.mTdHeaders:
            msg.error( "Header [" + name + "] is not in mTdHeaders:\n" + str(csv_filter.mTdHeaders), location )
            return False

    # All csv's seen end in the same message
    last_cell = df.loc[row_count - 1][ csv_filter.mTdHeaders[0] ] # Gets the last cell of the first column
    expected_eof = "***END OF FILE***"
    if last_cell != expected_eof:
        msg.error( "Last row of '" + csv_path + "' is expected to be '" + expected_eof + "' but is '" + last_cell + "'", location )
        return False

    return True


def transferCsvContents( input_csv, output_csv ):
    """
    Description:    
    Arguments:      
    Returns:        

    """

    #file_name = sys._getframe(  ).f_code.co_file_name
    func_name = transferCsvContents.__name__
    location = file_name + ":" + func_name

    # Gets characteristics of input csv
    df = pd.read_csv( input_csv, sep=',' )
    row_count, col_count = df.shape
    column_names = list(df.columns)

    # Creates base for new datafram
    new_csv = pd.DataFrame( columns=csv_filter.mOutputHeaders )

    # Filters information row by row of input csv
    for row_curr in range( row_count - 1 ):
        output_row = csv_filter.filterTdAmeritradeDetails( list( df.loc[ row_curr ] ) )
        new_csv.loc[ row_curr ] = output_row

    # Outputs the dataframe into a csv
    new_csv.to_csv( output_csv, index=True )
    #new_csv.to_csv( str(output_csv + ".tmp" ) )     # TODO: Compare this to "index = False"

    return

