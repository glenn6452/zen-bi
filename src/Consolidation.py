#!/usr/bin/env python
# coding: utf-8

#Consolidation Data from Google Sheets (GDrive)
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import pandas as pd

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
drive = GoogleDrive(gauth)

drive = GoogleDrive(gauth)

# choose a local (colab) directory to store the data.
local_download_path = os.path.expanduser('drive/My Drive/Conso/')
try:
  os.makedirs(local_download_path)
except: pass

file_list = drive.ListFile(
    {'q': "'1oOMl4eFnt4f8e1jNiNBzKLpLv3wdNLSE' in parents"}).GetList()

file = []
for f in file_list:
  if f['id'] == '1auThKC1m8VhPAr0IsR2CDUaAAC46_B7Qu9Si0DBs3JI':
    file.append(f)
  else:
    None


for item in file:
    print(item['title'])
    # this should tell you which mimetype the file you're trying to download 
    # has. 
    print('title: %s, mimeType: %s' % (item['title'], item['mimeType']))
    mimetypes = {
        # Drive Document files as PDF
        'application/vnd.google-apps.document': 'application/pdf',

        # Drive Sheets files as MS Excel files.
        'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    # see https://developers.google.com/drive/v3/web/mim0e-types
    }
    download_mimetype = None
    if item['mimeType'] in mimetypes:
        download_mimetype = mimetypes[item['mimeType']]
        item.GetContentFile(os.path.join(local_download_path,item['title']+'.xlsx'), mimetype=download_mimetype)

        #item.GetContentFile(item['title'], mimetype=download_mimetype)
    else: 
        item.GetContentFile(os.path.join(local_download_path,item['title']))

xls = pd.ExcelFile(os.path.join(local_download_path,'TrialBalance.xlsx'))
sheets = xls.sheet_names

dfs = []
for i in range(len(sheets)):
    globals()['df'+str(i)] = pd.read_excel(xls,sheets[i])
    dfs.append(('df'+str(i),sheets[i]))
    
pd.DataFrame(dfs,columns=list(['dfs','sheets']))