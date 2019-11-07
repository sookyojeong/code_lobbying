"""
Created: June 21st 2019
By: Sookyo Jeong (sookyojeong@gmail.com)

This script gets pdfs of Congressional Reports (Bound) from gov website.
1950-1979 (volumne 96-125)
"""

import os
import requests
import json

root = "/Volumes/Elements/lobbying/data"
lyear = 1979
lvolume = 31

# get 1950-13 and 1951-1 again
for y in range(1950,1980):
    for p in range(1,40):
        if ((p>=lvolume)&(y>=lyear))|(y>lyear):
            issue = 'GPO-CRECB-'+str(y)+'-pt'+str(p)
            url = 'https://www.govinfo.gov/content/pkg/'+issue+'/pdf/'+issue+'.pdf'
            r = requests.get(url, stream=True)
            
            if (r.status_code==200):
                with open(os.path.join(root,'raw/pdfs',issue+'.pdf'), 'wb') as f:
                    f.write(r.content)
                    f.close()
                    
