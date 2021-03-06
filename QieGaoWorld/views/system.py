
import re,time
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from QieGaoWorld import parameter,common
from QieGaoWorld.views.decorator import check_post
from QieGaoWorld.views.decorator import check_login
from QieGaoWorld.views.dialog import dialog
from QieGaoWorld.models import Menu,Logs,Conf

@check_login
@check_post
def url(request, s):
    return eval(s)(request)



def menu_list(request,status=True):
    wenjuan=Menu.objects.order_by(status)

    return wenjuan 


def menu_star(request):
    status=str( request.POST.get('status',None))
    id=request.POST.get('id',None)
    menu=Menu.objects.get(id=id)
    if(status == "True"):
        menu.status=False
    else:
        menu.status=True
    menu.save()
    return HttpResponse(dialog('ok', 'success', 'ok!'))

def menu_del(request):
    id=request.POST.get('id',None)
    menu=Menu.objects.get(id=id)
    
    menu.delete()
    return HttpResponse(dialog('ok', 'success', '删除成功!'))

def menu_edit(request):
    id= request.POST.get('id',None)
    name=request.POST.get('name',None)
    url=request.POST.get('url',None)
    _type=request.POST.get("type",None)
    if(id==""):
        men=Menu.objects.filter(name=name)
        if(men):
            return HttpResponse(dialog('failed', 'danger', '该菜单名已被使用!'))
        menu=Menu(name=name,url=url,status=True,type=_type,parent=0)
    else:
        menu=Menu.objects.get(id=id)
        menu.name=name
        menu.url=url

    menu.save()
    return HttpResponse(dialog('ok', 'success', '编辑成功!'))

def para_list():
    _list=Conf.objects.all()
    return _list 

def para_edit(request):
    id= request.POST.get('id',None)
    name=request.POST.get('name',None)
    key=request.POST.get('key',None)
    content=request.POST.get("content",None)
    if(id==""):
        para=Conf.objects.filter(key=key)
        if(para):
            return HttpResponse(dialog('failed', 'danger', '该key已被使用!'))
        para=Conf(name=name,key=key,content=content)
    else:
        para=Conf.objects.get(id=id)
        para.name=name
        para.key=key
        para.content=content

    para.save()
    return HttpResponse(dialog('ok', 'success', '编辑成功!'))

def para_del(request):
    id=request.POST.get('id',None)
    para=Conf.objects.get(id=id)
    
    para.delete()
    return HttpResponse(dialog('ok', 'success', '删除成功!'))

def logs_list(request):
    
    
    # _list=system.logs_list(request,,page*size)
    # _list=Logs.objects.exclude(code="info").order_by("-time")[(page-1)*size:page*size]
    # _count=Logs.objects.annotate(count=Count("id")).exclude(code ="info").values("count")[0:1]
    # _count=_count[0]['count']/size +1
    type=request.POST.get("type","建筑申报")
    _list=Logs.objects.filter(code__contains='%s'%type).order_by("-time")
    page=request.POST.get("page",1)
    paginator = Paginator(_list, 25)
    _list=paginator.get_page(page)
    for i in range(0,len(_list)):
        _list[i].localtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(_list[i].time))

    context = {
        'permissions': request.session['permissions'],
        "list":_list,
        "page":common.page("system/logs_list",_list,type)
    }

    return render(request, "dashboard/system/logs_list.html", context)