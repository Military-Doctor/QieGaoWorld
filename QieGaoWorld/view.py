import logging,json

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from QieGaoWorld.views.announcement import announcement_list
from .views.declare import animals_list, buildings_list
from .views.decorator import check_login, check_post
from .views.police import page_police_hall
from .views.settings import page_settings
from .views.ops import whitelist
from .views.wenjuan import problem_list
from .views import system,society,skull,task
from QieGaoWorld import parameter as Para 
from QieGaoWorld.models import DeclareBuildings, DeclareAnimals, Cases,Menu,Conf,SkullCustomize,Logs
from QieGaoWorld import common

from QieGaoWorld.views.police import username_get_nickname

from django.db.models import Count
# 使用协议
def agreement(request):
    return render(request, "agreement.html", {})


# 忘记密码
def forgotten(request):
    return render(request, "forgotten.html", {})


def global_settings(request):
    return {"PROJECT_VERSION": settings.PROJECT_VERSION,
            'AUTHOR': settings.PROJECT_VERSION}


def handle_uploaded_file(f):
    with open(f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@check_login
def user_center(request):
    try:
        from mcstatus import MinecraftServer
        server = MinecraftServer.lookup(Para.MC_SERVER)
        status = server.status()

        mot = status.description['text']
        motd = str(mot)
        pos = motd.find('§')
        while pos != -1:
            motd = motd[:pos] + motd[pos + 2:]
            pos = motd.find('§')

        fav = status.favicon
        opn = status.players.online
        user = []

        if status.players.sample is not None:
            for e in status.players.sample:
                user.append({'name': e.name, 'id': e.id,"nickname":username_get_nickname(e.name)})


        announcements = announcement_list(request)

        na = len(DeclareAnimals.objects.all())
        nb = len(DeclareBuildings.objects.all())
        nc = len(Cases.objects.all())

        context = {
            'favicon': fav,
            'server_address': Para.MC_SERVER,
            'online_players_list': user,
            'online_players_number': opn,
            'number_buildings': nb,
            'number_animals': na,
            'number_cases': nc,
            'permissions': request.session['permissions'],
            'announcements': announcements
        }
        logging.debug(context)
    except Exception as e:
        print(e)
        logging.error(e)
        context = {}
    print(context)
    logging.debug(context['permissions'])
    return render(request, "dashboard/user_center.html", context)


@check_login
def page_announcement(request):
    announcements = announcement_list(request)
    print(announcements)
    content = {
        'announcements': announcements
    }
    return render(request, "dashboard/announcement/announcement.html", content)


@check_login
def page_declaration_center(request):
    animals = animals_list(request, 'all')
    buildings = buildings_list(request, 'all')
    content = {
        'animals': animals,
        'buildings': buildings,
        'skull': skull.skull_list(request,True),
        'permissions': request.session['permissions'],
    }
    return render(request, "dashboard/declaration/center.html", content)


@check_login
def page_call_the_police(request):
    return render(request, "dashboard/police/call_the_police.html", {})


@check_login
def page_declare_animals(request):
    my_animals = animals_list(request, 'user')
    content = {
        'my_animals': my_animals,
        'permissions': request.session['permissions'],
    }
    return render(request, "dashboard/declaration/animals.html", content)


@check_login
def page_declare_buildings(request):
    my_building = buildings_list(request, 'user')  # 这里选择获取当前登录用户的obj
    content = {
        'buildings': my_building,
        'permissions': request.session['permissions'],
    }
    return render(request, "dashboard/declaration/buildings.html", content)


@check_login
def page_papers(request):
    return render(request, "dashboard/papers/papers.html", {})


@check_login
def page_community(request):
    return render(request, "dashboard/papers/community.html", {})


@check_login
def page_project_plan(request):
    return render(request, "dashboard/papers/plans.html", {})


@check_login
def page_call_the_police(request):
    return render(request, "dashboard/police/call_the_police.html", {})


@check_login
def page_world_map(request):
    return render(request, "dashboard/world_map/map.html", {})


@check_login
def page_rookies(request):
    return render(request, "dashboard/rookies/rookies.html", {})


@check_login
def dashboard(request):
    context = {
        'avatar': request.session['avatar'],
        'nickname': request.session['nickname'],
        'permissions': request.session['permissions'],
        "menu":Menu.objects.filter(status=True)
    }

    return render(request, "dashboard/dashboard.html", context)
@check_login
def page_whitelist(request):
    white_list=whitelist(request)
    context = {
        'list': white_list,
        'permissions': request.session['permissions'],
        'len':len(white_list)
    }

    return render(request, "dashboard/ops/whitelist.html", context)

@check_login
def system_menu(request):
    context = {
        'permissions': request.session['permissions'],
        "menu":Menu.objects.all()
    }

    return render(request, "dashboard/system/menu.html", context)
@check_login
def page_wenjuan(request):

    _type=Conf.objects.get(key="wenjuan_type")
    context = {
        'permissions': request.session['permissions'],
        "wenjuan":problem_list(request),
        "type":json.loads(_type.content)
    }

    return render(request, "dashboard/wenjuan/wenjuan.html", context)


@check_login
def page_skull(request):
    
    context = {
        'permissions': request.session['permissions'],
        "skull":skull.skull_list(request)
    }

    return render(request, "dashboard/skull.html", context)

@check_login
def page_para(request):
    
    context = {
        'permissions': request.session['permissions'],
        "list":system.para_list(),
    }

    return render(request, "dashboard/system/parameter.html", context)

@check_login
def page_logs(request):
    
    _get=request.POST.get("_get",None)
    if(_get == None):
        page=1
    else:
        try:
            page=int(_get)
        except ValueError as e:
            page=1
    size=30
    # _list=system.logs_list(request,,page*size)
    _list=Logs.objects.exclude(code="info").order_by("-time")[(page-1)*size:page*size]
    _count=Logs.objects.annotate(count=Count("id")).exclude(code ="info").values("count")[0:1]
    _count=_count[0]['count']/size +1
    context = {
        'permissions': request.session['permissions'],
        "list":_list,
        "page":common.page("logs",_count,page)
    }

    return render(request, "dashboard/system/logs.html", context)

@check_login
def page_society(request):
    
    context = {
        'permissions': request.session['permissions'],
        "list":society.society_list()
    }

    return render(request, "dashboard/society/list.html", context)

def page_task_list(request):
    
    context = {
        'permissions': request.session['permissions'],
        "list":task.task_list(request,True),
        "type":"list",
        "title":"任务列表"
    }

    return render(request, "dashboard/task/list.html", context)
def page_task(request):
    
    context = {
        'permissions': request.session['permissions'],
        "list":task.task_list(request),
        "title":"我的任务"
    }

    return render(request, "dashboard/task/list.html", context)

@ensure_csrf_cookie
@check_login
@check_post
def dashboard_page(request):
    ensure_csrf_cookie(request)
    logging.info("Page Changed: " + request.POST.get("page", None))
    if request.POST.get("page", None) == "user_center":
        return user_center(request)

    if request.POST.get("page", None) == "announcement":
        return page_announcement(request)

    if request.POST.get("page", None) == "news":
        return render(request, "dashboard/settings/account.html", {})

    if request.POST.get("page", None) == "papers":
        return page_papers(request)

    if request.POST.get("page", None) == "project_plan":
        return page_project_plan(request)

    if request.POST.get("page", None) == "community":
        return page_community(request)

    if request.POST.get("page", None) == "declaration_center":
        return page_declaration_center(request)

    if request.POST.get("page", None) == "declare_buildings":
        return page_declare_buildings(request)

    if request.POST.get("page", None) == "declare_animals":
        return page_declare_animals(request)

    if request.POST.get("page", None) == "police_hall":
        return page_police_hall(request)

    if request.POST.get("page", None) == "call_the_police":
        return page_call_the_police(request)

    if request.POST.get("page", None) == "world_map":
        return page_world_map(request)

    if request.POST.get("page", None) == "rookies":
        return page_rookies(request)

    if request.POST.get("page", None) == "settings":
        return page_settings(request)
    if request.POST.get("page", None) == "whitelist":
        return page_whitelist(request)
    if request.POST.get("page", None) == "system_menu":
        return system_menu(request)
    if request.POST.get("page", None) == "wenjuan":
        return page_wenjuan(request)
    if request.POST.get("page", None) == "skull":
        return page_skull(request)
    if request.POST.get("page", None) == "logs":
        return page_logs(request)
    if request.POST.get("page", None) == "para":
        return page_para(request)
    if request.POST.get("page", None) == "society":
        return page_society(request)
    if request.POST.get("page", None) == "society_info":
        return society.society_info(request)
    if request.POST.get("page", None) == "task_list":
        return page_task_list(request)
    if request.POST.get("page", None) == "task":
        return page_task(request)

    return HttpResponse("Response: " + request.POST.get("page", None))
