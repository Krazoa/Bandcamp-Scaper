#Code by: Malfestio

import os
from bs4 import BeautifulSoup
from lxml import etree
import requests
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
            validationCondition = False
            
    return [albumURL, downloadURL]        

def retrieve(soup, downloadURL, givenTag1, givenTag2, extension):
    #Find item using given tags
    itemTag = soup.find(givenTag1, itemprop=givenTag2)
    #Find file from item source
    itemURL = itemTag.get("src")
    #Retrieve item source
    if itemURL != ""
        urllib.request.urlretrieve(itemURL, str(downloadURL + extension))
        return True
    else:
        return False

def getName():
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
    illegalChars = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]
    newString = ""
    for index in range(0, len(inptString)):
        for illegalChar in illegalChars:
            if char == illegalChar:
                newChar = "
        newString
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
artistURL = getName()  

