import csv;
import datetime;
import subprocess;

#Globals:
fileName = "snort.stats"

userName = "machina"
keyFile = "machina"
remoteDirectory = "/networking/packetLogs/"
serverUrl = "tempestindustries.net"

count = 0
total = 0

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
    subprocess.call(["scp", "-i", keyFile, userName + "@" + serverUrl + ":" + remoteDirectory + timeStamp])
    
def main():
    #print parseCurrentRate(fileName)
    #sendFileToServer("test.txt")
    
    
main()
