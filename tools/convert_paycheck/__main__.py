'''
This file is meant to automate moving my paycheck into an xml file.
    Features:
        - Downloads my paycheck
        - Converts the PDF into readable text
        - Moves that information into an XML sheet

    TODO: should not include anyt username / passwords in the file. instead
          manually enter it, or have a secure automated technique.
'''

# TODO: Find a better way to set/use environmental variables

#from PyPDF2 import PdfReader
from dotenv import load_dotenv
import pprint
import pdfplumber
import itertools
import re

# Environmental variables
load_dotenv()
pp = pprint.PrettyPrinter(width=41, compact=True)

class ExcelHeader:
    header_ula = [  "Period Beginning",
                    "Period Ending",
                    "Total Hours Worked",
                    "Pay Rate",
                    "Salary",
                    "EIP",
                    "2nd Shift Prem 1.0",
                    "3rd Shift Prem 1.0",
                    "Overtime 1.0",
                    "Gross Pay",
                    "D-401K Pre Tax",
                    "D-Medical BT",
                    "D-Dental BT",
                    "D-Health Savings Accnt BT",
                    "FED Withholding Tax",
                    "Social Security Tax",
                    "Medicare Tax",
                    "CO Withholding Tax",
                    "CO PFML Tax State Plan",
                    "Total Earnings",
                    "Total Taxes",
                    "Total Deductions",
                    "Net Pay",
                    "Imputed Income",
                    "FED Taxable",
                    "CO Taxable",
                    # These will be removed / not used
                    "Total Earnings",
                    "Net Pay",
                    "PTO Bank",
                    "Imputed Income",
                    "EMP Term Life" ]


# Prints out text in pretty format, then quits if explicitly selected.
def Pretty( text, stop=False):
    """
    Description:
    Arguments:
    Returns:
    """
    # Useful to see what the paycheck_text was
    pp = pprint.PrettyPrinter( width=41, compact=True )
    pp.pprint( text )
    if stop:
        exit(1)
    return




def ConvertPdfToText():
    """
    Description:
    Arguments:
    Returns:
    """

    # TODO: Fix this and the option-value-scan script. They are ahard coded values and
    #       Need to be replaced with environmental variables.
    REPO_PATH="/Users/phoot/code/finance/"
    PDF_PATH = str(REPO_PATH) + "sensitive_files/paystubs/test_statement.pdf"


    # Breaks down PDF into two sections, then finds text based on that
    x0 = 0.00   # Distance of left side of character from left side of page.
    x1 = 0.54   # Distance of right side of character from left side of page.
    y0 = 0.00   # Distance of bottom of character from bottom of page.
    y1 = 1.00   # Distance of top of character from bottom of page.

    all_content = []
    with pdfplumber.open( PDF_PATH ) as pdf:
        for i, page in enumerate( pdf.pages ):
            width = page.width
            height = page.height

            # Crop pages
            left_bbox = ( x0 * float( width ), y0 * float( height ), x1 * float( width ), y1 * float( height ) )
            page_crop = page.crop( bbox = left_bbox )
            left_text = page_crop.extract_text()

            left_bbox = ( 0.5 * float( width ), y0 * float( height ), 1 * float( width ), y1 * float( height ) )
            page_crop = page.crop( bbox = left_bbox )
            right_text = page_crop.extract_text()
            page_context = '\n'.join( [ left_text, right_text ] )
            all_content.append( page_context )
            #if i < 2:  # help you see the merged first two pages
            #    print(page_context)

    content_list = page_context.split('\n')

    return content_list



def RefineText( text_block ):
    """
    Description:
    Arguments:
    Returns:
    """

    # These are hardcoded values we care about in the paycheck

    # One argument after them
    keys_one = [ 
             "Period Beginning",
             "Period Ending",
             "Total Hours Worked",
             "Pay Rate",
             "PTO Bank Balance",
             "XXXXX1908" ]

    # Two arguments after them. If missing one, 0
    keys_two = [
             "Salary",
             "EIP",
             "2nd Shift Prem 1.0",
             "3rd Shift Prem 1.0",
             "Overtime 1.0",
             "Gross Pay",
             "D-401K Pre Tax",
             "D-Medical BT",
             "D-Dental BT",
             "D-Health Savings Accnt BT",
             "FED Withholding Tax",
             "Social Security Tax",
             "Medicare Tax",
             "CO Withholding Tax",
             "CO PFML Tax State Plan",
             "Total Earnings",
             "Total Taxes",
             "Total Deductions",
             "Net Pay",
             "Imputed Income",
             "FED Taxable",
             "CO Taxable",
             "Emp Term Life"
              ]

    keys = keys_one + keys_two


    # Adds an element for every key
    filtered_text = []
    for key in keys:
        found = False
        for curr in text_block:

            # Notes the element was found and adds to a new filtered block
            if key in curr:
                found = True
                filtered_text.append( curr )

                # Removes both the key and the found element
                text_block.remove( curr )
                break

        # Error: Key not found
        if not found:
            print( "ERROR:" )
            print( "Key not found '" + str( key ) + "'" )
            print( "Text:\n")
            for curr in text_block:
                print( "\t" + curr )
            exit(1)

    # Error: Not every key is accounted for
    if ( len( keys_one ) + len( keys_two ) ) != len( filtered_text ):
        print( "ERROR:" )
        print( "Not enough entries in fileted_text to match keys.")
        print( "filted_text:" )
        for curr in filtered_text: 
            print( "\t" + str( curr ) )
        print( "\nkeys_one:")
        for curr in keys_one:
            print( "\t" + str( curr ) )
        print("")
        print( "keys_two:" )
        for curr in keys_two:
            print( "\t" + str( curr ) )
        print("")
        exit(1)


    # Filters out the one / two arguments
    one_arg_list = []
    two_arg_list = []
    for curr in filtered_text:
        for key in keys:
            if key in curr:
                tmp = curr.replace( key, '' )       # Removes keyword from text
                tmp = tmp.replace( ':', '' )       # Removes all colons
                tmp = re.sub(r'^\s+', '', tmp )     # Removes leading whitespace
                tmp = re.sub(r'\s+$', '', tmp )     # Removes trailing whitespace
                tmp = tmp.split( ' ' )
                if ( len( tmp ) == 1 ) and ( key in keys_one ):
                    one_arg_list.append( [ key, tmp[ 0 ] ] )
                elif key in keys_two:
                    if len( tmp ) == 1:
                        two_arg_list.append( [ key, 0, tmp[ 0 ] ] )
                    elif len( tmp ) == 2:
                        two_arg_list.append( [ key, tmp[ 0 ], tmp[ 1 ] ] )
                    else:
                        print( "ERROR:" )
                        print( "tmp length is '" + str( len ( tmp ) ) + "' but is in keys_two." )
                        print( "key is '" + key + "'." )
                        print( "" )
                        exit(1)
                else:
                    print( "ERROR:" )
                    print( "Current element doesn't have 1 or 2 arguments." )
                    print( "len( tmp ) = " + str( len( tmp ) ) )
                    print( "tmp = '" + str(tmp) + "'" )
                    print( "curr: '" + curr + "'")
                    exit( 1 )

    print( "one_arg_list:" )
    for curr in one_arg_list:
        print( "\t" + str( curr ) )
    print( 'two_arg_list' )
    for curr in two_arg_list:
        print( "\t" + str( curr ) )
#
#
#    # Every key accounted for
#    print( "\n\nFound all keys. See text:" )
#    for curr in filtered_text:
#        print( "\t" + str( curr ) )

    return filtered_text



def main():
    # Takes out text into a pdf
    paycheck_text = ConvertPdfToText()

    # Formats text block based on ULA formating
    paycheck_text = RefineText( paycheck_text )

    # Useful to see what the paycheck_text was
    #pp = pprint.PrettyPrinter(width=41, compact=True)
    #pp.pprint(paycheck_text)

    return



if __name__ == "__main__":
    main()



