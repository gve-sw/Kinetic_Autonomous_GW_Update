# main application script to be run. --> python app.py

from api import *
from sshExtract import *
import sched, time

# function to ssh into head end router, and check that output against the Kinetic datababse. If a change has been made update the gateway information
def HER(output,gateways):
    output = sshExt()
    x = checkGWname(output,gateways)
    if x == 1:
        gateways = getGateways(orgID)
    return gateways

# retrieve kinetic gateway info, check "range" times every "sleep" seconds for head end router datababse. Update kinetic every "sleep" seconds
while True:
    gateways = getGateways(orgID)
    output = ""
    for x in range(3):
        gateways = HER(output,gateways)
        time.sleep(10)
    time.sleep(10)
