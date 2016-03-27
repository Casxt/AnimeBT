#/usr/bin/python3.4
from pprint import pprint
import xmlrpc.client
import json
url = 'http://localhost:6800/rpc'
dir = "/home/pi/file/video"
#dir = "/file/video"
def submitmtdownload (enclosure):
    s = xmlrpc.client.ServerProxy(url)
    gid = s.aria2.addUri([enclosure],{'dir':dir})
    return(gid)
# def submitbtdownload (download):
    # s = xmlrpc.client.ServerProxy(url)
    # gid = s.aria2.addUri([download.enclosure],{'dir':btdir})
    # return(gid)
def getstate(gid):
    s = xmlrpc.client.ServerProxy(url)
    state = s.aria2.tellStatus(gid)
    return(state)

    