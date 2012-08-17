#!/usr/bin/env python

from pysnmp.entity.rfc3413.oneliner import cmdgen
import sys, os, re, struct, threading

# determine directory automatically
directory = os.path.dirname(os.path.realpath(__file__))
parent = os.path.abspath(os.path.join(directory, os.path.pardir, os.path.pardir))
sys.path.append(parent)

import settings
from django.core.management import setup_environ
setup_environ(settings)
__builtins__.IS_SCRIPT = True

from nodeshot.models import *
from rrdgraphs.models import Graph

community = cmdgen.CommunityData('my-agent', 'public', 0)
pingcmd = "ping -c 1 %s > /dev/null"
MAX_THREAD_N = 10
interface_list = []
mutex = threading.Lock()
mac_format = "%02X:%02X:%02X:%02X:%02X:%02X"

oids = {'device_name': {'oid': (1,3,6,1,2,1,1,5,0), 'query_type': 'get',  'pos' : (3,0,1) },
        'device_type': {'oid': (1,2,840,10036,3,1,2,1,3,7), 'query_type': 'get',  'pos' : (3,0,1) },
        'ssid': {'oid': (1,3,6,1,4,1,14988,1,1,1,1,1,5), 'query_type': 'next',  'pos' : (3,0,0,1) },
        'frequency': {'oid': (1,3,6,1,4,1,14988,1,1,1,1,1,7), 'query_type': 'next',  'pos' : (3,0,0,1) },
        }


def tempname(ip,ifname):
    'comment'
    print "ifname" +ifname + "\n"
    global community
    transport = cmdgen.UdpTransportTarget((ip, 161))
    oid_in = None
    oid_out = None
    # search for the right oid
    for i in range(0,10):
            	if cmdgen.CommandGenerator().getCmd(community, transport, (1,3,6,1,2,1,2,2,1,2,i)  )[3][0][1] == ifname:
                	oid_in  = 1,3,6,1,2,1,2,2,1,10,i 
                	oid_out = 1,3,6,1,2,1,2,2,1,16,i
			print oid_in

class SNMPBugger(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self, name="ComputeThread-%d" % (id,))
    def run(self):
        while len(interface_list) > 0:
            # for each interface in interface_list ...
            mutex.acquire()
            inf = interface_list.pop() 
            mutex.release()
            ip = inf.ipv4_address
            # 1. check via ping if device is up
            ip_regexp = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
            if ip and len(ip) > 0 and ip_regexp.match(ip):
                ping_status = os.system(pingcmd % ip) # 0-> up , >1 down
            else:
                ping_status = 1 #invalid ip, maybe ipv6 or just mac
            if not ip or len(ip) <= 0:
                print "KO: Interface %d without ip (batman?)" % inf.id

            if ping_status == 0: #node answers to the ping
                device = inf.device
                node = inf.device.node
		ifname = inf.ifname
		if ifname:
			tempname(ip,ifname)


            else:
                # interface does not answer to ping
                print "KO: Interface %s is down" % ip
                inf.status = 'u'
                inf.save()


def main():
    print "main\n"
    for i in Interface.objects.all():
	try:
		g = Graph.objects.get(interface=i)
		if g.draw_graph:
       			 interface_list.append(i)

	except:
		None #print "No graph record for this interface\n"
    print interface_list
    for i in range(0, MAX_THREAD_N):
        # launch MAX_THREAD_N threads to bug the network
        SNMPBugger(i, ).start()
            
    try:
        from nodeshot.signals import clear_cache
        clear_cache()
    except:
        pass

if __name__ == "__main__":
        main()


