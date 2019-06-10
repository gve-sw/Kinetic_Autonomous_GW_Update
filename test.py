import re

def parseRemoteID(remoteID):
    BID=""
    matchID=0
    for y in remoteID:
        if y == "@":
            matchID=0
        if matchID == 1:
            BID += y
        if y == ":":
            matchID=1
    BID = re.sub('\D', '', BID)
    return BID

# parse IPv6 address and extract serial number
def parseIPv6(ipv6):
    i = 0
    serial = ""
    for x in ipv6:
        if i > 9:
            if x == '/':
                break
            serial += x
        i += 1
    serial=serial.replace(':',"")
    serial=serial.decode("hex")
    return serial

# parse through output.txt of head end router and extract Bus ID and Serial number. Return as list of dictionary.  {busID:xxx,serial:xxx}
def parseOutput(output):
    output=output.split(',')
    gatewayinfo =[]
    tempBID = ""
    for x in output:
        if 'Remoteid' in x:
            tempBID = parseRemoteID(x)
        if 'FC00:C15C:' in x:
            gatewayinfo.append({'busID':tempBID, 'serial':parseIPv6(x)})
    return gatewayinfo


print (parseRemoteID('Remote id: Bus-12345@iotspdev.io'))
