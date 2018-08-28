#Code by: Krazoa
#Bandcamp Spider: v0.1

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
        
#print("DEBUG: Loop Broken")
####Timer module
taskTimeStart = 0
taskTimeEnd = 0
taskTimeDiff = 0
taskTimeTotal = 0
    
        
#Scrape album page**
print("Getting album page HTML...")
taskTimeStart = time.time()
response = requests.get(albumURL) #non-object var
soup = BeautifulSoup(response.content, "lxml")
#print(str(soup)) #DEBUG: Checking to see if HTML was successfully grabbed
#taskTimeList.append(taskTimeStart - taskTimeEnd)
print("Got album page HTML")
taskTimeEnd = time.time()
taskTimeDiff = float(taskTimeEnd - taskTimeStart)
print("Operation completed in ", taskTimeDiff, "s")
taskTimeTotal += taskTimeDiff

#download album cover
print("Downloading album cover...")
taskTimeStart = time.time()
coverTag = soup.find("img", itemprop="image") #get album cover URL
coverUrl = coverTag.get("src") #assign it to coverURL
urllib.request.urlretrieve(coverUrl, downloadDestination + "\cover.jpg")
print("Album cover downloaded successfully")
taskTimeEnd = time.time()
taskTimeDiff = float(taskTimeEnd - taskTimeStart)
print("Operation completed in ", taskTimeDiff, "s")
taskTimeTotal += taskTimeDiff

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
trackNameListStr = list()
tracks = soup.find_all("a", href=re.compile("/track/"),itemprop="url")
#print(tracks) #DEBUG: Checking what tags were scrapped
##albumDesc = soup.find("meta", attrs={"name":"Description"}) #Scraping the discription to find no. of tracks: redundant now
##print(albumDesc)                                            #kept here for legacy reasons
##tracksOnAlbum = albumDesc.get("content")
tracksOnAlbum = soup.find_all("span", itemprop={"name"}, text=True)
#print(tracksOnAlbum)
for trackName in tracksOnAlbum:
    trackNameList.append(trackName.find_all(text=True, recursive=False))
#print(trackNameList) #DEBUG: Show the list of track names
trackLimit = len(tracksOnAlbum)

for iStr in range(0, len(tracksOnAlbum)):
    trackNameStrStore = str(trackNameList[iStr])
    trackCharIndex = 0
    trackNameStr = ""
    while trackCharIndex != len(trackNameStrStore):
        if trackNameStrStore[trackCharIndex] == "[" or trackNameStrStore[trackCharIndex] == "]":
            pass
        elif trackNameStrStore[trackCharIndex] == "'" or trackNameStrStore[trackCharIndex] == "'":
            pass
        else:
            trackNameStr += trackNameStrStore[trackCharIndex]
        trackCharIndex += 1
    trackNameListStr.append(trackNameStr)
#print(trackNameListStr) #DEBUG: Checking if the "[" and "'" elements are removed
#print(trackLimit) #DEBUG: Shows number of tracks on album
for i in range(0, trackLimit): #####replace with trackLimit for normal operation or 1 for testing
    print("Downloading track ", i, " - ", trackNameListStr[i])
    taskTimeStart = time.time()
    trackList.append(tracks[i].get("href"))#REMEMBER: The soup is an array/list
    #print(trackNameList[i]) #DEBUG: Checking if track names were extracted...
    #print(trackList[i]) #DEBUG: ...along with their respective track URLs
    #print(artistURL + trackList[i]) #DEBUG: Checking if track URL was successfully combined
    responseTrack = requests.get(artistURL + trackList[i])
    soup = BeautifulSoup(responseTrack.content, "lxml")
    trackJavaScript = soup.find_all("script", attrs={"type":"text/javascript"}, text=re.compile("t4.bcbits.com")) #Original method
    #print(trackJavaScript[0]) #Index value is hard coded as the 0th "script" tag contains one of the three mp3-128 urls
    ############
####REBUILD IS UP TO HERE#####
    ############
    if trackJavaScript == "":
        print("BUG: trackMp3128Tag = trackJavaScript[0].get_text(\"mp3-128\")\nIndexError: list index out of range")
        print("Skipping track")
        break
    trackMp3128Tag = trackJavaScript[0].get_text("mp3-128")
    #print(len(trackMp3128Tag))

    trackMp3128URL = ""
    tagPhrase = ""
    letter = 0
    firstOddQuoteMark = True
    #if the programs runs like stale shit sliding down a hill, it's because of this
    #for letter in range (0, len(trackMp3128Tag) - 1): #Removed due to the resetting of 'letter' each time this was run
    mp3128URLFound = False
    while letter != len(trackMp3128Tag) - 1 and mp3128URLFound == False:
        letter += 1
        quoteMarkCount = 0
        if trackMp3128Tag[letter] == '"': #If a new phrase is found, trigger phrase constructor
##            if firstOddQuoteMark == True:
##                quoteMarkCount = 2
##                firstOddQuoteMark = False
##            elif firstOddQuoteMark == False:
                quoteMarkCount += 1
                tagPhrase = ""
                while quoteMarkCount < 2:
                    letter += 1
                    #for letterPhrase in range (letter, len(trackMp3128Tag) - 1):
                    if trackMp3128Tag[letter] == '"':
                        quoteMarkCount += 1
                    else:
                        tagPhrase += trackMp3128Tag[letter]
        #print(tagPhrase) #DEBUG: Checking what the phrase constructor has built
        #This if statement produces 2 valid variations of the mp3-128 url. It has been
        #now set to only produce 1 but should be required, the other can be utilised
        if tagPhrase == "mp3-128" and mp3128URLFound == False:
            #print("Mp3-128 URL found")
            Mp3128URLIndex = letter + 3
            endQuoteMark = False
            while endQuoteMark == False:
                if trackMp3128Tag[Mp3128URLIndex] == '"':
                    endQuoteMark = True
                    letter = len(trackMp3128Tag) - 1
                else:
                    trackMp3128URL += trackMp3128Tag[Mp3128URLIndex]
                    Mp3128URLIndex += 1
            mp3128URLFound = True
            #print(trackMp3128URL) #DEBUG: Checking if the url has been correctly found and placed in variable
        if mp3128URLFound == True:
            #downloading the mmp3-128 file
            urllib.request.urlretrieve(trackMp3128URL, downloadDestination + "\\" + str(trackNameListStr[i]) + ".mp3")
            print("Saved as: ", downloadDestination + "\\" + str(trackNameListStr[i]) + ".mp3")
            letter = Mp3128URLIndex
            taskTimeEnd = time.time()
            taskTimeDiff = float(taskTimeEnd - taskTimeStart)
            print("Operation completed in ", taskTimeDiff, "s")
            taskTimeTotal += taskTimeDiff
            
print("Download Complete!")
print("All files saved in ", downloadDestination)
print("Total operation time: ", taskTimeTotal, "s")
print("Done")

