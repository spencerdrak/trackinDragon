import plistlib

def ripRegMac(regFile):
    '''
    Gets the relevant info from the Mac Plist file provided. 
    inputs:
        regFile: a flat text file exported from Regedit program in windows.
    outputs:
        a list of tuples containing SSID, BSSID, and the connection date. Sorted by SSID
    ''' 
    p1 = plistlib.readPlist(regFile)
    outList = []
    for item in p1["KnownNetworks"]:
        for leaky in p1["KnownNetworks"][item]["BSSIDList"]:
            print(leaky["LEAKY_AP_BSSID"])
            #outList.append(["KnownNetworks"][item]["SSIDString"],mac,p1["KnownNetworks"][item]["LastConnected"])
    print(outList)


ripRegMac("com.apple.airport.preferences.plist")