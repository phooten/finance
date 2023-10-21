# TODO: make header

import os
from messages import class_messages
from os import listdir
from os.path import isfile, join
import re
import shutil

msg = class_messages.messages()

def makeOneGlobalCsv():

    # Makes a list of all converted files
    # TODO: Don't hard code this
    transaction_path = "/Users/phoot/code/finance/sensitive_files/"
    global_transactions_file = transaction_path + "global_transactions.csv"
    global_transactions_file_backup = global_transactions_file + "_BACKUP.csv"
    all_sensitive_files = [ file for file in listdir(  transaction_path )if isfile( join( transaction_path, file ) ) ]
    #print( __name__ + ": all files: " + str( sensitive_files ) )

    converted_files = []
    pattern = re.compile( "^converted_transactions_20[0-9][0-9]\.csv$" )
    for file in all_sensitive_files:
        if pattern.match( str( file ) ):
            converted_files.append( file )
            msg.system( "Appending file to global csv '" + file + "'", __name__ )

    # Makes a backup of the global file if it exists, and removes the back up if it exists
    if os.path.exists( global_transactions_file_backup ):
        msg.system( "Old backup file removed under the name '" + global_transactions_file_backup + "'", __name__ )
        os.remove( global_transactions_file_backup )

    if os.path.exists( global_transactions_file ):
        msg.system( "Old file renamed to '" + global_transactions_file + "'", __name__ )
        os.rename( global_transactions_file, global_transactions_file_backup )

    # Appends all the found converted files to the global csv
    count = 0
    base_file = ""
    gf = open( global_transactions_file , "w" )
    for file in converted_files:
        with open( transaction_path + str( file ), "r" ) as tf:
            msg.system( "looking through file '" + file + "'", __name__ )
            gf.write( tf.read() )
            tf.close()

    gf.close()


    msg.system( "New file created under the name '" + global_transactions_file + "'", __name__ )

    return True, global_transactions_file


def convertAllAvailableCsvFiles():
    """
    Description:    
    Arguments:      
    Returns:        
    """

    mypath = "/Users/phoot/code/finance/sensitive_files"
    sensitive_files = [ f for f in listdir( mypath ) if isfile( join( mypath, f ) ) ]

    # TODO This needs to not be hard coded
    regex_pattern_transactions = "^transactions_20[0-9][0-9]\.csv$"
    pattern_transactions = re.compile( regex_pattern_transactions )
    files_to_convert = []

    # TODO: warn if already converted
    # TODO: Don't hard code single file conversion
    for file in sensitive_files:
        if pattern_transactions.match( file ):
            msg.system( "Found a file to convert '" + file + "'", __name__ )

            # Checks the file isn't already converted
            # TODO: Don't hard code this 'converted_'
            converted_file = "converted_" + file
            for file_conv in sensitive_files:
                if file_conv == converted_file:
                    msg.warning( "File has already been converted '" + file + "'. Waiting for user input.", __name__ )

                    # Asks user if they want to continue
                    user_input = ""
                    while user_input != "y":
                        user_input = input( "Would you like to overwrite 'conversion_" + file + "' ? (y/n): " )
                        if user_input == "n":
                            msg.warning( "User chose 'n' so script won't continue.", __name__ )
                            return False
                    msg.system( "User chose 'y' so '" + file + "' will be converted and overwite file. Script continuing.", __name__ )

            # Adds file to list and will convert later
            files_to_convert.append( file )


    for file in files_to_convert:
        msg.system( "Converting '" + file + "'", __name__ )
        #python __main__.py -f file
        try:
            msg.system( "Running command: 'python convert_single_td_csv/__main__.py -f " + file + "'", __name__ )
            os.system(f'python convert_single_td_csv/__main__.py -f {file}')
        except FileNotFoundError:
            # TODO: Don't hard code this
            msg.error( "The python program 'convert_single_td_csv/__main__.py' does not exist.", __name__ )

    return True


def refineFile( raw_file ):
    """
    Description:    Removes headers that appear more than once and re-numbers the first column into a total order
    Arguments:      Raw file of the global file that was appended together
    Returns:        Void
    """

    count = 0
    with open( raw_file ) as fileObject:
        for row in fileObject:
            if count < 10:
                print( row )

            if count == 0:
                #TODO: need to remove the header in the middle of the file and renumber the first column
                header = row
                print( row )
                print( header )

            else:
                if row == header:
                    msg.error( "Found another header at count '" + str( count ) + "'.", __name__ )

            count += 1

    return True

def main():

    passed = convertAllAvailableCsvFiles()
    if not passed:
        msg.error( "converAllAvailableCsvFiles() failed.", __name__ )
        msg.quit_script()

    passed, file = makeOneGlobalCsv()
    if not passed:
        msg.error( "makeOneGlobalCsv() failed.", __name__ )
        msg.quit_script()
        

    passed = refineFile( file )
    if not passed:
        msg.error( "refineFile() failed.", __name__ )
        msg.quit_script()

    msg.quit_script()

    return


if __name__ == "__main__":
    main()

