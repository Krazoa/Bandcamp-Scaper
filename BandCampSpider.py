#Code by: Krazoa

import shutil
import os
import sys
from bs4 import BeautifulSoup
import requests
from lxml import etree
import urllib.request
import re
import time

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

#download album cover** (WORKS)
##coverTag = soup.find("img", itemprop="image") #get album cover URL
##coverUrl = coverTag.get("src") #assign it to coverURL
##urllib.request.urlretrieve(coverUrl, downloadDestination + "\cover.jpg")
##print("Album cover downloaded successfully")

#downloading tracks**
noOfTracks = 0
trackList = list()
trackNameList = list()
tracks = soup.find_all("a", href=re.compile("/track/"),itemprop="url")
#print(tracks) #DEBUG: Checking what tags were scrapped
##albumDesc = soup.find("meta", attrs={"name":"Description"})
##print(albumDesc)
##tracksOnAlbum = albumDesc.get("content")
tracksOnAlbum = soup.find_all("span", itemprop={"name"}, text=True) #Solution 2
#print(tracksOnAlbum)
for trackName in tracksOnAlbum:
    trackNameList.append(trackName.find_all(text=True))
trackLimit = len(tracksOnAlbum)
print(trackLimit)
for i in range(0, trackLimit): 
    trackList.append(tracks[i].get("href"))
    print(trackNameList[i]) #DEBUG: Checking if track names were extracted...
    print(trackList[i]) #DEBUG: ...along with their respective track URLs
    
    
    
#change albumUrl into albumTrackUrl (See notes)
#for i in range(0, 10): #Change max range to number of songs in album (Duplicate, consider merging this for loop in the above for loop
    #Open each link
        #fetch the track source
        #download it
print("Done")

