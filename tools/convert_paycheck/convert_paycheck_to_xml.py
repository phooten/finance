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

    return all_content



def RefineText( text_block ):
    """
    Description:
    Arguments:
    Returns:
    """

    # These are hardcoded values we care about in the paycheck
    keys = [ "Period Beginning",
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
             "EMP Term Life",
             "If you have any questions regarding your" ]

    # Adds an element for every single key
    filtered_text = []
    found = False
    for curr in text_block:
        for key in keys:
            if key in curr:
                found = True
                filtered_text.append( curr )
                keys.remove( key )
                continue


    if len( keys ) != 0:
        print( "Not every key was found. See keys: '" + str( keys ) + "'\n")
        print( "Also see text:\n")
        for curr in text_block:
            print( curr )
        exit(1)

    # Useful to see what the filtered text contains
    pp.pprint( filtered_text )

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



