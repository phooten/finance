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

class Paycheck:
    key_list_other = [ "Period Beginning",
                        "Period Ending",
                        "Total Hours Worked",
                        "Pay Rate" ]

    key_list_earnings = [ "Salary",
                          "EIP",
                          "2nd Shift Prem 1.0",
                          "3rd Shift Prem 1.0",
                          "Overtime 1.0",
                          "Gross Pay" ]

    key_list_taxes = [ "D-401K Pre Tax",
                        "D-Medical BT",
                        "D-Dental BT",
                        "D-Health Savings Accnt BT",
                        "FED Withholding Tax",
                        "Social Security Tax",
                        "Medicare Tax",
                        "CO Withholding Tax",
                        "CO PFML Tax State Plan",
                        "Total Taxes" ]

    key_list_gross_to_net = [ "Total Earnings",
                                "Total Taxes",
                                "Total Deductions",
                                "Net Pay",
                                "Imputed Income",
                                "FED Taxable",
                                "CO Taxable" ]




def DownloadPaycheck():
    # ULA ADP site
    paycheck_site=''
    username=''
    pasword=''

    return paycheck



def ConvertPdfToText():

    # TODO: Fix this and the option-value-scan script. They are ahard coded values and 
    #       Need to be replaced with environmental variables. 
    REPO_PATH="/Users/phoot/code/finance/"
    PDF_PATH = str(REPO_PATH) + "input/paystubs/test_statement.pdf"
    with pdfplumber.open(PDF_PATH) as pdf:
        text = ""
        for page in pdf.pages:
            extracted_text = page.extract_text()
            text += f"Page {page.page_number + 1}:\n\n{extracted_text}\n\n"

    return text



def FormatUlaTextBlock( text_block ):

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

    text = text_block.split('\n')
    filtered_text = []

    # Checks for key words in text
    for line in text:
        for word in keys:
            if word in line:
                filtered_text.append( line )

    # Useful to see what the filtered text contains
    #pp = pprint.PrettyPrinter(width=41, compact=True)
    #pp.pprint( filtered_text )

    # Removes duplicate entries
    unique_text = []
    [unique_text.append(line) for line in filtered_text if line not in unique_text]

    # TODO: Need to filter out 2 numbers after the key is found
    # Removes key from line
    #for curr in range(len(unique_text)):
    #    for key in keys:
    #        unique_text[curr] = unique_text[curr].replace(key, '')
            #unique_text.insert(curr-1, str(key) + ":")
            #unique_text[curr] = unique_text[curr].replace(key, str(key) + ":\n\t")

    # Prints out text block
    #for line in unique_text:
    #    print( line )

    #return filtered_text
    return unique_text


def ExtractInformation( pay_stub_obj, text_block ):
    # Key words to scan through paycheck
    extracted_info = dict()

    # Extracts the payperiod ( start / end ), hours, payrate
    for key in pay_stub_obj.key_list_other:
        #print("Looking for '" + str(key) + "'")
        for line in text_block:
            if key in line:
                extracted_info[str(key)] = line

    # Extracts
    for key in pay_stub_obj.key_list_earnings:
        print("Looking for '" + str(key) + "'")
        for line in text_block:
            if key in line:
                extracted_info[str(key)] = line
                print( line )

    return



def main():
    paycheck_text = ConvertPdfToText()

    paycheck_text = FormatUlaTextBlock( paycheck_text )

    # Useful to see what the paycheck_text was
    #pp = pprint.PrettyPrinter(width=41, compact=True)
    #pp.pprint(paycheck_text)

    stub = Paycheck()
    ExtractInformation( stub, paycheck_text )

    return



if __name__ == "__main__":
    main()



