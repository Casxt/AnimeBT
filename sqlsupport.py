#/usr/bin/python3.4
import pymysql
import time
#pymysql.install_as_MySQLdb()
config={'host':'******.rds.amazonaws.com',#默认127.0.0.1
        'user':'user',
        'password':'user',
        'port':3306 ,#默认即为3306
        'database':'DB',
        'charset':'utf8'#默认即为utf8
        }
class search():
    def __init__(self):
        self.id = ""
        self.name = ""
        self.amount = ""
        self.keyword = ""
        self.progress = ""
        self.isfinish = ""
        self.remark = ""
        self.addtime = ""
        self.state = "undefine"
        self.values = ""
    def define(self,values):
        self.values = values
        if len(values) == 9 and isinstance(values,tuple):
            self.id = values[0]
            self.name = values[1]
            self.amount = values[2]
            self.keyword = values[3]
            if values[4] == None:
                self.progress = 0 
            else:
                self.progress = values[4]
            self.isfinish = values[5]
            self.remark = values[6]
            self.addtime = values[7]
            self.updatetime = values[8]
            self.state = "success"
        else:
            self.state = "err"
    # def get_indexview_list_define(self,values):#id,name,remark,updatetime
        # self.values = values
        # if len(values) == 4 and isinstance(values,tuple):
            # self.id = values[0]
            # self.name = values[1]
            # self.remark = values[2]
            # self.updatetime = values[3]
            # self.state = "success"
        # else:
            # self.state = "err"
class download():
    def __init__(self):
        self.id = ""
        self.title = ""
        self.link = ""
        self.pubDate = ""
        self.description = ""
        self.enclosure = ""
        self.author = ""
        self.guid = ""
        self.category = ""
        self.isdownload = ""
        self.isdelete = ""
        self.path = ""
        self.filename = ""
        self.keyword = ""
        self.belongid = ""
        self.downloadid = ""
        self.downloadtime = ""
        self.time = ""
        self.state = "undefine"
        self.values = ""
    def getdownloads_define(self,values):
        self.values = values
        if len(values) == 6 and isinstance(values,tuple):
            self.id = values[0]
            self.title = values[1]
            self.enclosure = values[2]
            self.num = values[3]
            self.belongid = values[4]
            self.time = values[5]
            self.state = "success"
        else:
            self.state = "err"
    def getstate_define(self,values):
        self.values = values
        if len(values) == 4 and isinstance(values,tuple):
            self.id = values[0]
            self.downloadid = values[1]
            self.path = values[2]
            self.filename = values[3]
            self.state = "success"
        else:
            self.state = "err"
    def autodelete_getlist_define(self,values):#id,title,path,filename
        self.values = values
        if len(values) == 5 and isinstance(values,tuple):
            self.id = values[0]
            self.title = values[1]
            self.path = values[2]
            self.filename = values[3]
            self.downloadid = values[4]
            self.state = "success"
        else:
            self.state = "err"
def getkeyword ():#取得查询所需的关键字
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    sql = 'select * from AnimeBT_index_pi WHERE isfinish=0'  
    cursor.execute(sql)
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    list = []
    for value in values:
        a = search()
        a.define(value)
        list.append(a)
    return(["success",list])
def state_newdownload (items):#写入查询到的信息
    list = []
    for i in items:
        a = [i.title,i.link,i.pubDate,i.description,i.enclosure,i.author,i.guid,i.category,i.order,i.keyword,i.id,time.localtime()]
        list.append(a)
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    sql = 'insert into AnimeBT_state_pi (title,link,pubDate,description,enclosure,author,guid,category,num,keyword,belongid,time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.executemany(sql,list)
    cursor.close()
    conn.commit()
    conn.close()
    return("success")
def updateprogress (items):#更新progress信息
    list = []
    for i in items:
        a = [i.order,time.localtime(),i.id]
        list.append(a)
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    sql = "UPDATE AnimeBT_index_pi SET progress=%s,updatetime=%s WHERE id=%s"
    cursor.executemany(sql,list)
    cursor.close()
    conn.commit()
    conn.close()
    return("success")
def getdownloads():#取得尚未下载的剧集信息
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    sql = 'select id,title,enclosure,num,belongid,time from AnimeBT_state_pi WHERE isdownload=0'#状态0表示未下载
    cursor.execute(sql)
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    list = []
    for value in values:
        a = download()
        a.getdownloads_define(value)
        list.append(a)
    return(["success",list])
def getstate1():#取得state=1的剧集列表
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    sql = 'select id,downloadid,path,filename from AnimeBT_state_pi WHERE isdownload=1'#状态1表示只下载了BT种子
    cursor.execute(sql)
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    list = []
    for value in values:
        a = download()
        a.getstate_define(value)
        list.append(a)
    return(["success",list])
def getstate2():#取得state=2的剧集列表
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    sql = 'select id,downloadid,path,filename from AnimeBT_state_pi WHERE isdownload=2'#状态2表示正在下载
    cursor.execute(sql)
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    list = []
    for value in values:
        a = download()
        a.getstate_define(value)
        list.append(a)
    return(["success",list])
def updatestatedownloadid(download,state):#更新state信息
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    list = [[download.downloadid,download.path,download.filename,state,time.localtime(),download.id],]#,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    sql = "UPDATE AnimeBT_state_pi SET downloadid=%s,path=%s,filename=%s,isdownload=%s,downloadtime=%s WHERE id=%s"#
    cursor.executemany(sql,list)
    cursor.close()
    conn.commit()
    conn.close()
    return("success")
def checkindexfinished():#检查番剧是否下载完成
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    sql = "UPDATE AnimeBT_index_pi SET isfinish=1 WHERE progress >=  amount"
    cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()
    return("success")
def autodelete_getlist(interval=30):#取得需要删除的剧集信息
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    sql = "SELECT id,title,path,filename,downloadid from AnimeBT_state_pi WHERE isdelete=0 AND DATE_SUB(CURDATE(), INTERVAL %s DAY) > downloadtime"%(str(interval))#DATE_SUB(CURDATE(), INTERVAL 30 DAY) 取得30天前的日期
    cursor.execute(sql)
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    list = []
    for value in values:
        a = download()
        a.autodelete_getlist_define(value)
        list.append(a)
    return(["success",list])
def autodelete_updateisdelete(download):#更新isdelete信息
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    list = [[time.localtime(),download.id],]
    sql = "UPDATE AnimeBT_state_pi SET isdelete=1,downloadtime=%s WHERE id=%s"#
    cursor.executemany(sql,list)
    cursor.close()
    conn.commit()
    conn.close()
    return("success")
def get_indexview_list():
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    sql = 'select id,name,remark,updatetime from AnimeBT_index_pi ORDER BY updatetime desc'
    cursor.execute(sql)
    values = cursor.fetchall()
    print(values)
    list = []
    allinfolist=[]
    for value in values:
        a = {}
        a['id'] = value[0]
        a['name'] = value[1]
        a['remark'] = value[2]
        try:
            a['updatetime'] = value[4].strftime('%y-%m-%d %H:%M:%S')
        except:
            a['updatetime'] = "暂无信息"
        a['state'] = "success"
        list.append(a)
    for anime in list:
        sql = 'select id,title,enclosure,guid,num,path,filename,isdownload,isdelete,downloadtime from AnimeBT_state_pi WHERE belongid=%s ORDER BY num'%(anime['id'])
        cursor.execute(sql)
        values = cursor.fetchall()
        list2 = []
        for value in values:
            b = {}
            b['id'] = value[0]
            b['title'] = value[1]
            b['enclosure'] = value[2]
            b['guid'] = value[3]
            b['num'] = value[4]
            b['path'] = value[5]
            b['filename'] = value[6]
            b['isdownload'] = value[7]
            b['isdelete'] = value[8]
            b['downloadtime'] = value[9].strftime('%y-%m-%d %H:%M:%S')
            b['state'] = "success"
            if len(value[5].split(".")) > 1:
                b['ispath'] = 0
            else:
                b['ispath'] = 1
            list2.append(b)
        anime["episode"]=list2
        allinfolist.append(anime)
    cursor.close()
    conn.close()
    return(allinfolist)
