#Code by: Krazoa

import shutil
import os
import sys
from bs4 import BeautifulSoup
import requests
from lxml import etree
import urllib.request

#get target album URL**
albumURL = input("Enter target album URL: ")
validationCondition = 0
#get download destination file address (where track will be downloaded to
while validationCondition == 0:
    downloadDestination = input("Enter URL of download destination on your computer: ")
    #check download destination and verify its existance
    downloadConfirm = input("Are you sure this is your download directory? This cannot be changed. Please type [confirm] or press enter to cancel: ").upper()
    if downloadConfirm == "CONFIRM":
        directoryValidation = os.path.exists(downloadDestination)
        if directoryValidation == False:
            print("Invalid directory. Check your input directory and try again")
        else:
            print("Directory successfully validated")
            validationCondition = 1
    else:
        validationCondition = 0
#else:
    #print("DEBUG: Loop Broken")

#Scrape album page**
response = requests.get(albumURL) #non-object var
soup = BeautifulSoup(response.content, "lxml")
##with open(albumURL) as html_file: #object var
##    soup = str(BeautifulSoup(html_file, "lxml"))
#print(str(soup)) #DEBUG: Checking to see if HTML was successfully grabbed

#Create a folder for the files to be downloaded in**
#fetch album title
##albumTitle = soup.head2
##print(albumTitle)

#download album cover**
coverTag = soup.find("img", itemprop="image") #get album cover URL
coverUrl = coverTag.get("src") #assign it to coverURL
##coverResponse = requests.get(coverUrl, stream=True)#download the cover to destination folder
##with open(downloadDestination, "w", opener=opener) as file:#deposit it into the download destination as 'cover.jpg'
##    shutil.copyfileobj(coverResponse.raw, downloadDestination)
print(downloadDestination + "\cover.jpg")
urllib.request.urlretrieve(coverUrl, downloadDestination + "\cover.jpg")

#downloading tracks**
#get number of tracks in album
#assign each track an index number
#for each index number in the album track list...
    #...open each URL Source for each track...
    #play music file (to enable streaming to the player, enabling download)
    #download the file to the download destination file address
#print 'done'

