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
    hours_worked='Testing'
#    gross_salary
#    gross_eip
#    gross_2nd_shift_premium
#    gross_3rd_shift_premium
#    gross_overtime
#    deduction_401k_pre_tax
#    deduction_medical
#    deduction_dental
#    deduction_hsa
#    tax_fed_withholding
#    tax_ss
#    tax_medicare
#    tax_co_witholding
#    tax_pfml_tax_state_plan



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



def ExtractInformation( pay_stub_obj, text_block ):
    


    return



def main():
    paycheck_text = ConvertPdfToText()

    stub = Paycheck()
    ExtractInformation( stub, paycheck_text )

    return



if __name__ == "__main__":
    main()



