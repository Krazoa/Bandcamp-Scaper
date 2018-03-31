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
#print(str(soup)) #DEBUG: Checking to see if HTML was successfully grabbed

#download album cover** (WORKS)
##coverTag = soup.find("img", itemprop="image") #get album cover URL
##coverUrl = coverTag.get("src") #assign it to coverURL
##urllib.request.urlretrieve(coverUrl, downloadDestination + "\cover.jpg")
##print("Album cover downloaded successfully")

##getting raw bandcamp name
slashCount = 0
artistURL = ""
index = 0
while slashCount < 3:
    if albumURL[index] == "/":
        slashCount += 1
    if slashCount != 3:
        artistURL += albumURL[index]
    index += 1
#print(artistURL) #DEBUG: Checking the reconstructed bandcamp URL

#downloading tracks**
noOfTracks = 0
trackList = list()
trackNameList = list()
tracks = soup.find_all("a", href=re.compile("/track/"),itemprop="url")
#print(tracks) #DEBUG: Checking what tags were scrapped
##albumDesc = soup.find("meta", attrs={"name":"Description"}) #Scraping the discription: unused now
##print(albumDesc)                                            #kept here for legacy reasons
##tracksOnAlbum = albumDesc.get("content")
tracksOnAlbum = soup.find_all("span", itemprop={"name"}, text=True)
#print(tracksOnAlbum)
for trackName in tracksOnAlbum:
    trackNameList.append(trackName.find_all(text=True))
trackLimit = len(tracksOnAlbum)
#print(trackLimit) #DEBUG: Shows number of tracks on album
for i in range(0, 1): #####replace with trackLimit
    trackList.append(tracks[i].get("href"))#REMEMBER: The soup is an array/list
    #print(trackNameList[i]) #DEBUG: Checking if track names were extracted...
    #print(trackList[i]) #DEBUG: ...along with their respective track URLs
    #print(artistURL + trackList[i]) #DEBUG: Checking if track URL was successfully combined
    responseTrack = requests.get(artistURL + trackList[i])
    soup = BeautifulSoup(responseTrack.content, "lxml")
    trackJavaScript = soup.find_all("script", attrs={"type":"text/javascript"}, text=re.compile("t4.bcbits.com")) #Original method
    #print(trackJavaScript[7]) #Index value is hard coded as the 7th "script" tag contains the mp3-128 url
    #trackMp3128URL = trackJavaScript[7].get_text("mp3-128")
    
    #if the programs runs like stale shit sliding down a hill, its because of this
    for letter 
    
    #print(trackMp3128URL)


    
#change albumUrl into albumTrackUrl (See notes)
print("Done")

