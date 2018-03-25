#Code by: Krazoa

import shutil
import os
import sys
import subprocess
#import urlib2
from bs4 import BeautifulSoup
import requests
from lxml import etree

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
else:
    print("DEBUG: Loop Broken")

#Scrape album page**
response = requests.get(albumURL) #non-object var
soup = str(BeautifulSoup(response.content, "lxml"))
##with open(albumURL) as html_file: #object var
##    soup = str(BeautifulSoup(html_file, "lxml"))
#print(soup) #DEBUG: Checking to see if HTML was successfully grabbed

#Create a folder for the files to be downloaded in**
#fetch album title
albumTitle = soup.find('h2', class_="trackTitle")
print(albumTitle)

#download album cover**
##cover = soup.find('a', class_="popupImage")
##print(cover)


    #get album cover URL
#assign it to coverURL
#use scrapy to get it...
#...and deposit it into the download destination as 'cover.jpg'
#get number of tracks in album
#assign each track an index number
#for each index number in the album track list...
    #...open each URL Source for each track...
    #play music file (to enable streaming to the player, enabling download)
    #download the file to the download destination file address
#print 'done'

