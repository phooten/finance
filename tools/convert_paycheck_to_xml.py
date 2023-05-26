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
             "Pay Rate"
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
             "CO Taxable" ]

    text = text_block.split('\n')
    filtered_text = []

    # Checks for key words in text
    for line in text:
        for word in keys:
            if word in line:
                filtered_text.append( line )

    for line in filtered_text:
        print( line )

    return filtered_text



def ExtractInformation( pay_stub_obj, text_block ):
    # Key words to scan through paycheck

    for key in key_list_other:
        print("Looking for '" + str(key) + "'")
        for line in text_block:
            if key in line:
                print(line)

    return



def main():
    paycheck_text = ConvertPdfToText()

    paycheck_text = FormatUlaTextBlock( paycheck_text )
    # print(paycheck_text)
    stub = Paycheck()

    #ExtractInformation( stub, paycheck_text )

    return



if __name__ == "__main__":
    main()



