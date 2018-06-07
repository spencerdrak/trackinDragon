import plistlib

p1 = plistlib.readPlist("com.apple.airport.preferences.plist")
for item in p1["KnownNetworks"]:
    print(str(item))