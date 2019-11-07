from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
import io
import os

root = "/Volumes/ELEMENTS/lobbying/data"

rsrcmgr = PDFResourceManager()
retstr = io.StringIO()
codec = 'utf-8'
laparams = LAParams()
device = TextConverter(rsrcmgr, retstr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)

lyear=1971
buffer = 40

# check that the page is lobbying report
def reportPage(data):
    lines = [x.strip() for x in data.splitlines()]
    flag= False
    for word in lines:
        if (word[0:3]=="A. ")|(word[0:3]=="B. "):
            flag = True
            return flag
    return flag

# iterate through each txt file
for filename in os.listdir(os.path.join(root,'raw/txt')):
    try:
        name = os.path.splitext(filename)[0]
        print(name)
        
        if '.txt' in filename:
            # the original filename
            oname = filename.split(".")[0]+".pdf"
            # page name
            pname = int(filename.split(".")[1].split("-")[1][4:])
            # year
            yname = filename.split("-")[2]
            
            if int(yname)>=lyear:
                # get the original pdf
                fp = open(os.path.join(root,'raw/pdfs',oname), 'rb')
                
                iEnd = False
                
                for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
                                    
                    if ((pageNumber >= pname)&(iEnd==False)):
                        print("page number is ", pageNumber)
                        
                        # get text from pdf page
                        interpreter.process_page(page)
                        data = retstr.getvalue()
                        dname = oname.split("-")[3].split(".")[0]
                       
                        # verify that it is a lobbying reporde                    
                        if reportPage(data):
                            # save it
                            if os.path.exists(os.path.join(root,'raw/txt',yname,dname+'pg'+str(pname)+'.txt')):
                                with open(os.path.join(root,'raw/txt',yname,dname+'pg'+str(pname)+'.txt'), 'a+', encoding='utf-8') as file:
                                    file.write(data)
                            else:
                                with open(os.path.join(root,'raw/txt',yname,dname+'pg'+str(pname)+'.txt'), 'wb') as file:
                                    file.write(data.encode('utf-8'))
                    
                        if (reportPage(data)==False)&(pageNumber>=pname+buffer):
                            iEnd = True
                        
                        # re initiate
                        data = ''
                        retstr.truncate(0)
                        retstr.seek(0)
    except:
        print("parsing ",filename, " failed")
                    
