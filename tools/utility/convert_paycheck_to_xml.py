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

from PyPDF2 import PdfReader
from dotenv import load_dotenv

# Environmental variables
load_dotenv()

#class Paycheck:
    



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
    PATH_TO_PDF = str(REPO_PATH) + "input/test_statement.pdf"
    # creating a pdf reader object
    reader = PdfReader( PATH_TO_PDF )

    # printing number of pages in pdf file
    print("len(reader.pages)")
    print(len(reader.pages))

    # getting a specific page from the pdf file
    page = reader.pages[0]

    # extracting text from page
    text = page.extract_text()
    print("text")
    print(text)

    text_block=''
    return text_block

def main():
    ConvertPdfToText()
    return

if __name__ == "__main__":
    main()



