#!/usr/bin/python

"""
ecmp_routing.py: run ECMP routing expts on a fat-tree and a non-blocking topology

Nikhil Handigol
"""

import sys
sys.path = ['../'] + sys.path

import os
import random
import json
from time import sleep
from optparse import OptionParser
from subprocess import Popen, PIPE
import multiprocessing
import termcolor as T

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info, warn, error, debug
from mininet.util import custom, quietRun, run

from topo import FatTreeTopo


def FatTreeNet(k=4, bw=100, cpu=-1,  queue=100):
    "Convenience function for creating pair networks"
    global opts

    #pox_c = Popen("~/pox/pox.py --no-cli riplpox.riplpox --topo=ft,%s --routing=st --mode=proactive 1> pox.out 2> pox.out" % (k), shell=True)
    pox_c = Popen("~/pox/pox.py --no-cli riplpox.riplpox --topo=ft,%s --routing=hashed --mode=reactive  1> pox.out 2> pox.out" % (k), shell=True)
    sleep(2) #wait a second for the controller to start
    topo = FatTreeTopo(k, speed=bw/1000.)
    #host = custom(CPULimitedHost, cpu=cpu)
    link = custom(TCLink, bw=bw, max_queue_size=queue)
	                      
    net = Mininet(topo, host=CPULimitedHost, link=link, 
	    switch=OVSKernelSwitch, controller=RemoteController, 
	    autoStaticArp=True)
    return net, pox_c

def progress(t):
    while t > 0:
	print T.colored('  %3d seconds left  \r' % (t), 'cyan'),
	t -= 1
	sys.stdout.flush()
	sleep(1)
    print '\r\n'

def hostArray( net ):
    "Return array[1..N] of net.hosts"
    try:
	host_array = sorted(net.hosts, key=lambda x: int(x.name))
    except:
	host_array = sorted(net.hosts, key=lambda x: x.name)
    return host_array

def enable_tcp_ecn():
    Popen("sysctl -w net.ipv4.tcp_ecn=1", shell=True).wait()

def disable_tcp_ecn():
    Popen("sysctl -w net.ipv4.tcp_ecn=0", shell=True).wait()

def enable_dctcp():
    Popen("sysctl -w net.ipv4.tcp_dctcp_enable=1", shell=True).wait()
    enable_tcp_ecn()

def disable_dctcp():
    Popen("sysctl -w net.ipv4.tcp_dctcp_enable=0", shell=True).wait()
    disable_tcp_ecn()

def FatTreeTest():
    "run the traffic on a fat tree"
    k = 4
    net, pox_c = FatTreeNet( k=k )
    net.start()
    hosts = hostArray( net )
    # wait for the switches to connect to the controller
    info('** Waiting for switches to connect to the controller\n')
    progress(5)
    net.pingAll()
    CLI(net)
    net.stop()
    pox_c.terminate()


def clean():
    '''Clean any running instances of POX'''
    p = Popen("ps aux | grep 'pox' | awk '{print $2}'",
	    stdout=PIPE, shell=True)
    p.wait()
    procs = (p.communicate()[0]).split('\n')
    for pid in procs:
	try:
	    pid = int(pid)
	    Popen('kill %d' % pid, shell=True).wait()
	except:
	    pass

if __name__ == '__main__':
    random.seed()
    setLogLevel( 'info' )

    #clean()

    FatTreeTest()

    Popen("killall -9 top bwm-ng", shell=True).wait()
    clean()
    os.system('sudo mn -c')
