import requests
import json
import ast
from parser import *

# Translink api apiKey
apiKey = "API_KEY"
orgID = "ORGANIZATION_ID"

def getOrganizations():
    url = "https://us.ciscokinetic.io/api/v2/organizations"
    headers = {
        'Accept': "text/plain",
        'Authorization': "Token " + apiKey,
        'Cache-Control': "no-cache",
        'Postman-Token': "bd88e584-a8c9-5fb8-9362-27a962812d9e"
        }
    response = requests.request("GET", url, headers=headers)
    x = response.json()
    organizationID = x[0]['id']
    print(organizationID)
    return organizationID

# return all gateways in organization
def getGateways(orgID):
    url = "https://us.ciscokinetic.io/api/v2/organizations/" + orgID + "/gate_ways"
    headers = {
        'Accept': "application/json",
        'Authorization': "Token " + apiKey,
        'Cache-Control': "no-cache",
        }
    response = requests.request("GET", url, headers=headers)
    x = response.json()

    # create gateway in the form of a list of dictionaries
    gateways = []
    # create gateways in the form of a dictionary
    for g in x['gate_ways']:
        gateways.append({'name':str(g['name']),  'id':str(g['id']), 'serial':str(g['uuid'])})
        # gateways[str(g['name'])] = g[str('id')]
    # print(gateways)
    return gateways

# update gateway with desired gateway name
def updateGateway(gatewayID, gatewayName):
    url = "https://us.ciscokinetic.io/api/v2/gate_ways/" + gatewayID
    payload = "{ \n \"gate_way\":{ \n \"name\":\"" + gatewayName + "\"  \n } \n }"
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': "Token " + apiKey,
        'Cache-Control': "no-cache",
        }
    response = requests.request("PUT", url, data=payload, headers=headers)
    print(response.text)
    return

# take gateways dictionary and parse to remove brackets
def extractKineticGateways(gateways):
    temp=gateways.replace('[','')
    temp=temp.replace(']','')
    GW=ast.literal_eval(temp)
    return GW

# return device id from serial number.  Gets list of gateways and parses gateways to return list of dictionaries
def getGatewayIDfromSerial(serial):
    GW = getGateways(orgID)
    for x in GW:
        if x['serial'] == serial:
            return x['id']

    print('serial not found')
    return

# check output of head end router and see if it matches up with saved kinetic gateways.
# parseOutput to return dictionary of HER
# returns whether Gatway has been updated or not
def checkGWname(output,gateways):
    out = parseOutput(output)
    GW = gateways
    updated = 0
    for y in out:
        found = 0
        for x in GW:
            if y['serial'] == x['serial']:
                found = 1
                if y['busID'] != x['name']:
                    updateGateway(getGatewayIDfromSerial(y['serial']),y['busID'])
                    print('updated gateway')
                    updated = 1
                    break
                else:
                    print('gateway up to date')
                    break
        if found == 0:
            print('gateway not found')
    return updated
