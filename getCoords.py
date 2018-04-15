#!/usr/bin/python3

import requests
import json
import datetime
import sys

def getJSON(bssid,wigleKey):
    '''
    Takes a BSSID and gets the pertinent data from the WiGLE server to plot it. 
    inputs:
        bssid: a comma delimited BSSID (mac address) of the wifi access point
    outputs:
        returns a response from the database. Data is sanitized in the receiving function
    '''
    #print(bssid)
    bssidList = bssid.strip().split(",")

    json_headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic {}'.format(wigleKey)
    }
    url = 'https://api.wigle.net/api/v2/network/search?onlymine=false&freenet=false&paynet=false&netid={}%3A{}%3A{}%3A{}%3A{}%3A{}'.format(bssidList[0],bssidList[1],bssidList[2],bssidList[3],bssidList[4],bssidList[5])
    s = requests.session()
    #print("session created")
    resp = s.get(url, headers=json_headers)
    #print("response received")
    return resp

def extractInfo(ssid,resp):
    '''
    Takes the response from the wigle database and gets the relevant info out.
    input: 
        resp: See https://api.wigle.net/swagger for information on the format of the response JSON object
    output:
        tuple containing the latitude, longitude, and network SSID if avaialble. 
        If the search comes back negative, lat=long=0, and SSID = "No Network Found"
        If the client made a bad query, then lat=long=0, and SSID = "Bad Query"
    '''
    status = resp.status_code
    #if(status == 200):
    #    print("OK, query returned")
    #else:
    #    print("Server returned: " + str(status))
    #    return 0,0,"Bad Query"
    #print(resp.text)
    jsonResp = json.loads(resp.text)

    if(jsonResp["totalResults"] == 0):
        lat = 0
        lon = 0
        # print("Latitude: " + str(lat))
        # print("Longitude: " + str(lon))
        # print("Network SSID: " + str(ssid))
        return lat,lon,ssid,2
    else:
        lat = jsonResp["results"][0]["trilat"]
        lon = jsonResp["results"][0]["trilong"]
        ssid = jsonResp["results"][0]["ssid"]
        # print("Latitude: " + str(lat))
        # print("Longitude: " + str(lon))
        # print("Network SSID: " + str(ssid))
        return (lat,lon,ssid,1)

def ripReg(regFile):
    '''
    Gets the relevant info from the registry file provided. 
    inputs:
        regFile: a flat text file exported from Regedit program in windows.
    outputs:
        a list of tuples containing SSID, BSSID, and the connection date. Sorted by SSID
    ''' 
    with open(regFile,"r") as inFile:
        nameList = []
        bssidList = []
        dateNameList =[]
        dateList = []
        for line in inFile:
            if("FirstNetwork" in line):
                lst = line.split('"')
                if(len(lst) == 5):
                    nameList.append(lst[3].strip())
            if("DefaultGatewayMac" in line):
                lst = line.split(':')
                bssidList.append(lst[1].strip())
            if("ProfileName" in line):
                lst = line.split('"')
                if(len(lst) == 5):
                    dateNameList.append(lst[3].strip())
            if("DateCreated" in line):
                lst = line.split(':')
                dateList.append(lst[1].strip())

        zList1 = list(zip(nameList,bssidList))

        # print(len(zList1))
        # print(zList1)

        zList2 = list(zip(dateNameList,dateList))

        # print(len(zList2))
        # print(zList2)

        zList1.sort(key=lambda x: x[0])
        zList2.sort(key=lambda x: x[0])
        resultList = []

        for i in range(0,len(zList1)):
            resultList.append((zList1[i][0],zList1[i][1],decodeDate(zList2[i][1])))
            #name,bssid,date

        #print(resultList)
        return resultList

 
def getDayOfWeek(num):
    if(num == 0):
        return "Sunday"
    if(num == 1):
        return "Monday"
    if(num == 2):
        return "Tuesday"
    if(num == 3):
        return "Wednesday"
    if(num == 4):
        return "Thursday"
    if(num == 5):
        return "Friday"
    if(num == 6):
        return "Saturday"

def decodeDate(dateString):
    '''
    returns a python3 datetime object with the registry date string given.
    params: 
        dateString- a registry date string in hex
    output: 
        a python datetime.datetime object with the date time that the network was connected to.
    '''
    lst = dateString.split(",")
    yearHex = lst[1] + lst[0]
    monthHex = lst[3] + lst[2]
    weekdayHex = lst[5] + lst[4]
    dateHex = lst[7] + lst[6]           
    hourHex = lst[9] + lst[8]
    minHex = lst[11] + lst[10]
    secHex = lst[13] + lst[12]
    year = str(int(yearHex,16))
    month = str(int(monthHex,16))
    weekday = str(int(weekdayHex,16))
    date = str(int(dateHex,16))
    hour = str(int(hourHex,16))
    minute = str(int(minHex,16))
    sec = str(int(secHex,16))
    #print("{},{},{},{},{},{},{}".format(year,month,weekday,date,hour,minute,sec))
    dt = datetime.datetime(int(year),int(month),int(date),int(hour),int(minute),int(sec))
    #print(dt)
    #print(dt.weekday())
    #TODO- needs work. Python .weekday() seems to be one off from the given weekday in the registry.
    return dt

def createWordSet():
    '''
    reads in the word to take out of the SSIDs from the wifiWords.txt file in this directory.
    params: 
        N/A. 
    output: 
        a python set containing the words to remove from the SSIDs.
    '''
    badWordSet = set()
    with open("wifiWords.txt","r") as wordFile:
        for line in wordFile:
            word = line.strip().lower()
            badWordSet.add(word)
    return badWordSet

def checkBadPlaces(badList,googleKey):
    '''
    strips the SSID and tries to find a match based on the network name for the SSID using the Google geocode API.
    params: 
        badList- the list of tuples that WiGLE was unable to locate. 
    output: 
        two python lists of tuples - (SSID, BSSID, datetime.datetime, lat, long). First one is places it could locate, second one is places that remain unknown.
    '''
    newFoundList = []
    newBadList = []
    searchTermList = []
    badWordSet = createWordSet()
    for item in badList:
        ssid = item[0]
        lowCaseSSID = ssid.lower()
        wordList = lowCaseSSID.replace('-',' ').replace('_',' ').split()
        searchList = []
        for word in wordList:
            if word not in badWordSet:
                result = ''.join([letter for letter in word if not letter.isdigit()])
                searchList.append(result)

        searchTerm = " ".join(searchList)
        if(len(searchTerm) > 1):
            searchTermList.append(searchTerm)
            print("Rechecking SSID " + ssid + " using the text " + searchTerm + " on Google Geocode API.")
            resp = getGeocodeResp(searchTerm,googleKey)
            jsonResp = json.loads(resp.text)
            if(jsonResp["status"]=="ZERO_RESULTS"):
                newBadList.append((item[0],item[1],item[2],item[3],item[4],3))
            else:
                lat = jsonResp["results"][0]["geometry"]["location"]["lat"]
                lng = jsonResp["results"][0]["geometry"]["location"]["lng"]
                newFoundList.append((item[0],item[1],item[2],lat,lng,2))

    return newFoundList,newBadList

def getGeocodeResp(searchTerm,googleKey):
    '''
    takes a search term string and tries the Geocode API for it.
    params: 
        searchTerm -  a string with words separated by spaces
    output: 
        the as-is response from the server. 
    '''
    url = "https://maps.googleapis.com/maps/api/geocode/json?sensor=false&key={}&address={}".format(googleKey,searchTerm.replace(" ","%20"))
    s = requests.session()
    #print("session created")
    resp = s.get(url)
    #print("response received")
    return resp


def main(inFile,googleKey,wigleKey):
    '''
    returns a list of all the info needed. SSID, BSSID, dateconnected, lat, long.
    params: 
        inFile- the registry file in question. Must be a flat text file exported from Regedit program in windows.
    output: 
        a python list of tuples - (SSID, BSSID, datetime.datetime, lat, long). Includes empty hits from the database, no malformed queries.
    '''
    lst = ripReg(inFile) #name,bssid,date
    print("Ripped the data from the Reg File")
    lst.sort(key=lambda x: x[2]) #sort by date
    finalList = []
    for item in lst:
        if(len(item[1].split(","))==6):
            print(item[0])
            j = getJSON(item[1],wigleKey)
            lat,lon,ssid,status = extractInfo(item[0],j)
        if(ssid != "Bad Query"):
            finalList.append((ssid,item[1],item[2],lat,lon,status))

    notFound = []
    goodData = []

    for item in finalList:
        if(item[5] == 2):
            notFound.append(item)
        else:
            goodData.append(item)

    newFoundList,trueNotFoundList = checkBadPlaces(notFound,googleKey)

    for item in newFoundList:
        goodData.append(item)

    goodData.sort(key=lambda x: x[2])
    trueNotFoundList.sort(key=lambda x: x[2])

    outJSON = {}
    outJSON["registryFile"] = inFile
    outJSON["analysisTime"] = str(datetime.datetime.now())
    outJSON["goodData"] = {}
    outJSON["badData"] = {}
    for item in goodData:
        if(item[1] == "00,11,22,33,44,55" or item[0] == "IETDCommercial"):
            continue
        outJSON["goodData"][item[0]] = {"bssid":item[1],"dtg":str(item[2]),"coords":{"lat":item[3],"lng":item[4]},"source":item[5]}
    for item in trueNotFoundList:
        outJSON["badData"][item[0]] = {"bssid":item[1],"dtg":str(item[2]),"coords":{"lat":item[3],"lng":item[4]}}

    varName = inFile.split(".")[0]

    with open(varName + 'data.json', 'w') as outfile:
        json.dump(outJSON, outfile)

    print(goodData)
    print(trueNotFoundList)
        





if __name__ == "__main__":
    #j = getJSON("68:72:51:54:68:da")
    #lat,lon,ssid = extractInfo(j)
    #j = getJSON("14:91:82:a6:21:41")
    #lat,lon,ssid = extractInfo(j)
    #j = getJSON("a0:04:60:1a:ae:53")
    #lat,lon,ssid = extractInfo(j)
    #j = getJSON("68:72:51:54:6b:da")
    #lat,lon,ssid = extractInfo(j)
    #r = ripReg("USMAcomp.txt")
    if(len(sys.argv) < 2):
        sys.exit("Please include a filename argument. Exiting...")
    main(sys.argv[1],sys.argv[2],sys.argv[3])
