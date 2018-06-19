import plistlib

def ripRegMac(regFile):
    p1 = plistlib.readPlist(regFile)
    for item in p1["KnownNetworks"]:
        print(p1["KnownNetworks"][item]["LastConnected"])


ripRegMac("com.apple.airport.preferences.plist")