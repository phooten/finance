import os
from phootlogger import logger
from os import listdir
from os.path import isfile, join
import pandas as pd
import re
import shutil

msg = logger.messages( __name__ )

def makeOneGlobalCsv():

    # Makes a list of all converted files
    # TODO: Don't hard code this
    
    transaction_path = str( os.environ[ 'SENSITIVE_FILES_PATH' ] )
    global_transactions_file = str( os.environ[ 'GLOBAL_TRANSACTIONS' ] )
    global_transactions_file_backup = global_transactions_file + "_BACKUP.csv"

    # Gets a list of all files in the directory
    dir_list = sorted( listdir( transaction_path ) )
    all_sensitive_files = []
    for file in dir_list:
        all_sensitive_files.append( file )

    converted_files = []
    pattern = re.compile( "converted_transactions_20[0-9][0-9]\.csv$" )
    for file in all_sensitive_files:
        if pattern.match( str( file ) ):
            converted_files.append( file )
            msg.system( str( "Appending file to global csv '" + file + "'" ) )

    # Makes a backup of the global file if it exists, and removes the back up if it exists
    if os.path.exists( global_transactions_file_backup ):
        msg.system( "Old backup file removed under the name '" + global_transactions_file_backup + "'" )
        os.remove( global_transactions_file_backup )

    if os.path.exists( global_transactions_file ):
        msg.system( "Old file renamed to '" + global_transactions_file + "'" )
        os.rename( global_transactions_file, global_transactions_file_backup )

    # Appends all the found converted files to the global csv
    count = 0
    base_file = ""
    gf = open( global_transactions_file , "w" )
    for file in converted_files:
        with open( transaction_path + str( file ), "r" ) as tf:
            msg.system( "looking through file '" + file + "'" )
            gf.write( tf.read() )
            tf.close()

    gf.close()


    msg.system( "New file created under the name '" + global_transactions_file + "'" )

    return True, global_transactions_file


def convertAllAvailableCsvFiles():
    """
    Description:    
    Arguments:      
    Returns:        
    """

    mypath = str( os.environ[ 'SENSITIVE_FILES_PATH' ] )
    sensitive_files = [ f for f in listdir( mypath ) if isfile( join( mypath, f ) ) ]

    # TODO: This needs to not be hard coded
    regex_pattern_transactions = "^transactions_20[0-9][0-9]\.csv$"
    pattern_transactions = re.compile( regex_pattern_transactions )
    files_to_convert = []

    # TODO: Don't hard code single file conversion
    for file in sensitive_files:
        if pattern_transactions.match( file ):
            convert_file = True
            msg.system( "Found a file to convert '" + file + "'" )

            # Checks the file isn't already converted
            # TODO: Don't hard code this 'converted_'
            converted_file = "converted_" + file
            for file_conv in sensitive_files:
                if file_conv == converted_file:
                    msg.warning( "File has already been converted '" + file + "'. Waiting for user input." )

                    # Asks user if they want to overwrite conversion file
                    user_input = ""
                    while user_input != "y" and user_input != "n":
                        user_input = input( "Would you like to overwrite 'conversion_" + file + "' ? (y/n): " )
                        if user_input == "n":
                            msg.warning( "User chose 'n' so file won't be overwritten." )
                            convert_file = False
                    msg.system( "User chose 'y' so '" + file + "' will be converted and overwite file. Script continuing." )

            # Adds file to list and will convert later
            if convert_file:
                files_to_convert.append( file )


    for file in files_to_convert:
        msg.system( "Converting '" + file + "'" )
        #python __main__.py -f file
        try:
            msg.system( "Running command: 'python convert_single_td_csv/__main__.py -f " + file + "'" )
            os.system(f'python convert_single_td_csv/__main__.py -f {file}')
        except FileNotFoundError:
            # TODO: Don't hard code this
            msg.error( "The python program 'convert_single_td_csv/__main__.py' does not exist." )

    return True


def refineFile( raw_file ):
    """
    Description:    Removes headers that appear more than once and re-numbers the first column into a total order
    Arguments:      Raw file of the global file that was appended together
    Returns:        Void
    """

    count = 0
    df = pd.read_csv( raw_file, sep=',' )
    row_count, col_count = df.shape
    df_header_list = list(df.columns.values) 
    df_header_list = df_header_list[ 1: ]

    for row_index in range( row_count ):
        df_row_list = df.loc[ row_index ].values
        df_row_list = df_row_list[ 1: ]
        if set( df_row_list ) == set( df_header_list ):
            msg.system( "Found header row at index '" + str( row_index ) + "'. This is most likley the header of appeneded files, so this is being removed." )
            df = df.drop( index=row_index )

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.to_csv( raw_file, index=True )

        #if df.loc[ row ] == df.loc[ 0 ]:
        #    print( df.loc[ row ] )

#    with open( raw_file ) as fileObject:
#        for row in fileObject:
#            if count < 10:
#                print( row )
#
#            if count == 0:
#                #TODO: need to remove the header in the middle of the file and renumber the first column
#                header = row
#                print( row )
#                print( header )
#
#            else:
#                if row == header:
#                    msg.error( "Found another header at count '" + str( count ) + "'." )
#
#            count += 1

    return True

def main():

    passed = convertAllAvailableCsvFiles()
    if not passed:
        msg.error( "converAllAvailableCsvFiles() failed." )
        msg.quit_script()


    passed, file = makeOneGlobalCsv()
    if not passed:
        msg.error( "makeOneGlobalCsv() failed." )
        msg.quit_script()

    passed = refineFile( file )
    if not passed:
        msg.error( "refineFile() failed." )
        msg.quit_script()

    msg.quit_script()

    return


if __name__ == "__main__":
    main()

