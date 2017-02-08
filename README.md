# AnimeBT
示例网址 anime.forer.cn (由于缺钱，服务器已关，而且依赖外部程序太多，暂时停止更新)<br>
A Django project can auto download anime from share.dmhy.org
因为懒得翻墙上花园。<br>
用python3写了一个程序自动下载新番。<br>
功能包括<br>
<br>
1.根据预设关键词自动搜索新资源<br>
2.自动调用下载器下载<br>
3.自动检测下载状态<br>
4.自动分析下载内容中的有效部分(多文件夹中，当只有一个视频时自动获取视频文件的地址作为默认地址)<br>
5.自动删除过期资源节约空间<br>
结合Nginx、MariaDB和Django后，成为了一个自动化的番剧下载网站。
<br>
数据库结构：<br>
Anime_index_pi:<br>
包含字段：id,name,amount,keyword,progress,isfinish,remark,addtime,updatetime<br>
Anime_state_pi:<br>
包含字段：id,title,link,pubDate,description,enclosure,author,guid,category,num,isdownload,isdelete,path,filename,keyword,belongid,downloadid,downloadtime,time<br>
数据库需要自行创建。<br>
需要配合aria2c作为下载器，配置文件已给出
最新动向：
最近增加了一个控制是否显示番剧的功能，日后详细写
