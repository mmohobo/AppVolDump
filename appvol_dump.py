# Logs into a VMware App Volumes manager via the web REST API and dumps all writeable volume info
# to a JSON file, and selected useful fields to a CSV for manipulation in your spreadsheet app of choice.

# IMPORTANT: This script was written for App Volumes v2209. If you have an earlier version (<2203)
# please ensure you read the API reference, as it will be different from what's in this script.

# Ref:  https://developer.vmware.com/apis/1331/app-volumes-rest

import requests
import json
import csv

# Edit hostname and domain to point to your App Volumes manager
managerHostname = 'servername'
managerDomain = 'company.com'

managerFQDN = managerHostname + '.' + managerDomain
sessionURL = 'https://' + managerFQDN + '/app_volumes/sessions'
writeablesURL = 'https://' + managerFQDN + '/app_volumes/writables'
csvFilename = managerHostname + '.csv'
jsonFilename = managerHostname + '.json'
userSession = requests.Session()

# Input credentials and create login POST json
print('Enter App Volumes admin user credentials')
username = input('Username: ')
password = input('Password: ')
loginCredentials = {'username': username, 'password': password}

# Login to App Volumes API with provided credentials
response = userSession.post(sessionURL, data=loginCredentials)

#Get all writeables
volumes = userSession.get(writeablesURL, cookies=userSession.cookies)

# Logout
logout = userSession.delete(sessionURL, cookies=userSession.cookies)
print(logout.json())

# Convert JSON to a dictionary, make it pretty, and save it to a file
volumesDict = json.loads(volumes.text)

prettyFormat = json.dumps(volumesDict, indent=4)
volumesFile = open(jsonFilename, "w")
volumesFile.write(prettyFormat)
volumesFile.close()

# Save a CSV of specified bits of info from the 'data' set
# Check the API reference and edit the csvHeaders and row variables if you want different info
csvHeaders = ['USERNAME', 'VOLUME ID', 'STATUS', '% AVAILABLE', 'LAST LOGIN']
volumesCSV = open(csvFilename, "w", encoding="utf-8")
csvWriter = csv.writer(volumesCSV)
csvWriter.writerow(csvHeaders)

for i in volumesDict['data']:
    row = [i['owner_upn'], i['id'], i['status'], i['percent_available'], i['mounted_at_human']]
    csvWriter.writerow(row)
    print("Username:", i['owner_upn'])
    print("Volume ID:", i['id'])
    print("Status:", i['status'])
    print("Percent available:", i['percent_available'])
    print("Last login:", i['mounted_at_human'])
    print()
    
volumesCSV.close()
