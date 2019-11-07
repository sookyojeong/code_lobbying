"""
    Created: Sep 18th 2019
    By: Sookyo Jeong (sookyojeong@gmail.com)
    
    This script takes txt where lobbying info is and turns it into dfs
    """

import numpy as np
import pandas as pd
import os
pd.set_option('display.max_colwidth', -1)

root = "/Volumes/ELEMENTS/lobbying/data"

def appendLine(line,df,flag,y,filename):
    types = ['A','B','C','D','E']
    # if item starts with either abcde
    if (itemStarts(line)!='Z'): #Z means not A,B,C,D,E
        for i in types:
            # if item starts with type
            if (itemStarts(line) == i):
                flag['A'] = flag['B'] = flag['C'] = flag['D'] = flag['E'] = False
                flag[i] = True 
                if (i != 'A'):
                    df.at[df.shape[0]-1,i] = str(df.at[df.shape[0]-1,i])+line
                    return df, flag
                    '''
                    if (df.iloc[df.shape[0]-1].isnull()[i]==True):  # if missing, fill it
                        df.at[df.shape[0]-1,i] = line
                        return df, flag
                    else:
                        # if not, add new obs
                        df = df.append({i:line}, ignore_index=True)
                        df.at[df.shape[0]-1,'year'] = y
                        df.at[df.shape[0]-1,'filename'] = filename
                        return df,flag
                    '''
                else:
                    df = df.append({i:line}, ignore_index=True)
                    df.at[df.shape[0]-1,'year'] = y
                    df.at[df.shape[0]-1,'filename'] = filename
                    return df,flag
    # if item doesnt start with abcde
    else:        
        for i in types:
            if (flag[i]==True): 
                df.at[df.shape[0]-1,i] = df.iloc[df.shape[0]-1][i] + line 
                return df,flag
        

def itemStarts(line):
    types = ['A','B','C','D','E']
    for i in types:
        if (line[0:3]==i+". "):
            return i  
    return 'Z'

df = pd.DataFrame() # initiate data frame
df['A']= df['B']=df['C']=df['D']=df['E']=df['year']=df['filename']=""
flag = {}  # flags to indicate item type
 
for y in range(1950,1980):
    for filename in os.listdir(os.path.join(root,'raw/txt',str(y))):

        flag['report']=flag['A']=flag['B']=flag['C']=flag['D']=flag['E']=False
        
        with open(os.path.join(root,'raw/txt',str(y),filename), encoding='utf-8', errors='ignore') as f:
            for line in f:
                print(line)
                # mark the start of report if hadn't already
                if (flag['report'] == False):
                    # if it starts with "A. " then it's the start of report
                    if (line[0:3]=="A. "):
                        flag['report'] = True
                
                # if the report started, and didn't end, record it as data
                if (flag['report'] == True):
                    if (line != '\n'):
                        df,flag = appendLine(line,df,flag,y,filename)
        
df.shape

# after compiling, clean 'nan' strings in fields B,C,D,E
for c in ['B','C','D','E']:
    df[c] = df[c].astype(str).str.strip('$nan')
 
df.to_csv(os.path.join(root,'clean/congreport.csv'), encoding='utf-8')
