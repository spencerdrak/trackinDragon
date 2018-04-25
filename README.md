# trackinDragon

A simple tool to get data from a Windows Registry, extract any historical BSSIDs that are stored in the registry, and then geolocate those BSSIDs if possible. This project was created for USMA Dept. of EECS CS483 Digital Forensics class.

Thanks to the WiGLE team for allowing use of their database for this project and to the Google team for the use of their API services.

Special thanks to the CS483 advisors/instructors for their help in getting this project started.

To run this script, please follow the steps below. 
* First, extract the data from the Registry of the computer in question, following these steps.
    1. Go to the windows start menu, and type “regedit.” Click on it, then hit yes when you are prompted.
    2. Drop down the “Computer” key if it isn’t already, and then drop down the “HKEY_LOCAL_MACHINE”
    3. Keep dropping down the keys until you reach the NetworkList key at this path: \Software\Microsoft\Windows NT\CurrentVersion\NetworkList 
    4. Right click on the “NetworkList” Key and then click export.
    5. Save this file to the _registryTracker_ directory.
* Then, you can run `python3 getCoords.py regTextFile.reg [WiGLE API KEY] [Google Geocode API KEY]` to get the output from the file. See below for notes on these keys. This will output a JSON with all the data you need, which is the input filename concatenated with _data.json_. Save this for later use. Then, it will also print out two lists, one with SSIDs it found, and the other with SSIDs it couldn't.
* Fire up the _map.html_ webpage on your browser. This will only run locally and is not hosted as an HTTP server (yet).
* Finally, import the JSON from earlier, hit enter, and BAM. You are viewing the locations of the SSIDs in the registry file.

Google Geocode is a service that allows you to turn an address or name into a latitutde and longitude. In order to get a Google Geocode API Key, you'll need to visit here: https://developers.google.com/maps/documentation/geocoding/get-api-key

WiGLE is a crowd-sourced database of BSSID's mapped to a location via their wardriving app. To obtain a key from them, go to: https://api.wigle.net/
Once you have a key, go to the "Your Account" Page, and click "Show my Token". From there, a box will give you a key that says "Encoded for Use:" feed this key into the python script for use. You may need to request more access, at the time of writing, WiGLE API is in Beta and they have a low limit on the database. You may not even have enough queries to perform a full check on a single registry.
