from django.shortcuts import render
from django.http import HttpResponse
from .Anime import *
from .sqlsupport import *
#from .GETBTseed import *
#from .Animedownload import *
#from .forms import AddForm  
# Create your views here.get_indexview_list()
def index(request):
    json = get_indexview_list()
    return render(request, 'index.html', {'json': json})
def SearchAnime(request):
    a = checkindexfinished() 
    b = updatestate()
    c = startdownload ()
    if a=="success" and b=="success" and isinstance(c,list):
        return HttpResponse(u"200")
    else:
        return HttpResponse(str(a)+str(b)+str(c))
def CheckDownload(request):
    a = checkstate1()
    b = checkstate2()
    if a=="finished" and b=="finished":
        return HttpResponse(u"200")
    else:
        return HttpResponse(str(a)+str(b))
def AutoDelete(request):
    a = autodelete()
    if a=="success":
        return HttpResponse(u"200")
    else:
        return HttpResponse(str(a))