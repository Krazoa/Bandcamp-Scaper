#Code by: Malfestio

import os
from bs4 import BeautifulSoup
from lxml import etree
import requests
import urllib.request
import re

def Soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, "lxml")

def userInpt():
    #Album URL input
    validationCondition = True
    while validationCondition == True:
        albumURL = input("Enter album URL: ")
        userValidation = input("Confirm album URL [y/n]: ")
        if userValidation == "y":
            validationCondition = False

    #Download destination input
    validationCondition = True
    while validationCondition == True:
        downloadURL = input("Enter download destination: ")
        userValidation = input("Confirm download destination [y/n]: ")
        if userValidation == "y":
            directoryValidation = os.path.exists(downloadURL)
            if directoryValidation == False:
                print("Invalid directory. Check your input directory and try again")
            else:
                print("Directory successfully validated")
                validationCondition = False
            
    return [albumURL, downloadURL]        

def retrieve(soup, downloadURL, givenTag1, givenTag2, extension):
    #Find item using given tags
    itemTag = soup.find(givenTag1, itemprop=givenTag2)
    #Find file from item source
    itemURL = itemTag.get("src")
    #Retrieve item source
    if itemURL != "":
        urllib.request.urlretrieve(itemURL, str(downloadURL + extension))
        return True
    else:
        return False

def getName(albumURL):
    slashCount = 0
    artistURL = ""
    index = 0
    while slashCount < 3:
        if albumURL[index] == "/":
            slashCount += 1
        if slashCount != 3:
            artistURL += albumURL[index]
        index += 1
    return artistURL

def illegalCharCheck(inptString):
    illegalChars = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"] #Potential bug with checking the "\\" char
    newString = ""
    invalidChar = False
    for index in range(0, len(inptString)):
        for illegalChar in illegalChars:
            if inptString[index] == illegalChar:
                newString += "-"
                invalidChar = True
        if invalidChar == True:
            newString += inptString[index]
            invalidChar == False
    return newString

#Get input and create soup
userInput = userInpt()
soup = Soup(str(userInput[0]))

#Get album cover
print("Getting album cover")
operationState = retrieve(soup, str(userInput[1]), "img", "image", "\cover.jpg")
if operationState == True:
    print("Album cover downloaded successfully!")
else:
    print("Error: Item not found. Check tags.")

#Get album data
artistURL = getName(userInput[0])
print(artistURL)

#Building track list
noOfTracks = 0
trackList = list()
trackNameList = list()
trackNameListStr = list()
tracks = soup.find_all("a", href=re.compile("/track/"),itemprop="url")

tracksOnAlbum = soup.find_all("span", itemprop={"name"}, text=True)
for trackName in tracksOnAlbum:
    trackNameList.append(trackName.find_all(text=True, recursive=False))
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
