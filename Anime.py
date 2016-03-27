#/usr/bin/python3.4
from .GETBTseed import *
from .sqlsupport import *
from .Animedownload import *
from pprint import pprint
import time
#checkindexfinished()检查整个番剧是否下载完成，每小时调用,执行成功返回success
#updatestate() 更新每集的下载信息，每小时调用,执行成功返回success
#startdownload () 开始下载未下载的番,每小时调用,与updatestate() 同步,执行成功返回开始下载番剧的信息
#checkstate1()检查种子是否下载完成，每10分钟调用,执行成功返回finished
#checkstate2()检查文件是否下载完成，每10分钟调用,执行成功返回finished
def searchinfo(keyword,order,digit=2):
    if isinstance(keyword,search):
        if keyword.state == "success":
            order = str(order).zfill(digit)
            keywords = keyword.keyword+"+"+order
            result = getdmhyxml(keywords)
            if result[0] == "success":
                results = getitems(result[1])
                if results[0] == "success":
                    item = results[1][0]#只取第一个结果！
                    item.keyword = keywords
                    item.id = keyword.id
                    item.order = order
                    return(["success",item])
                else:
                    return(results)
            else:
                return(result)
        else:
            return([keyword.values,keyword.state])                    
    else:
        return("error input")
def updatestate():
    keywords = getkeyword ()
    items = []
    print(keywords)
    if keywords[0]=="success" and len(keywords[1])!=0:
        for keyword in keywords[1]:
            print (keyword.keyword)
            print(keyword.progress)
            order = keyword.progress+1
            item = searchinfo(keyword,order)
            if item[0]=="success" and item[1].state == "success":
                #print(item[1].title)
                #print(item[1].link)
                items.append(item[1])
            else:
                continue
        l = state_newdownload (items)
        if l=='success' :
            u = updateprogress (items)
            if u=='success':
                return('success')
            else:
                return(u)
        else:
            return(l)
    else:
        return("all anime is finished")        
def startdownload ():
    list = []
    downloads = getdownloads()
    if downloads[0] == "success":
        for download in downloads[1]:
            if download.state == "success":
                gid = submitmtdownload (download.enclosure)#提交下载磁力链
                download.downloadid = gid
                info = getstate(gid)
                try:
                    download.path = info.get('dir','err')
                except:
                    download.path = "err"
                try:
                    download.filename = info["infoHash"]#["files"][0]["path"]
                except:
                    download.filename = "err"
                download.downloadtime = time.localtime()
                a = updatestatedownloadid(download,state=1)
                #print(a)
                list.append(download)
            else:
                continue
        return (list)
    return ("startdownload err")
def checkstate1():
    list = getstate1()
    if list[0]=="success":
        for download in list[1]:
            i  = checkstate1_getstate(download)
            print(i)
    else:
        return(list)
    return ("finished")
def checkstate2():
    list = getstate2()
    if list[0]=="success":
        for download in list[1]:
            i  = checkstate2_getstate(download)
            print(i)
    else:
        return(list)
    return ("finished")
def checkstate1_getstate(download):
    info = getstate(download.downloadid)
    followedBy = info.get("followedBy"," ")[0]
    if len(followedBy)==16 and followedBy != download.downloadid: 
        download.downloadid = followedBy
        try:
            download.path = info.get('dir','err')
        except:
            download.path = "err"
        try:
            download.filename = info["infoHash"]
        except:
            download.filename = "err"
        a = updatestatedownloadid(download,state=2)
        if a == "success":
            return("success")
        else:   
            return(a)
    return("no followedBy")
def checkstate2_getstate(download):
    info = getstate(download.downloadid)
    pprint (info)
    state = info.get("status","")
    if state == "complete": 
        try:
            download.path = info.get('dir','err')
        except:
            return ("download path err")
        try:
            download.filename = dealwith_file_path(info)#info["files"][0]["path"].split("/")[-1]#如果包含多个文件，即为一个文件夹时的处理办法。dealwith_file_path(info)
        except:
            return ("download filename err")
        a = updatestatedownloadid(download,state=3)
        if a == "success":
            return("success")
        else:   
            return(a)
    return("all finished")
def dealwith_file_path(info):
    maindir = info["dir"]+"/"
    num = 0
    for file in info["files"]:
        extraname = file["path"].split(".")[-1]
        if extraname in ["mp4","MP4","Mp4","mP4"]:#["85或以上版本____"] ["mp4","MP4","Mp4","mP4"]
            num = num+1
            subpath = file["path"].split(maindir)[-1]
    if num == 1:
        return(subpath)
    elif num != 1:
        return(info["files"][0]["path"].split(maindir)[-1].split("/")[0])
def autodelete():
    import os
    list = autodelete_getlist()
    if list[0]=="success":
        for anime in list[1]:
            filename = anime.filename.split("/")
            if len(filename) == 1:
                path = anime.path+"/"+anime.filename
                os.system("sudo rm -rf '%s'"%(path))
                autodelete_updateisdelete(anime)
            elif len(filename) > 1:
                path = anime.path+"/"+filename[0]
                os.system("sudo rm -rf '%s'"%(path))
                autodelete_updateisdelete(anime)
            else:
                return("autodelete err")
    return("success")
#pprint(get_indexview_list())
#pprint(updatestate())
#checkindexfinished()检查整个番剧是否下载完成，每小时调用
#updatestate() 更新每集的下载信息，每小时调用
#startdownload () 开始下载未下载的番,每小时调用,与updatestate() 同步
#checkstate1()#检查种子是否下载完成，每10分钟调用
#checkstate2()#检查文件是否下载完成，每10分钟调用