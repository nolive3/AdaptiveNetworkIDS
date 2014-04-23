################################################################################
# Resonance Project                                                            #
# Resonance implemented with Pyretic platform                                  #
# author: Hyojoon Kim (joonk@gatech.edu)                                       #
# author: Nick Feamster (feamster@cc.gatech.edu)                               #
# author: Muhammad Shahbaz (muhammad.shahbaz@gatech.edu)                       #
################################################################################
import os
import sys

import subprocess, threading
from idstools import unified2
from pyretic.pyresonance.json_sender import main as send_json

HOST = '127.0.0.1'
PORT = 50002
loop_alerts = True


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

def main():

    #t = threading.Thread(target=get_alerts)
    #t.start()
    get_alerts()
    while(true):
        filler = 1 #this can be removed. just to fill the while loop
        ##### Shanes stuff here
        ##### Sleep if not at send deadline
        ##### Send /var/log/snort/snort.log to the server
        ##### Clear /var/log/snort/snort.log but leave the file there
    
    #t.join()

if __name__ == '__main__': 
    main()
