################################################################################
# Resonance Project                                                            #
# Resonance implemented with Pyretic platform                                  #
# author: Hyojoon Kim (joonk@gatech.edu)                                       #
# author: Nick Feamster (feamster@cc.gatech.edu)                               #
# author: Muhammad Shahbaz (muhammad.shahbaz@gatech.edu)                       #
################################################################################
import os
import sys
import csv
import datetime
import subprocess
import threading
import time
from idstools import unified2
from pyretic.pyresonance.json_sender import main as send_json

HOST = '127.0.0.1'
PORT = 50002
loop_alerts = True

#Globals:
statsFileName = "snort.stats"
logFileName = "/var/log/snort/snort.log"

timeDelay = 3600

userName = "mininet"
keyFile = "mininetKey"
remoteDirectory = "/home/mininet/packetLog/"
serverUrl = "10.0.0.101"
count = 0
total = 0

#could use subprocess to start snort.
#command is sudo snort -dev -h 192.168.1.0/16 -c /etc/snort/snort.conf

def get_alerts():
   reader = unified2.SpoolRecordReader("/var/log/snort", "snort.alert", follow=True)
   while(loop_alerts):
        record = reader.next()
        if(record != None):
            cmd = "python ../pyretic/pyretic/pyresonance/json_sender.py --flow='{srcip=%s}' -e ids -s infected -a %s -p %d" % (record["source-ip"], HOST, PORT)
            myenv = os.environ.copy()
            subprocess.call(cmd, shell=True, env=myenv)
            #print "source IP     : %s" % record["source-ip"]
            #print "destination IP: %s" % record["destination-ip"]
            #print record
   return

def parseCurrentRate(name):
    
    mbsPERsec = 0
    
    with open(name, 'r') as statsFile:
        reader = csv.reader(statsFile)
        
        listReader = list(reader)
        
        lastLine = str(listReader[-1])
        
        if(lastLine.startswith("#", 2)):
            mbsPERsec = listReader[-2][2]
        
        else:
            mbsPERsec = listReader[-1][2]
        
    return mbsPERsec    
        
def updateMean():
    total += parseCurrentRate(fileName)
    count+= 1
    return    
    
def getMean():
    return float(total) / float(count)   
    
def sendFileToServer(name):
    timeStamp = "\"" + str(datetime.datetime.now()) + "\""
    subprocess.call(["scp", "-i", keyFile, name, userName + "@" + serverUrl + ":" + remoteDirectory + timeStamp])
 
def main():
   

    t = threading.Thread(target=get_alerts)
    t.start()
 
    while(True):   
        ##### Shanes stuff here
        ##### Sleep if not at send deadline
        ##### Send /var/log/snort/snort.log to the server
        ##### Clear /var/log/snort/snort.log but leave the file there
	    
	time.sleep(timeDelay)
	print "Awake. Attempting to send file to the server."
	sendFileToServer(logFileName)


    t.join()

if __name__ == '__main__': 
    main()
