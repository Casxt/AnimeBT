#/usr/bin/python3.4
#------------web search-------------
import sys
import urllib
from urllib import request
import http.cookies
import os
import re
from xml.parsers.expat import ParserCreate
class item (object):
    def __init__(self):
        self.title = ""
        self.link = ""
        self.pubDate = ""
        self.description = ""
        self.enclosure = ""
        self.author = ""
        self.guid = ""
        self.category = ""
        self.order = ""
        self.keyword = ""
        self.xml = ""
        self.id = ""
        self.state = "undefine"
    def dealxml(self,xml):
        a = re.match(r'<title><\!\[CDATA\[([\S|\s]+?)\]\]></title><link>([\S|\s]+?)</link><pubDate>([\S|\s]+?)</pubDate><description><\!\[CDATA\[([\S|\s]+?)\]\]></description><enclosure\surl\="([\S|\s]+?)"[\S|\s]+?<author><\!\[CDATA\[([\S|\s]+?)\]\]></author><guid[\S|\s]+?>([\S|\s]+?)</guid><category[\S|\s]+?><\!\[CDATA\[([\S|\s]+?)\]\]></category>',xml).groups()
        self.xml = xml
        if len(a) == 8:
            self.title = a[0]
            self.link = a[1]
            self.pubDate = a[2]
            self.description = a[3]
            self.enclosure = a[4]
            self.author = a[5]
            self.guid = a[6]
            self.category = a[7]
            self.state = "success"
        else:
            self.state = "err"
def getdmhyxml(keyword):
    url = "http://share.dmhy.org/topics/rss/rss.xml?keyword=" + urllib.parse.quote(keyword).replace("%2B","+")
    req = request.Request(url)
    req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
    #尝试链接三次
    attempts = 1
    success = False
    while attempts < 3 and not success:
        try:
            xml = request.urlopen(req, timeout=120).read()
            success = True
        except:
            attempts = attempts + 1
    if attempts==3 and not success:
        return ("getdmhyxml err")
    #尝试链接三次
    xml = xml.replace(b"\n",b"").decode("utf-8")
    return (["success",xml])

def getitems(xml):
    list = []
    rule = r"<item>([\S|\s]+?)</item>"
    items = re.findall(rule,xml)
    resultnum = len(items)
    if resultnum != 0:
        for i in items:
            a = item()
            a.dealxml(i)
            list.append(a)
        return (["success",list])
    elif resultnum == 0:
        return ("get 0 result")
    else:
        return ("getitem err")

#已经废弃的函数
# def getanmielist(xml):
    # # rule = r'<item><title><\!\[CDATA\[([\S|\s]+?)\]\]></title>\
    # # <link>([\S|\s]+?)</link>\
    # # <pubDate>([\S|\s]+?)</pubDate>\
    # # <description><\!\[CDATA\[([\S|\s]+?)\]\]></description>\
    # # <enclosure url="([\S|\s]+?)"[\S|\s]+?/>\
    # # <author><\!\[CDATA\[([\S|\s]+?)\]\]></author>\
    # # <guid[\S|\s]+?>([\S|\s]+?)</guid>\
    # # <category[\S|\s]+?><\!\[CDATA\[([\S|\s]+?)\]\]></category></item>'
    # # #rule = r"<item>([\S|\s]+?)</item>"
    # #re_telephone = re.compile(rule.replace(b"\n",b"").decode("utf-8"))
    # vuinfos = re.findall(rule.replace(b"\n",b"").decode("utf-8"),xml)
    # return (len(vuinfos))
# def testxml():
    # f = open('testxml.xml', 'r')
    # print (f.read())
    # return (f.read())
    #
    #
    #class的废弃函数
    # def dealxml(self,xml):
        # self.xml = xml
        # self.title = re.search(r'<title><\!\[CDATA\[([\S|\s]+?)\]\]></title>', xml).group()
        # self.link = re.search(r'<link>([\S|\s]+?)</link>', xml).group()
        # self.pubDate = re.search(r'<pubDate>([\S|\s]+?)</pubDate>', xml).group()
        # self.description = re.search(r'<description><\!\[CDATA\[([\S|\s]+?)\]\]></description>', xml).group()
        # self.enclosure = re.search(r'<enclosure\surl\="([\S|\s]+?)"[\S|\s]+?<author>', xml).group()
        # self.author = re.search(r'<author><\!\[CDATA\[([\S|\s]+?)\]\]></author>', xml).group()
        # self.guid = re.search(r'<guid[\S|\s]+?>([\S|\s]+?)</guid>', xml).group()
        # self.category = re.search(r'<category[\S|\s]+?><\!\[CDATA\[([\S|\s]+?)\]\]></category>', xml).group()