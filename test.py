import plistlib

def ripRegMac(regFile):
    '''
    Gets the relevant info from the Mac Plist file provided. 
    inputs:
        regFile: a flat text file exported from Regedit program in windows.
    outputs:
        a list of tuples containing SSID, BSSID dictionary, and the connection date. Sorted by SSID
    ''' 
    p1 = plistlib.readPlist(regFile)
    outList = []
    for item in p1["KnownNetworks"]:
        ssid = p1["KnownNetworks"][item]["SSIDString"]
        bssidDict = {}
        connectDate = p1["KnownNetworks"][item]["LastConnected"]
        count = 0 
        for leaky in p1["KnownNetworks"][item]["BSSIDList"]:
            bssidDict[count] = leaky["LEAKY_AP_BSSID"]
            count += 1
        outList.append((ssid,bssidDict,connectDate))
    print(outList)


ripRegMac("com.apple.airport.preferences.plist")