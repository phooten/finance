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

def initialCsvFileCheck( csv_path ):
    """
    Description:    
    Arguments:      
    Returns:        
    """


    # Checks the correct extension, which should only ever be .csv
    extension = csv_path[ len(csv_path)-4: ]
    if ".csv" != extension:
        msg.error( "File isn't .csv: '" + csv_path + "'", "TODO")
        return False


    # Check the file exists
    if not os.path.isfile( csv_path ):
        msg.error( "File doesn't exist: '" + csv_path + "'", "TODO" )
        return False


    # Check the file isn't empty
    if os.stat( csv_path ).st_size == 0:
        msg.error( "File is empty: '" + csv_path + "'", "TODO" )
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
        msg.error( "File has [" + str(row_count) + "] rows. Need to have at least [" + str(row_minimum) + "].", "TODO" )
        return False

    # Checks the amount of columns in given csv
    if col_count != len( csv_filter.td_headers ):
        msg.error( "File has [" + str(col_count) + "] headers but expects [" + str( len( csv_filter.td_headers ) ) + "].", "TODO" )
        return False

    # Checks the names of the headers in Csv
    for name in column_names:
        if name not in csv_filter.td_headers:
            msg.error( "Header [" + name + "] is not in td_headers:\n" + str(csv_filter.td_headers), "TODO" )
            return False

    return True

def transferCsvContents( input_csv, output_csv ):
    """
    Description:    
    Arguments:      
    Returns:        

    """

    # Gets characteristics of input csv
    df = pd.read_csv( input_csv, sep=',' )
    row_count, col_count = df.shape
    column_names = list(df.columns)

    # Creates base for new datafram
    new_csv = pd.DataFrame( columns=csv_filter.output_headers )

    # TODO: before doing anything else:
    #       - move this check to the proper location:
    #       - clean this up
    #       - write unit test for it
    # NOTE: Last row is expected to be *EOF*
    last_cell = df.loc[row_count - 1][ csv_filter.td_headers[0] ] # Gets the last cell of the first column
    should_be = "***END OF FILE***"
    if str(last_cell) != should_be:
        msg.error( "Last row is not \"" + should_be+ "\": '" + str(last_cell) + "'", "TODO")
        return False



    # Filters information row by row of input csv
    for row in range( row_count - 2 ):
        # TODO: after doing the above todo, start filtering out by row
        print( str(row) )


    # Outputs the dataframe into a csv
    new_csv.to_csv( output_csv, index=False )
    new_csv.to_csv( str(output_csv + ".tmp" ) )     # TODO: Compare this to "index = False"


