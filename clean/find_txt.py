"""
Created: Aug 17th 2019
By: Sookyo Jeong (sookyojeong@gmail.com)

This script converts pdfs to text file in excel.
"""

import PyPDF2
import os

root = "/Volumes/ELEMENTS/lobbying/data"


lobbyingtxt = 'LOBBYING ACT'
fyear = 1958
lvolume =3
lyear = 1980


for y in range(fyear,lyear):
    print(y)
    for p in range(1,30):
        if ((p>=lvolume)&(y>=fyear))|(y>fyear):
            filename = 'GPO-CRECB-'+str(y)+'-pt'+str(p)+'.pdf'
            
            try:
                pdfFileObj = open(os.path.join(root,'raw/pdfs',filename), 'rb')
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                
                for page in range(0, pdfReader.numPages):
                    print('page '+str(page))
                    pageObj = pdfReader.getPage(page)
                    text = pageObj.extractText()
                    if ((lobbyingtxt in text)):
                        print('lobbying info is in text')
                        page_name = "{}-page{}.txt".format(filename,page)
                        with open(os.path.join(root,'raw/txt',page_name), mode='w', encoding='UTF-8') as o:
                            o.write(text)
                    else:
                        print('info not in text')
            except:
                print('pdf volume ',p,' not in folder')
                pass

