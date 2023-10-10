# TODO: make header

from os import listdir
from os.path import isfile, join
import re
import shutil


def makeOneGlobalCsv():

    transaction_path = "/Users/phoot/code/finance/sensitive_files/"
    #transaction_path = "../../../sensitive_files"
    all_sensitive_files = [ file for file in listdir(  transaction_path )if isfile( join( transaction_path, file ) ) ]
    #print( __name__ + ": all files: " + str( onlyfiles ) )

    converted_files = []
    pattern = re.compile( "^converted_transactions_20[0-9][0-9]\.csv$" )
    for file in all_sensitive_files:
        #print( __name__ + ": file => " + file )
        if pattern.match( str( file ) ):
            converted_files.append( file )
            #print( __name__ + ": Found file: " + file )

    # Remove back up if it exists
    # Mv global to a back up if it exists
    # Create new global

    count = 0
    for file in converted_files:
        base_file = ""
        print( "here" )
        if count == 0:
            shutil.copyfile( transaction_path + str( file ), transaction_path + "/global_transactions.csv" )
            with open( transaction_path + file, 'r' ) as base:
                base_file = base.read()
                print( str( base_file ) )
            count += 1

        else:
            with open( transaction_path + file, 'r' ) as file_open:
                file_open.write( str( base_file ) )

   # with open('original.csv', 'r') as f1:
   #     original = f1.read()
   # 
   # with open('all.csv', 'a') as f2:
   #     f2.write('\n')
   #     f2.write(original)

    
    global_csv_name = "Fixme"
    return global_csv_name

def main():
    name = makeOneGlobalCsv()

    print( __name__ + ": " + name )

    return
# functions # Filter out stocks


if __name__ == "__main__":
    main()
